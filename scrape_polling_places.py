#!/usr/bin/env python3
"""
Scrape polling place data from Virginia Department of Elections website.

The ELECT website provides Excel files with polling place information for each election.
This script downloads and parses those files into our JSON format.
"""

import json
import requests
import pandas as pd
from io import BytesIO
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
import time
import os


# Known polling place file URLs from Virginia elections website
POLLING_PLACE_URLS = {
    "2025_november_general": "https://www.elections.virginia.gov/media/registration-statistics/2025-November-General-Election-Day-Polling-Locations-20250912.xlsx",
    "2024_november_general": "https://www.elections.virginia.gov/media/registration-statistics/2024-November-General-Election-Day-Polling-Locations-(10-9-24).xlsx",
    "2025_june_democratic": "https://www.elections.virginia.gov/media/registration-statistics/2025-June-Democratic-Primary-Election-Day-Polling-Locations-(5-28-25).xlsx",
    "2025_june_republican": "https://www.elections.virginia.gov/media/registration-statistics/2025-June-Republican-Primary-Election-Day-Polling-Locations-(5-28-25).xlsx",
}


class PollingPlaceScraper:
    """Scraper for Virginia polling place data."""

    def __init__(self):
        self.geolocator = Nominatim(user_agent="csc-ep-tool/1.0")
        self.geocode_cache = {}

    def download_excel(self, url):
        """Download Excel file from URL."""
        print(f"Downloading from {url}...")
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            return BytesIO(response.content)
        except requests.RequestException as e:
            print(f"Error downloading file: {e}")
            return None

    def geocode_address(self, address, city, state="VA", zip_code=None):
        """
        Geocode an address to get latitude/longitude.
        Uses caching to avoid repeated requests for the same address.
        """
        # Create cache key
        full_address = f"{address}, {city}, {state}"
        if zip_code:
            full_address += f" {zip_code}"

        # Check cache first
        if full_address in self.geocode_cache:
            return self.geocode_cache[full_address]

        # Try to geocode
        try:
            time.sleep(1)  # Rate limiting - Nominatim requires max 1 request/sec
            location = self.geolocator.geocode(full_address)

            if location:
                result = {
                    "latitude": round(location.latitude, 4),
                    "longitude": round(location.longitude, 4)
                }
                self.geocode_cache[full_address] = result
                return result
            else:
                print(f"  Could not geocode: {full_address}")
                return None

        except (GeocoderTimedOut, GeocoderServiceError) as e:
            print(f"  Geocoding error for {full_address}: {e}")
            return None

    def parse_excel(self, excel_file):
        """
        Parse Excel file and extract polling place information.

        Expected columns may include:
        - Locality/County
        - Precinct Name/Number
        - Polling Place Name
        - Address
        - City
        - Zip
        """
        try:
            # Try to read all sheets (sometimes data is in a specific sheet)
            excel_data = pd.ExcelFile(excel_file)
            print(f"Available sheets: {excel_data.sheet_names}")

            # Usually the first sheet has the data
            df = pd.read_excel(excel_file, sheet_name=0)

            print(f"\nColumns found: {df.columns.tolist()}")
            print(f"Total rows: {len(df)}")
            print(f"\nFirst few rows:")
            print(df.head())

            return df

        except Exception as e:
            print(f"Error parsing Excel file: {e}")
            return None

    def normalize_column_names(self, df):
        """
        Normalize column names to handle variations in the Excel files.
        """
        # Create a mapping of possible column names to our standard names
        column_mapping = {
            # Locality/County variations
            'locality': 'county',
            'locality name': 'county',
            'county': 'county',
            'county name': 'county',
            'jurisdiction': 'county',

            # Precinct variations
            'precinct': 'precinct',
            'precinct name': 'precinct',
            'precinct number': 'precinct',
            'precinct #': 'precinct',
            'voting precinct name': 'precinct',

            # Polling place name variations
            'polling place': 'name',
            'polling place name': 'name',
            'polling location': 'name',
            'location name': 'name',
            'location': 'name',
            'name': 'name',

            # Address variations
            'address': 'address',
            'street address': 'address',
            'polling place address': 'address',
            'location address': 'address',
            'address line 1': 'address',
            'address line 2': 'address2',

            # City variations
            'city': 'city',
            'town': 'city',

            # Zip variations
            'zip': 'zip',
            'zip code': 'zip',
            'zipcode': 'zip',
        }

        # Normalize column names (lowercase, strip)
        df.columns = df.columns.str.lower().str.strip()

        # Rename columns based on mapping
        rename_dict = {}
        for col in df.columns:
            if col in column_mapping:
                rename_dict[col] = column_mapping[col]

        if rename_dict:
            df = df.rename(columns=rename_dict)
            print(f"Renamed columns: {rename_dict}")

        return df

    def convert_to_json_format(self, df, include_geocoding=False):
        """
        Convert DataFrame to our JSON format for polling places.

        Args:
            df: DataFrame with polling place data
            include_geocoding: If True, geocode addresses (slow!)
        """
        polling_places = []

        # Normalize column names
        df = self.normalize_column_names(df)

        print(f"\nColumns after normalization: {df.columns.tolist()}")

        # Check for required columns
        required_cols = ['county', 'name', 'address']
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            print(f"WARNING: Missing required columns: {missing_cols}")
            print("Available columns:", df.columns.tolist())
            return []

        # Process each row
        for idx, row in df.iterrows():
            try:
                # Skip rows with missing essential data
                if pd.isna(row['name']) or pd.isna(row['address']):
                    continue

                # Build address (combine address line 1 and 2 if present)
                address = str(row['address']).strip()
                if 'address2' in row and not pd.isna(row.get('address2')):
                    address2 = str(row['address2']).strip()
                    if address2:
                        address = f"{address}, {address2}"

                # Clean up zip code (sometimes they're concatenated or have extra digits)
                zip_code = str(row.get('zip', '')).strip() if 'zip' in row and not pd.isna(row.get('zip')) else ''
                if zip_code and len(zip_code) > 5:
                    # Take first 5 digits as main zip
                    zip_code = zip_code[:5]

                # Extract basic information
                place = {
                    "id": f"pp-{idx+1:04d}",
                    "name": str(row['name']).strip(),
                    "address": address,
                    "city": str(row.get('city', '')).strip() if 'city' in row and not pd.isna(row.get('city')) else '',
                    "county": str(row['county']).strip(),
                    "state": "VA",
                    "zip": zip_code,
                }

                # Get coordinates if requested
                if include_geocoding:
                    coords = self.geocode_address(
                        place['address'],
                        place['city'] or place['county'],
                        "VA",
                        place['zip']
                    )
                    if coords:
                        place["latitude"] = coords["latitude"]
                        place["longitude"] = coords["longitude"]
                    else:
                        # Default to Virginia center if geocoding fails
                        place["latitude"] = 37.5
                        place["longitude"] = -78.5
                else:
                    # Default coordinates (Virginia center)
                    place["latitude"] = 37.5
                    place["longitude"] = -78.5

                # Add placeholder data for fields not in source
                place["total_voters"] = 0  # Would need voter file data
                place["multi_state_registrations"] = 0
                place["recent_registrations"] = 0
                place["purged_voters"] = 0
                place["risk_score"] = 0

                polling_places.append(place)

                if (idx + 1) % 100 == 0:
                    print(f"Processed {idx + 1} locations...")

            except Exception as e:
                print(f"Error processing row {idx}: {e}")
                continue

        return polling_places

    def scrape(self, election="2024_november_general", include_geocoding=False):
        """
        Main scraping function.

        Args:
            election: Key from POLLING_PLACE_URLS dict
            include_geocoding: If True, geocode all addresses (VERY SLOW!)

        Returns:
            List of polling places in JSON format
        """
        url = POLLING_PLACE_URLS.get(election)
        if not url:
            print(f"Unknown election: {election}")
            print(f"Available elections: {list(POLLING_PLACE_URLS.keys())}")
            return []

        # Download Excel file
        excel_file = self.download_excel(url)
        if not excel_file:
            return []

        # Parse Excel
        df = self.parse_excel(excel_file)
        if df is None or df.empty:
            return []

        # Convert to JSON format
        print(f"\nConverting to JSON format...")
        if include_geocoding:
            print("WARNING: Geocoding enabled. This will be VERY slow (1 request/second).")
            print(f"Estimated time: {len(df) / 60:.1f} minutes")

        polling_places = self.convert_to_json_format(df, include_geocoding)

        print(f"\nSuccessfully converted {len(polling_places)} polling places")
        return polling_places


def main():
    """CLI interface for the scraper."""
    import argparse

    parser = argparse.ArgumentParser(description="Scrape Virginia polling place data")
    parser.add_argument(
        "--election",
        default="2024_november_general",
        choices=list(POLLING_PLACE_URLS.keys()),
        help="Which election to scrape"
    )
    parser.add_argument(
        "--geocode",
        action="store_true",
        help="Geocode addresses (SLOW - about 1 hour per 1000 locations)"
    )
    parser.add_argument(
        "--output",
        default="data/polling_places_scraped.json",
        help="Output JSON file path"
    )
    parser.add_argument(
        "--preview",
        action="store_true",
        help="Preview the Excel structure without converting"
    )

    args = parser.parse_args()

    # Create scraper
    scraper = PollingPlaceScraper()

    if args.preview:
        # Just download and show structure
        url = POLLING_PLACE_URLS[args.election]
        excel_file = scraper.download_excel(url)
        if excel_file:
            scraper.parse_excel(excel_file)
        return

    # Scrape data
    polling_places = scraper.scrape(args.election, args.geocode)

    if not polling_places:
        print("No data scraped. Exiting.")
        return

    # Save to file
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    with open(args.output, 'w') as f:
        json.dump(polling_places, f, indent=2)

    print(f"\nSaved {len(polling_places)} polling places to {args.output}")

    # Show summary
    counties = {}
    for place in polling_places:
        county = place['county']
        counties[county] = counties.get(county, 0) + 1

    print(f"\nTop 10 counties by polling place count:")
    for county, count in sorted(counties.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"  {county}: {count}")


if __name__ == "__main__":
    main()
