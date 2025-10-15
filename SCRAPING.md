# Polling Place Data Scraping

This document explains how to scrape real polling place data from the Virginia Department of Elections website.

## Overview

The Virginia Department of Elections publishes Excel files containing polling place information for each election. These files are available at:
https://www.elections.virginia.gov/resultsreports/registration-statistics/

The `scrape_polling_places.py` script downloads and parses these Excel files into our JSON format.

## Quick Start

### Install Dependencies

```bash
pip install pandas openpyxl requests geopy
```

### Basic Usage

Scrape the 2024 November General Election polling places (default):

```bash
python3 scrape_polling_places.py
```

This will create `data/polling_places_scraped.json` with 2,538 polling places.

### Available Elections

You can scrape data from different elections:

```bash
# 2024 November General (default)
python3 scrape_polling_places.py --election 2024_november_general

# 2025 November General
python3 scrape_polling_places.py --election 2025_november_general

# 2025 June Democratic Primary
python3 scrape_polling_places.py --election 2025_june_democratic

# 2025 June Republican Primary
python3 scrape_polling_places.py --election 2025_june_republican
```

### Preview Mode

To see the structure of the Excel file without converting:

```bash
python3 scrape_polling_places.py --preview
```

### Custom Output File

```bash
python3 scrape_polling_places.py --output my_data.json
```

## Geocoding

By default, the scraper uses placeholder coordinates (Virginia center: 37.5, -78.5) for all locations.

To geocode addresses and get real coordinates:

```bash
python3 scrape_polling_places.py --geocode
```

**WARNING**: Geocoding is VERY slow:
- Uses OpenStreetMap Nominatim API (free, but rate-limited to 1 request/second)
- For 2,538 locations, this takes approximately **42 minutes**
- Coordinates are cached to avoid re-geocoding the same address

### Geocoding Best Practices

1. **Test with a subset first**: Modify the script to process only the first 10-20 locations
2. **Run overnight**: For full dataset geocoding, run it as a background process
3. **Cache is saved**: Re-running will use cached coordinates for addresses already geocoded

## Data Format

The scraper produces JSON in our application format:

```json
{
  "id": "pp-0001",
  "name": "CHINCOTEAGUE CENTER",
  "address": "6155 Community Dr",
  "city": "Chincoteague",
  "county": "ACCOMACK COUNTY",
  "state": "VA",
  "zip": "23336",
  "latitude": 37.5,
  "longitude": -78.5,
  "total_voters": 0,
  "multi_state_registrations": 0,
  "recent_registrations": 0,
  "purged_voters": 0,
  "risk_score": 0
}
```

### Field Notes

- **id**: Sequential ID assigned during scraping (pp-0001, pp-0002, etc.)
- **name**: Official polling place name from ELECT
- **address**: Complete address (combines Address Line 1 and 2)
- **city**: City name
- **county**: County/City name (Virginia has independent cities)
- **zip**: 5-digit ZIP code (cleaned from source data)
- **latitude/longitude**: Coordinates (placeholder unless --geocode is used)
- **total_voters**: Set to 0 (requires voter file data)
- **multi_state_registrations**: Set to 0 (requires voter file data)
- **recent_registrations**: Set to 0 (requires voter file data)
- **purged_voters**: Set to 0 (requires voter file data)
- **risk_score**: Set to 0 (requires calculation based on voter data)

## Statistics (2024 November General)

- **Total Polling Places**: 2,538
- **Counties/Cities**: 133 localities

**Top 10 by Polling Place Count**:
1. Fairfax County: 264
2. Virginia Beach City: 108
3. Loudoun County: 107
4. Prince William County: 103
5. Henrico County: 90
6. Chesterfield County: 78
7. Richmond City: 72
8. Chesapeake City: 64
9. Arlington County: 54
10. Norfolk City: 48

## Integration with Application

### Replace Mock Data

To use scraped data instead of generated mock data:

```bash
# Backup current mock data
mv data/polling_places.json data/polling_places_mock.json

# Use scraped data
python3 scrape_polling_places.py --output data/polling_places.json
```

### Merge with Voter Data

The scraped polling places have placeholder values for voter statistics. To populate these fields:

1. Obtain voter file data (e.g., from Catalist via CTA PAD BigQuery)
2. Match voters to polling places by precinct/address
3. Calculate statistics (total voters, multi-state registrations, etc.)
4. Calculate risk scores using the algorithm in `generate_data.py`

## Updating Data

To refresh polling place data before an election:

1. Check https://www.elections.virginia.gov/resultsreports/registration-statistics/
2. Note the election date and file name
3. Update the URL in `POLLING_PLACE_URLS` dict if needed
4. Run the scraper with the appropriate election parameter

## Troubleshooting

### Connection Errors

If download fails:
- Check your internet connection
- Verify the URL is still valid (ELECT may change file locations)
- Try again later (temporary server issues)

### Parsing Errors

If Excel parsing fails:
- Run with `--preview` to see the structure
- Check if column names have changed
- Update `normalize_column_names()` mapping if needed

### Geocoding Issues

If geocoding fails or times out:
- Reduce the rate limit delay in `geocode_address()`
- Use a different geocoding service (requires API key)
- Accept placeholder coordinates and geocode in a separate process

## Future Enhancements

Potential improvements to the scraper:

1. **Batch Geocoding**: Use a commercial geocoding API with higher rate limits
2. **Database Storage**: Store scraped data directly in PostgreSQL
3. **Change Detection**: Compare with previous scrape to detect changes
4. **Precinct Mapping**: Link to precinct shapefiles for geographic analysis
5. **Historical Tracking**: Store multiple snapshots to track polling place changes
6. **Data Validation**: Verify addresses and flag anomalies
7. **Auto-Update**: Schedule regular scrapes to keep data current

## License

This scraper is for defensive security and election protection purposes only.
