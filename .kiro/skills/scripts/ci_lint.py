#!/usr/bin/env python3
"""Validate GitHub Actions workflow YAML structure."""

import argparse
import sys
import json
import os

REQUIRED_KEYS = ["name", "on", "jobs"]
REQUIRED_JOB_KEYS = ["runs-on", "steps"]

def lint_workflow(path: str) -> list:
    issues = []
    
    if not os.path.exists(path):
        return [{"level": "error", "msg": f"File not found: {path}"}]
    
    try:
        import importlib.util
        if importlib.util.find_spec("yaml") is None:
            # Fallback: basic text checks without pyyaml
            with open(path) as f:
                content = f.read()
            for key in REQUIRED_KEYS:
                if key + ":" not in content:
                    issues.append({"level": "error", "msg": f"Missing top-level key: '{key}'"})
            return issues
        
        import yaml
        with open(path) as f:
            doc = yaml.safe_load(f)
        
        for key in REQUIRED_KEYS:
            if key not in doc:
                issues.append({"level": "error", "msg": f"Missing top-level key: '{key}'"})
        
        for job_name, job in (doc.get("jobs") or {}).items():
            for jk in REQUIRED_JOB_KEYS:
                if jk not in job:
                    issues.append({"level": "warn", "msg": f"Job '{job_name}' missing '{jk}'"})
    
    except Exception as e:
        issues.append({"level": "error", "msg": str(e)})
    
    return issues

def main():
    parser = argparse.ArgumentParser(description="Lint GitHub Actions workflow")
    parser.add_argument("--workflow", required=True, help="Path to workflow YAML")
    parser.add_argument("--output", choices=["text", "json"], default="text")
    parser.add_argument("--strict", action="store_true", help="Treat warnings as errors")
    args = parser.parse_args()

    issues = lint_workflow(args.workflow)

    if args.output == "json":
        print(json.dumps(issues, indent=2))
    else:
        if not issues:
            print("✓ Workflow looks valid")
        for i in issues:
            icon = "✗" if i["level"] == "error" else "⚠"
            print(f"{icon} [{i['level'].upper()}] {i['msg']}")

    errors = [i for i in issues if i["level"] == "error"]
    warns = [i for i in issues if i["level"] == "warn"]
    sys.exit(1 if errors or (args.strict and warns) else 0)

if __name__ == "__main__":
    main()
