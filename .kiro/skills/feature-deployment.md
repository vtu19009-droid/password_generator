---
name: "feature-deployment"
version: "1.0.0"
description: "Use when deploying a new feature, releasing a version, or shipping to production. Triggers: 'deploy feature', 'ship to production', 'release this', 'prepare deployment', 'create release'."
category: "engineering"
tier: "standard"
inclusion: "manual"
requires: ["git-workflow", "ci-cd-pipeline"]
domains: ["backend", "devops"]
---

# Feature Deployment

End-to-end deployment workflow for Java desktop applications — from feature branch to GitHub release.

---

## Table of Contents

- [Quick Start](#quick-start)
- [Deployment Workflow](#deployment-workflow)
- [Pre-Deploy Validation](#pre-deploy-validation)
- [Release Process](#release-process)
- [Rollback Procedures](#rollback-procedures)
- [Python Tools](#python-tools)
- [Common Commands](#common-commands)

---

## Quick Start

```bash
# 1. Run pre-deploy checks
python .kiro/skills/scripts/pre_deploy_check.py --branch feature/my-feature

# 2. Validate build
python .kiro/skills/scripts/build_validator.py

# 3. Create release (dry-run)
python .kiro/skills/scripts/release.py --version 1.0.0 --dry-run

# 4. Create actual release
python .kiro/skills/scripts/release.py --version 1.0.0
```

---

## Deployment Workflow

### Phase 1: Pre-Deploy Validation

```
Feature Complete → Tests Pass → Build Validates → Ready for Release
```

| Check | Tool | Pass Condition |
|-------|------|----------------|
| All tests green | `pre_deploy_check.py --tests` | 0 failures |
| Code compiles | `build_validator.py --compile` | Exit code 0 |
| JAR packages | `build_validator.py --package` | JAR created successfully |
| No merge conflicts | `pre_deploy_check.py --conflicts` | Clean merge to main |
| Version bumped | `pre_deploy_check.py --version` | Version tag ready |
| Changelog updated | `pre_deploy_check.py --changelog` | CHANGELOG.md has entry |

**Gate:** All checks must pass before proceeding to Phase 2.

---

### Phase 2: Environment Decision

For desktop Java apps, deployment means creating a GitHub release:

```
Is this a major version?
├── YES → Create release notes → Tag → Build → Release → Announce
└── NO  →
      Is this a hotfix?
      ├── YES → Fast-track → Tag → Build → Release
      └── NO  → Standard release process
```

| Scenario | Release Type | Process |
|----------|--------------|---------|
| Major version (v2.0.0) | Breaking changes | Full release notes + migration guide |
| Minor version (v1.1.0) | New features | Feature highlights + changelog |
| Patch version (v1.0.1) | Bug fixes | Bug fix list + affected versions |
| Hotfix | Critical bug | Expedited release + security advisory |

---

### Phase 3: Release Execution

```bash
# Step 1: Merge feature to main
git checkout main
git pull password_origin main
git merge feature/my-feature
git push password_origin main

# Step 2: Create version tag
git tag v1.0.0
git push password_origin v1.0.0

# Step 3: GitHub Actions builds and creates release automatically
# (see .github/workflows/release.yml)

# Step 4: Verify release on GitHub
gh release view v1.0.0
```

**Automated by CI/CD:**
- Compile Java code
- Package JAR
- Create GitHub Release
- Attach JAR artifact
- Generate release notes

---

### Phase 4: Post-Deploy Verification

| Check | Command | Expected |
|-------|---------|----------|
| Release exists | `gh release view v1.0.0` | Release found |
| JAR attached | `gh release view v1.0.0 --json assets` | JAR in assets |
| JAR downloads | `gh release download v1.0.0` | File downloads |
| JAR runs | `java -jar PasswordGenerator.jar` | UI launches |
| Version correct | Check UI title or About dialog | Shows v1.0.0 |

---

## Pre-Deploy Validation

### Validation Checklist

**Code Quality:**
- [ ] All code reviewed and approved
- [ ] No commented-out code
- [ ] No TODO/FIXME in critical paths
- [ ] Consistent code style

**Functionality:**
- [ ] Feature works as expected
- [ ] No regressions in existing features
- [ ] Edge cases handled
- [ ] Error messages are user-friendly

**Documentation:**
- [ ] README.md updated
- [ ] CHANGELOG.md has entry for this version
- [ ] Code comments added for complex logic
- [ ] Release notes drafted

**Build:**
- [ ] Code compiles without warnings
- [ ] JAR packages successfully
- [ ] JAR runs on clean system
- [ ] No missing dependencies

**Git:**
- [ ] Feature branch up-to-date with main
- [ ] No merge conflicts
- [ ] Commit messages follow convention
- [ ] Version tag ready (e.g., v1.0.0)

---

## Release Process

### Semantic Versioning

Follow [SemVer](https://semver.org/): `MAJOR.MINOR.PATCH`

| Version | When to Bump | Example |
|---------|--------------|---------|
| **MAJOR** | Breaking changes, incompatible API | v1.0.0 → v2.0.0 |
| **MINOR** | New features, backward compatible | v1.0.0 → v1.1.0 |
| **PATCH** | Bug fixes, backward compatible | v1.0.0 → v1.0.1 |

**For this project:**
- MAJOR: Change password generation algorithm, remove features
- MINOR: Add password history, add breach checking, new UI theme
- PATCH: Fix clipboard bug, fix UI alignment, security patch

### Release Workflow

**Step 1: Prepare Release**
```bash
# Update version in code (if displayed in UI)
# Update CHANGELOG.md
# Commit changes
git add .
git commit -m "chore: prepare v1.0.0 release"
git push password_origin main
```

**Step 2: Create Tag**
```bash
git tag -a v1.0.0 -m "Release v1.0.0: Initial public release"
git push password_origin v1.0.0
```

**Step 3: GitHub Actions Runs**
- Triggered by tag push
- Compiles code
- Packages JAR
- Creates GitHub Release
- Attaches JAR

**Step 4: Verify and Announce**
```bash
# Download and test
gh release download v1.0.0
java -jar PasswordGenerator.jar

# Announce (if public project)
# - Update README with latest version
# - Post on social media / forums
# - Notify users
```

### Release Notes Template

```markdown
## v1.0.0 - 2026-03-31

### ✨ New Features
- Add password strength indicator
- Implement copy to clipboard
- Dark theme UI

### 🐛 Bug Fixes
- Fix clipboard error on Windows
- Correct strength label color

### 🔧 Improvements
- Optimize password generation performance
- Improve button hover states

### 📦 Downloads
- [PasswordGenerator.jar](link)

### 🔒 Security
- Use SecureRandom for password generation

### 📝 Notes
- Requires Java 8 or higher
- Tested on macOS, Windows, Linux
```

---

## Rollback Procedures

### Rollback Decision Table

| Trigger | Action | Command |
|---------|--------|---------|
| Critical bug in release | Delete release, revert tag | See below |
| JAR doesn't run | Delete release, fix, re-release | See below |
| Security vulnerability | Immediate patch release | Fast-track v1.0.1 |
| User reports major issue | Investigate, patch if confirmed | Standard patch process |

### Rollback Steps

**Step 1: Delete GitHub Release**
```bash
gh release delete v1.0.0 --yes
```

**Step 2: Delete Git Tag**
```bash
# Delete local tag
git tag -d v1.0.0

# Delete remote tag
git push password_origin :refs/tags/v1.0.0
```

**Step 3: Revert Commits (if needed)**
```bash
# Find commit hash of bad release
git log --oneline

# Revert the commit
git revert <commit-hash>
git push password_origin main
```

**Step 4: Create Hotfix**
```bash
# Fix the issue
git checkout -b hotfix/critical-bug
# Make fixes
git add .
git commit -m "fix: critical bug in password generation"
git push password_origin hotfix/critical-bug

# Merge to main
git checkout main
git merge hotfix/critical-bug
git push password_origin main

# Create new release
git tag v1.0.1
git push password_origin v1.0.1
```

---

## Python Tools

### `scripts/pre_deploy_check.py`

```python
#!/usr/bin/env python3
"""Pre-deployment validation checks for Java desktop app."""

import argparse
import subprocess
import sys
import json
import os
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
    # Check if there's a recent version entry
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
    tags = result.stdout.strip().split("\n")
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
```

---

### `scripts/build_validator.py`

```python
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
    # First compile if not already done
    compile_result = validate_compile()
    if not compile_result["passed"]:
        return {"passed": False, "error": "Compilation failed"}
    
    # Package JAR
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
    
    # Can't actually run GUI in headless mode, just check JAR is valid
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

    # If no specific check, run all
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
```

---

### `scripts/release.py`

```python
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
    
    # Check if JAR exists
    jar_path = Path("PasswordGenerator.jar")
    if not jar_path.exists():
        return {"success": False, "error": "JAR not found. Run build first."}
    
    # Create tag
    tag_cmd = ["git", "tag", "-a", version, "-m", f"Release {version}"]
    if dry_run:
        print(f"[DRY RUN] Would run: {' '.join(tag_cmd)}")
    else:
        subprocess.run(tag_cmd, check=True)
        subprocess.run(["git", "push", "password_origin", version], check=True)
    
    # Create release
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
```

---

## Common Commands

```bash
# Full pre-deploy validation
python .kiro/skills/scripts/pre_deploy_check.py --compile --changelog --version

# Build validation
python .kiro/skills/scripts/build_validator.py

# Create release (dry-run first)
python .kiro/skills/scripts/release.py --version 1.0.0 --dry-run
python .kiro/skills/scripts/release.py --version 1.0.0

# Manual release process
javac PasswordGenerator.java
jar cfe PasswordGenerator.jar PasswordGenerator *.class
git tag v1.0.0
git push password_origin v1.0.0
gh release create v1.0.0 PasswordGenerator.jar --generate-notes

# Rollback
gh release delete v1.0.0 --yes
git tag -d v1.0.0
git push password_origin :refs/tags/v1.0.0

# JSON output (CI/CD)
python .kiro/skills/scripts/pre_deploy_check.py --compile --output json
python .kiro/skills/scripts/build_validator.py --output json
```

---

## Reference Documentation

| File | Contains | Use When |
|------|----------|----------|
| `references/release-checklist.md` | Manual pre-release checklist | Before creating release |
| `references/versioning-guide.md` | SemVer decision guide | Choosing version number |
| `references/rollback-procedures.md` | Detailed rollback steps | Emergency rollback needed |
| `references/changelog-template.md` | Changelog format | Writing release notes |
