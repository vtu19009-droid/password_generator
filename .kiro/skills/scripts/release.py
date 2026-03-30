#!/usr/bin/env python3
"""Create GitHub release with JAR artifact."""

import argparse
import subprocess
import sys
import json
from datetime import datetime
from pathlib import Path

def create_release(version: str, dry_run: bool):
    """Create GitHub release."""
    if not version.startswith("v"):
        version = f"v{version}"
    
    jar_path = Path("PasswordGenerator.jar")
    if not jar_path.exists():
        return {"success": False, "error": "JAR not found. Run build first."}
    
    tag_cmd = ["git", "tag", "-a", version, "-m", f"Release {version}"]
    if dry_run:
        print(f"[DRY RUN] Would run: {' '.join(tag_cmd)}")
    else:
        subprocess.run(tag_cmd, check=True)
        subprocess.run(["git", "push", "password_origin", version], check=True)
    
    release_cmd = [
        "gh", "release", "create", version,
        "PasswordGenerator.jar",
        "--title", f"Release {version}",
        "--generate-notes"
    ]
    
    if dry_run:
        print(f"[DRY RUN] Would run: {' '.join(release_cmd)}")
        return {
            "success": True,
            "dry_run": True,
            "version": version,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    result = subprocess.run(release_cmd, capture_output=True, text=True)
    return {
        "success": result.returncode == 0,
        "version": version,
        "output": result.stdout,
        "error": result.stderr if result.returncode != 0 else None
    }

def main():
    parser = argparse.ArgumentParser(description="Create GitHub release")
    parser.add_argument("--version", required=True, help="Version (e.g., 1.0.0 or v1.0.0)")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--output", choices=["text", "json"], default="text")
    args = parser.parse_args()

    result = create_release(args.version, args.dry_run)

    if args.output == "json":
        print(json.dumps(result, indent=2))
    else:
        status = "✓" if result["success"] else "✗"
        mode = " (DRY RUN)" if args.dry_run else ""
        print(f"{status} Release {args.version}{mode}")
        if "error" in result and result["error"]:
            print(f"Error: {result['error']}")

    sys.exit(0 if result["success"] else 1)

if __name__ == "__main__":
    main()
