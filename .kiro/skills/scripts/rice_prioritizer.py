#!/usr/bin/env python3
"""RICE prioritization calculator."""

import argparse
import csv
import json
import sys
from typing import List, Dict

IMPACT_MAP = {
    "minimal": 0.25,
    "low": 0.5,
    "medium": 1.0,
    "high": 2.0,
    "massive": 3.0
}

EFFORT_MAP = {
    "xs": 0.5,
    "s": 1,
    "m": 3,
    "l": 6,
    "xl": 12
}

CONFIDENCE_MAP = {
    "low": 0.5,
    "medium": 0.8,
    "high": 1.0
}

def calculate_rice(reach: int, impact: str, confidence: str, effort: str) -> float:
    """Calculate RICE score."""
    i = IMPACT_MAP.get(impact.lower(), 1.0)
    c = CONFIDENCE_MAP.get(confidence.lower(), 0.8)
    e = EFFORT_MAP.get(effort.lower(), 3)
    return (reach * i * c) / e

def prioritize_features(csv_file: str) -> List[Dict]:
    """Read CSV and calculate RICE scores."""
    features = []
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rice = calculate_rice(
                int(row['reach']),
                row['impact'],
                row['confidence'],
                row['effort']
            )
            features.append({
                'name': row['name'],
                'reach': int(row['reach']),
                'impact': row['impact'],
                'confidence': row['confidence'],
                'effort': row['effort'],
                'rice_score': round(rice, 2),
                'description': row.get('description', '')
            })
    
    return sorted(features, key=lambda x: x['rice_score'], reverse=True)

def generate_sample():
    """Generate sample CSV."""
    sample = """name,reach,impact,confidence,effort,description
Password History,500,high,high,m,Save last 10 generated passwords
Dark Mode Toggle,800,medium,high,s,User-selectable theme
Breach Checking,300,massive,medium,l,Check against HaveIBeenPwned
Export to File,200,low,high,s,Save passwords to CSV
Pronounceable Passwords,400,medium,low,m,Generate memorable passwords"""
    print(sample)

def main():
    parser = argparse.ArgumentParser(description="RICE prioritization")
    parser.add_argument("csv_file", nargs='?', help="CSV file with features")
    parser.add_argument("--output", choices=["text", "json", "csv"], default="text")
    parser.add_argument("--capacity", type=int, help="Team capacity (person-months)")
    parser.add_argument("--sample", action="store_true", help="Generate sample CSV")
    args = parser.parse_args()

    if args.sample:
        generate_sample()
        return

    if not args.csv_file:
        print("Error: csv_file required (or use --sample)")
        sys.exit(1)

    features = prioritize_features(args.csv_file)

    if args.output == "json":
        print(json.dumps(features, indent=2))
    elif args.output == "csv":
        writer = csv.DictWriter(sys.stdout, fieldnames=features[0].keys())
        writer.writeheader()
        writer.writerows(features)
    else:
        print("RICE Prioritization Results")
        print("=" * 80)
        for i, f in enumerate(features, 1):
            priority = "🔴" if f['rice_score'] > 100 else "🟡" if f['rice_score'] > 50 else "🟢"
            print(f"{i}. {priority} {f['name']} (RICE: {f['rice_score']})")
            print(f"   Reach: {f['reach']} | Impact: {f['impact']} | Confidence: {f['confidence']} | Effort: {f['effort']}")
            print(f"   {f['description']}")
            print()
        
        if args.capacity:
            total_effort = sum(EFFORT_MAP.get(f['effort'].lower(), 3) for f in features)
            print(f"Total effort: {total_effort} person-months")
            print(f"Team capacity: {args.capacity} person-months")
            print(f"Can complete: {args.capacity / total_effort * 100:.0f}% of features")

if __name__ == "__main__":
    main()
