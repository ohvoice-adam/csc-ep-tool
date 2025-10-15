#!/usr/bin/env python3
"""Generate mock report data for Virginia polling places"""

import json
import random
from datetime import datetime, timedelta

# Issue types
ISSUE_TYPES = [
    "Long lines",
    "Equipment failure",
    "Equipment failure",  # Duplicate to make more common
    "Accessibility issue",
    "Staffing problem",
    "Voter intimidation",
    "ID requirements issue",
    "Other",
]

# Sample reporter names
FIRST_NAMES = [
    "James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda",
    "William", "Barbara", "David", "Elizabeth", "Richard", "Susan", "Joseph", "Jessica",
    "Thomas", "Sarah", "Charles", "Karen", "Christopher", "Nancy", "Daniel", "Lisa",
    "Matthew", "Betty", "Anthony", "Margaret", "Mark", "Sandra", "Donald", "Ashley",
    "Steven", "Kimberly", "Paul", "Emily", "Andrew", "Donna", "Joshua", "Michelle",
]

LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
    "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson",
    "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson",
    "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson", "Walker",
]

# Description templates by issue type
DESCRIPTIONS = {
    "Long lines": [
        "Wait time is over {time} hours. Many {group} voters are struggling.",
        "Line wraps around the building. Estimated {time} hour wait.",
        "Over {count} people in line at {time_str}. Not enough voting machines.",
        "Extremely long wait times. Some voters leaving without voting.",
        "{count}+ people waiting. Only {machines} machines working.",
    ],
    "Equipment failure": [
        "{count} voting machines are down. Poll workers waiting for replacements.",
        "Check-in tablets not working. Using paper backup lists causing delays.",
        "Scanner jammed. Ballots piling up, not being counted.",
        "Electronic pollbook crashed. Unable to verify voters quickly.",
        "Ballot marking device broken. Long delays for accessible voting.",
    ],
    "Accessibility issue": [
        "Wheelchair ramp blocked by {obstacle}. Disabled voters cannot enter easily.",
        "No accessible parking available. Disabled voters having to walk long distance.",
        "Accessible voting machine is broken. No alternative provided.",
        "Building entrance has stairs only. No ramp or elevator access.",
        "Signage unclear for voters with visual impairments.",
    ],
    "Staffing problem": [
        "Only {count} poll workers for a very busy location. Check-in is very slow.",
        "Insufficient staff. Voters waiting {time} minutes just to check in.",
        "Poll workers appear untrained. Giving conflicting information to voters.",
        "Not enough staff to manage the crowds. Very disorganized.",
        "Chief election officer not present. Workers unsure how to handle issues.",
    ],
    "Voter intimidation": [
        "Individuals outside polling place challenging voters aggressively.",
        "Suspicious activity near entrance. Voters feel uncomfortable.",
        "People taking photos of voters entering and leaving.",
        "Verbal confrontations happening in parking lot.",
        "Intimidating presence near polling place entrance.",
    ],
    "ID requirements issue": [
        "Poll workers requiring photo ID from all voters, including those with utility bills.",
        "Confusion about ID requirements. Workers giving incorrect information.",
        "Valid IDs being rejected inappropriately.",
        "Voters with proper documentation being turned away.",
        "Inconsistent application of ID requirements.",
    ],
    "Other": [
        "Power outage affecting voting equipment.",
        "Heating/cooling system not working. Uncomfortable conditions.",
        "Insufficient parking. Voters circling for {time} minutes.",
        "Incorrect precinct information given. Voters sent to wrong location.",
        "Ballots running low. Concern about running out.",
    ],
}

def generate_description(issue_type):
    """Generate a description for the issue type"""
    template = random.choice(DESCRIPTIONS.get(issue_type, DESCRIPTIONS["Other"]))

    # Fill in template variables
    replacements = {
        "{time}": str(random.choice([1, 1.5, 2, 2.5, 3, 3.5, 4])),
        "{count}": str(random.choice([50, 75, 100, 150, 200, 250, 300])),
        "{machines}": str(random.choice([2, 3, 4, 5])),
        "{time_str}": random.choice(["7am", "8am", "9am", "noon", "5pm", "6pm"]),
        "{group}": random.choice(["elderly", "disabled", "working", "first-time"]),
        "{obstacle}": random.choice(["temporary fencing", "construction materials", "parked vehicles", "snow/ice"]),
    }

    for key, value in replacements.items():
        template = template.replace(key, value)

    return template

def generate_email(first_name, last_name):
    """Generate a realistic email address"""
    domains = ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "icloud.com", "aol.com"]
    patterns = [
        f"{first_name.lower()}.{last_name.lower()}@{random.choice(domains)}",
        f"{first_name[0].lower()}{last_name.lower()}@{random.choice(domains)}",
        f"{first_name.lower()}{last_name[0].lower()}@{random.choice(domains)}",
        f"{first_name.lower()}{random.randint(1, 99)}@{random.choice(domains)}",
    ]
    return random.choice(patterns)

def generate_phone():
    """Generate a Virginia phone number"""
    area_codes = ["703", "571", "804", "757", "540", "434"]
    area = random.choice(area_codes)
    prefix = random.randint(200, 999)
    line = random.randint(1000, 9999)
    return f"{area}-{prefix}-{line:04d}"

def generate_timestamp():
    """Generate a timestamp for election day"""
    # Election day 2024-11-05, between 6am and 8pm
    base = datetime(2024, 11, 5, 6, 0, 0)
    hours = random.randint(0, 14)  # 6am to 8pm
    minutes = random.randint(0, 59)
    return (base + timedelta(hours=hours, minutes=minutes)).isoformat() + "Z"

def generate_report(idx, polling_place_ids):
    """Generate a single report"""
    first_name = random.choice(FIRST_NAMES)
    last_name = random.choice(LAST_NAMES)
    issue_type = random.choice(ISSUE_TYPES)

    # Determine status - most are reported, some investigating, few resolved
    status_choice = random.random()
    if status_choice < 0.7:
        status = "reported"
    elif status_choice < 0.9:
        status = "investigating"
    else:
        status = "resolved"

    # More likely to report on high-risk locations
    # But we don't have access to risk scores here, so just random
    polling_place_id = random.choice(polling_place_ids)

    return {
        "id": f"rpt-{idx+1:03d}",
        "polling_place_id": polling_place_id,
        "reporter_name": f"{first_name} {last_name}",
        "reporter_email": generate_email(first_name, last_name),
        "reporter_phone": generate_phone(),
        "issue_type": issue_type,
        "description": generate_description(issue_type),
        "timestamp": generate_timestamp(),
        "status": status
    }

def generate_reports(count=75, polling_places_file="data/polling_places.json"):
    """Generate reports for random polling places"""
    # Load polling places to get IDs
    with open(polling_places_file, "r") as f:
        polling_places = json.load(f)

    polling_place_ids = [p["id"] for p in polling_places]

    # Generate reports
    reports = []
    for i in range(count):
        reports.append(generate_report(i, polling_place_ids))

    # Sort by timestamp
    reports.sort(key=lambda x: x["timestamp"])

    return reports

if __name__ == "__main__":
    print("Generating 75 reports...")
    reports = generate_reports(75)

    # Save to file
    with open("data/reports.json", "w") as f:
        json.dump(reports, f, indent=2)

    print(f"Generated {len(reports)} reports")

    # Print some statistics
    issue_counts = {}
    for report in reports:
        issue_type = report["issue_type"]
        issue_counts[issue_type] = issue_counts.get(issue_type, 0) + 1

    print(f"\nReports by issue type:")
    for issue_type, count in sorted(issue_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  {issue_type}: {count}")

    status_counts = {}
    for report in reports:
        status = report["status"]
        status_counts[status] = status_counts.get(status, 0) + 1

    print(f"\nReports by status:")
    for status, count in sorted(status_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  {status}: {count}")
