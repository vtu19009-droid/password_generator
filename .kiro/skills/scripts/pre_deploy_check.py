#!/usr/bin/env python3
"""Pre-deployment validation checks for Java desktop app."""

import argparse
import subprocess
import sys
import json
from pathlib import Path

def check_compile():
    """Check if Java code compiles."""
    result = subprocess.run(
        ["javac", "PasswordGenerator.java"],
        capture_output=True,
        text=True
    )
    return {
        "passed": result.returncode == 0,
        "output": result.stderr if result.stderr else "Compiled successfully"
    }

def check_conflicts(branch: str):
    """Check for merge conflicts with main."""
    result = subprocess.run(
        ["git", "merge-tree", "main", branch],
        capture_output=True,
        text=True
    )
    has_conflicts = "<<<<<<" in result.stdout
    return {
        "passed": not has_conflicts,
        "conflicts": has_conflicts
    }

def check_changelog():
    """Check if CHANGELOG.md exists and has recent entry."""
    changelog_path = Path("CHANGELOG.md")
    if not changelog_path.exists():
        return {"passed": False, "message": "CHANGELOG.md not found"}
    
    content = changelog_path.read_text()
    has_entry = "##" in content
    return {
        "passed": has_entry,
        "message": "Changelog has entries" if has_entry else "No version entries"
    }

def check_version_tag():
    """Check if version tag is ready."""
    result = subprocess.run(
        ["git", "tag", "-l"],
        capture_output=True,
        text=True
    )
    tags = result.stdout.strip().split("\n") if result.stdout.strip() else []
    return {
        "passed": len(tags) > 0,
        "tags": tags,
        "latest": tags[-1] if tags else None
    }

def main():
    parser = argparse.ArgumentParser(description="Pre-deploy checks")
    parser.add_argument("--branch", help="Feature branch name")
    parser.add_argument("--compile", action="store_true")
    parser.add_argument("--conflicts", action="store_true")
    parser.add_argument("--changelog", action="store_true")
    parser.add_argument("--version", action="store_true")
    parser.add_argument("--output", choices=["text", "json"], default="text")
    args = parser.parse_args()

    results = {}
    
    if args.compile:
        results["compile"] = check_compile()
    if args.conflicts and args.branch:
        results["conflicts"] = check_conflicts(args.branch)
    if args.changelog:
        results["changelog"] = check_changelog()
    if args.version:
        results["version"] = check_version_tag()

    if args.output == "json":
        print(json.dumps(results, indent=2))
    else:
        for k, v in results.items():
            status = "✓" if v["passed"] else "✗"
            print(f"{status} {k}")
            if "message" in v:
                print(f"  {v['message']}")

    failed = [k for k, v in results.items() if not v.get("passed")]
    sys.exit(1 if failed else 0)

if __name__ == "__main__":
    main()
