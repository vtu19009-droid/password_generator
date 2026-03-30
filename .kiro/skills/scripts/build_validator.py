#!/usr/bin/env python3
"""Validate Java build and JAR packaging."""

import argparse
import subprocess
import sys
import json
from pathlib import Path

def validate_compile():
    """Compile Java code."""
    result = subprocess.run(
        ["javac", "-g:none", "PasswordGenerator.java"],
        capture_output=True,
        text=True
    )
    return {
        "passed": result.returncode == 0,
        "output": result.stderr or "Compiled successfully"
    }

def validate_package():
    """Package as JAR."""
    compile_result = validate_compile()
    if not compile_result["passed"]:
        return {"passed": False, "error": "Compilation failed"}
    
    result = subprocess.run(
        ["jar", "cfe", "PasswordGenerator.jar", "PasswordGenerator", "PasswordGenerator.class"],
        capture_output=True,
        text=True
    )
    
    jar_exists = Path("PasswordGenerator.jar").exists()
    return {
        "passed": result.returncode == 0 and jar_exists,
        "jar_created": jar_exists
    }

def validate_run():
    """Test if JAR runs (headless check)."""
    if not Path("PasswordGenerator.jar").exists():
        return {"passed": False, "error": "JAR not found"}
    
    result = subprocess.run(
        ["jar", "tf", "PasswordGenerator.jar"],
        capture_output=True,
        text=True
    )
    
    has_main = "PasswordGenerator.class" in result.stdout
    return {
        "passed": result.returncode == 0 and has_main,
        "has_main_class": has_main
    }

def main():
    parser = argparse.ArgumentParser(description="Build validation")
    parser.add_argument("--compile", action="store_true")
    parser.add_argument("--package", action="store_true")
    parser.add_argument("--run", action="store_true")
    parser.add_argument("--output", choices=["text", "json"], default="text")
    args = parser.parse_args()

    if not (args.compile or args.package or args.run):
        args.compile = args.package = args.run = True

    results = {}
    
    if args.compile:
        results["compile"] = validate_compile()
    if args.package:
        results["package"] = validate_package()
    if args.run:
        results["run"] = validate_run()

    if args.output == "json":
        print(json.dumps(results, indent=2))
    else:
        for k, v in results.items():
            status = "✓" if v["passed"] else "✗"
            print(f"{status} {k}")

    failed = [k for k, v in results.items() if not v.get("passed")]
    sys.exit(1 if failed else 0)

if __name__ == "__main__":
    main()
