#!/usr/bin/env python3
"""Scaffold a GitHub Actions workflow from a template."""

import argparse
import os
import sys

TEMPLATES = {
    "node": """\
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - run: npm ci
      - run: npm run lint
      - run: npm test
      - run: npm run build
""",
    "java": """\
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with:
          java-version: '17'
          distribution: 'temurin'
      - run: javac *.java
      - run: jar cfe app.jar Main *.class
      - uses: actions/upload-artifact@v4
        with:
          name: app-jar
          path: app.jar
""",
    "python": """\
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - run: pip install -r requirements.txt
      - run: python -m pytest
""",
}

def main():
    parser = argparse.ArgumentParser(description="Scaffold CI workflow")
    parser.add_argument("--stack", choices=list(TEMPLATES.keys()), required=True)
    parser.add_argument("--trigger", choices=["push", "pr", "tag"], default="push")
    parser.add_argument("--out", default=".github/workflows/ci.yml")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--output", choices=["text", "json"], default="text")
    args = parser.parse_args()

    content = TEMPLATES[args.stack]

    if args.dry_run:
        print(f"--- DRY RUN: would write to {args.out} ---")
        print(content)
        sys.exit(0)

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w") as f:
        f.write(content)

    if args.output == "json":
        import json
        print(json.dumps({"written": args.out, "stack": args.stack}))
    else:
        print(f"✓ Written: {args.out}")

if __name__ == "__main__":
    main()
