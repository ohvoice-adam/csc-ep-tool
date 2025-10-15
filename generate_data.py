#!/usr/bin/env python3
"""Generate mock polling place data for Virginia"""

import json
import random

# Virginia cities and counties with approximate coordinates
VA_LOCATIONS = [
    # Northern Virginia
    {"city": "Fairfax", "county": "Fairfax County", "lat": 38.8462, "lng": -77.3064},
    {"city": "Alexandria", "county": "Alexandria City", "lat": 38.8048, "lng": -77.0469},
    {"city": "Arlington", "county": "Arlington County", "lat": 38.8816, "lng": -77.0910},
    {"city": "Leesburg", "county": "Loudoun County", "lat": 39.1157, "lng": -77.5636},
    {"city": "Manassas", "county": "Prince William County", "lat": 38.7509, "lng": -77.4753},
    {"city": "Reston", "county": "Fairfax County", "lat": 38.9687, "lng": -77.3411},
    {"city": "Herndon", "county": "Fairfax County", "lat": 38.9696, "lng": -77.3861},
    {"city": "Vienna", "county": "Fairfax County", "lat": 38.9012, "lng": -77.2653},
    {"city": "Falls Church", "county": "Fairfax County", "lat": 38.8823, "lng": -77.1711},
    {"city": "Annandale", "county": "Fairfax County", "lat": 38.8304, "lng": -77.2164},

    # Richmond area
    {"city": "Richmond", "county": "Richmond City", "lat": 37.5407, "lng": -77.4360},
    {"city": "Henrico", "county": "Henrico County", "lat": 37.6526, "lng": -77.4847},
    {"city": "Chesterfield", "county": "Chesterfield County", "lat": 37.3771, "lng": -77.5047},
    {"city": "Mechanicsville", "county": "Hanover County", "lat": 37.6088, "lng": -77.3733},
    {"city": "Glen Allen", "county": "Henrico County", "lat": 37.6637, "lng": -77.4905},

    # Hampton Roads
    {"city": "Virginia Beach", "county": "Virginia Beach City", "lat": 36.8529, "lng": -75.9780},
    {"city": "Norfolk", "county": "Norfolk City", "lat": 36.8508, "lng": -76.2859},
    {"city": "Chesapeake", "county": "Chesapeake City", "lat": 36.7682, "lng": -76.2875},
    {"city": "Newport News", "county": "Newport News City", "lat": 37.0871, "lng": -76.4730},
    {"city": "Hampton", "county": "Hampton City", "lat": 37.0299, "lng": -76.3452},
    {"city": "Portsmouth", "county": "Portsmouth City", "lat": 36.8354, "lng": -76.2983},
    {"city": "Suffolk", "county": "Suffolk City", "lat": 36.7282, "lng": -76.5836},

    # Central Virginia
    {"city": "Charlottesville", "county": "Albemarle County", "lat": 38.0293, "lng": -78.4767},
    {"city": "Lynchburg", "county": "Lynchburg City", "lat": 37.4138, "lng": -79.1422},
    {"city": "Fredericksburg", "county": "Spotsylvania County", "lat": 38.3032, "lng": -77.4605},

    # Western Virginia
    {"city": "Roanoke", "county": "Roanoke City", "lat": 37.2710, "lng": -79.9414},
    {"city": "Blacksburg", "county": "Montgomery County", "lat": 37.2296, "lng": -80.4139},
    {"city": "Salem", "county": "Salem City", "lat": 37.2935, "lng": -80.0547},
    {"city": "Christiansburg", "county": "Montgomery County", "lat": 37.1299, "lng": -80.4089},

    # Other cities
    {"city": "Petersburg", "county": "Petersburg City", "lat": 37.2279, "lng": -77.4019},
    {"city": "Danville", "county": "Danville City", "lat": 36.5860, "lng": -79.3950},
    {"city": "Bristol", "county": "Bristol City", "lat": 36.5951, "lng": -82.1887},
    {"city": "Harrisonburg", "county": "Harrisonburg City", "lat": 38.4496, "lng": -78.8689},
    {"city": "Winchester", "county": "Winchester City", "lat": 39.1857, "lng": -78.1633},
    {"city": "Staunton", "county": "Staunton City", "lat": 38.1496, "lng": -79.0717},
    {"city": "Waynesboro", "county": "Waynesboro City", "lat": 38.0685, "lng": -78.8895},
]

# Building types for polling places
BUILDING_TYPES = [
    "Elementary School", "Middle School", "High School", "Primary School",
    "Community Center", "Recreation Center", "Civic Center",
    "Public Library", "Baptist Church", "Methodist Church", "Presbyterian Church",
    "Fire Station", "VFW Post", "American Legion Post",
    "Senior Center", "Community Hall", "Township Hall",
]

# Street names
STREET_NAMES = [
    "Main", "Oak", "Maple", "Pine", "Elm", "Cedar", "Birch", "Spruce", "Willow",
    "Washington", "Jefferson", "Madison", "Monroe", "Jackson", "Lincoln", "Grant",
    "First", "Second", "Third", "Fourth", "Fifth", "Broad", "Market", "Church",
    "School", "Park", "River", "Lake", "Hill", "Valley", "Ridge", "Mountain",
    "Colonial", "Heritage", "Liberty", "Freedom", "Independence", "Victory",
]

STREET_TYPES = ["St", "Ave", "Dr", "Rd", "Ln", "Blvd", "Way", "Ct", "Pl", "Cir"]

# President names for variety
PRESIDENTS = [
    "Washington", "Adams", "Jefferson", "Madison", "Monroe", "Jackson", "Van Buren",
    "Harrison", "Tyler", "Polk", "Taylor", "Fillmore", "Pierce", "Buchanan",
    "Lincoln", "Grant", "Hayes", "Garfield", "Arthur", "Cleveland", "McKinley",
    "Roosevelt", "Taft", "Wilson", "Harding", "Coolidge", "Hoover", "Truman",
    "Eisenhower", "Kennedy", "Johnson", "Nixon", "Ford", "Carter", "Reagan",
]

def generate_zip(location):
    """Generate a realistic zip code for the location"""
    # Use base zips for each area
    base_zips = {
        "Richmond City": 23219,
        "Henrico County": 23294,
        "Chesterfield County": 23832,
        "Fairfax County": 22030,
        "Alexandria City": 22314,
        "Arlington County": 22203,
        "Loudoun County": 20175,
        "Prince William County": 20110,
        "Virginia Beach City": 23451,
        "Norfolk City": 23510,
        "Chesapeake City": 23320,
        "Newport News City": 23601,
        "Hampton City": 23669,
        "Portsmouth City": 23701,
        "Suffolk City": 23434,
    }
    base = base_zips.get(location["county"], 20000)
    return base + random.randint(0, 50)

def generate_address():
    """Generate a random street address"""
    number = random.randint(100, 9999)
    street = random.choice(STREET_NAMES)
    street_type = random.choice(STREET_TYPES)
    return f"{number} {street} {street_type}"

def generate_polling_place(idx, location):
    """Generate a single polling place"""
    # Add some randomness to coordinates (within ~5 mile radius)
    lat_offset = random.uniform(-0.05, 0.05)
    lng_offset = random.uniform(-0.05, 0.05)

    # Generate voters with realistic distribution
    base_voters = random.choice([600, 800, 1000, 1200, 1400, 1600, 1800, 2000, 2200, 2400])
    voters = base_voters + random.randint(-200, 300)

    # Multi-state registrations (1-5% of voters)
    multi_state = int(voters * random.uniform(0.01, 0.05))

    # Recent registrations (2-15% of voters)
    recent_reg = int(voters * random.uniform(0.02, 0.15))

    # Purged voters (0.5-3% of voters)
    purged = int(voters * random.uniform(0.005, 0.03))

    # Calculate risk score based on factors
    risk_score = 0

    # High voter count increases risk
    if voters > 2000:
        risk_score += 25
    elif voters > 1500:
        risk_score += 15
    elif voters > 1000:
        risk_score += 8

    # Multi-state registration rate
    multi_rate = multi_state / voters
    risk_score += (multi_rate * 600)  # Moderate impact

    # Recent registration rate
    recent_rate = recent_reg / voters
    risk_score += (recent_rate * 120)  # Moderate impact

    # Purge rate
    purge_rate = purged / voters
    risk_score += (purge_rate * 300)  # Moderate impact

    # Add randomness to create variation
    risk_score = int(risk_score + random.randint(-5, 10))

    # Some locations are randomly higher risk (equipment, staffing, historical issues, etc.)
    if random.random() < 0.15:  # 15% chance
        risk_score += random.randint(15, 35)

    risk_score = max(20, min(100, risk_score))  # Clamp between 20-100

    # Generate name
    if random.random() < 0.3:
        # Use a president name
        name = f"{random.choice(PRESIDENTS)} {random.choice(BUILDING_TYPES)}"
    else:
        # Use a regular name
        name_part = random.choice(PRESIDENTS + STREET_NAMES)
        name = f"{name_part} {random.choice(BUILDING_TYPES)}"

    return {
        "id": f"pp-{idx+1:04d}",
        "name": name,
        "address": generate_address(),
        "city": location["city"],
        "county": location["county"],
        "state": "VA",
        "zip": str(generate_zip(location)),
        "latitude": round(location["lat"] + lat_offset, 4),
        "longitude": round(location["lng"] + lng_offset, 4),
        "total_voters": voters,
        "multi_state_registrations": multi_state,
        "recent_registrations": recent_reg,
        "purged_voters": purged,
        "risk_score": risk_score
    }

def generate_dataset(count=1000):
    """Generate the full dataset"""
    polling_places = []

    for i in range(count):
        # Distribute across locations with more in populous areas
        if i < 300:
            # First 300 in Northern Virginia
            location = random.choice([loc for loc in VA_LOCATIONS if "Fairfax" in loc["county"] or "Arlington" in loc["county"] or "Alexandria" in loc["city"] or "Loudoun" in loc["county"] or "Prince William" in loc["county"]])
        elif i < 500:
            # Next 200 in Hampton Roads
            location = random.choice([loc for loc in VA_LOCATIONS if "Virginia Beach" in loc["city"] or "Norfolk" in loc["city"] or "Chesapeake" in loc["city"] or "Newport News" in loc["city"] or "Hampton" in loc["city"]])
        elif i < 700:
            # Next 200 in Richmond area
            location = random.choice([loc for loc in VA_LOCATIONS if "Richmond" in loc["county"] or "Henrico" in loc["county"] or "Chesterfield" in loc["county"]])
        else:
            # Remaining distributed across all locations
            location = random.choice(VA_LOCATIONS)

        polling_places.append(generate_polling_place(i, location))

    return polling_places

if __name__ == "__main__":
    print("Generating 1000 polling places...")
    polling_places = generate_dataset(1000)

    # Save to file
    with open("data/polling_places.json", "w") as f:
        json.dump(polling_places, f, indent=2)

    print(f"Generated {len(polling_places)} polling places")

    # Print some statistics
    total_voters = sum(p["total_voters"] for p in polling_places)
    avg_risk = sum(p["risk_score"] for p in polling_places) / len(polling_places)
    high_risk = len([p for p in polling_places if p["risk_score"] >= 67])

    print(f"Total voters: {total_voters:,}")
    print(f"Average risk score: {avg_risk:.1f}")
    print(f"High risk locations (67+): {high_risk}")

    # County distribution
    counties = {}
    for p in polling_places:
        counties[p["county"]] = counties.get(p["county"], 0) + 1

    print(f"\nTop 10 counties by polling place count:")
    for county, count in sorted(counties.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"  {county}: {count}")
