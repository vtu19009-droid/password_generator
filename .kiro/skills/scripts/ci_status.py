#!/usr/bin/env python3
"""Check CI run status via GitHub API."""

import argparse
import urllib.request
import json
import sys
import os

GH_API = "https://api.github.com"

def get_runs(repo: str, branch: str, token: str):
    url = f"{GH_API}/repos/{repo}/actions/runs?branch={branch}&per_page=5"
    req = urllib.request.Request(url, headers={
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json"
    })
    with urllib.request.urlopen(req, timeout=10) as r:
        return json.loads(r.read())

def main():
    parser = argparse.ArgumentParser(description="Check CI run status")
    parser.add_argument("--repo", required=True, help="owner/repo")
    parser.add_argument("--branch", default="main")
    parser.add_argument("--output", choices=["text", "json"], default="text")
    parser.add_argument("--notify", action="store_true")
    parser.add_argument("--status", help="Status to report (for --notify)")
    parser.add_argument("--env", help="Environment context (for --notify)")
    args = parser.parse_args()

    token = os.getenv("GITHUB_TOKEN")
    if not token:
        print("✗ GITHUB_TOKEN not set", file=sys.stderr)
        sys.exit(1)

    try:
        data = get_runs(args.repo, args.branch, token)
        runs = data.get("workflow_runs", [])

        if args.output == "json":
            summary = [{
                "id": r["id"],
                "status": r["status"],
                "conclusion": r["conclusion"],
                "name": r["name"]
            } for r in runs]
            print(json.dumps(summary, indent=2))
        else:
            for r in runs:
                icon = "✓" if r["conclusion"] == "success" else "✗"
                print(f"{icon} [{r['conclusion'] or r['status']}] {r['name']}")

        latest = runs[0] if runs else {}
        sys.exit(0 if latest.get("conclusion") == "success" else 1)

    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
