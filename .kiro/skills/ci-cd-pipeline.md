---
name: "ci-cd-pipeline"
version: "1.1.0"
description: |
  Use when setting up CI/CD, GitHub Actions, automating builds, testing,
  or deploying applications. Trigger phrases: "setup CI/CD", "GitHub Actions",
  "automate build", "continuous integration", "deploy automation",
  "pipeline broken", "add tests to CI", "automate releases".
domains: ["backend", "frontend", "devops"]
category: "engineering"
tier: "standard"
inclusion: "manual"
requires: []
---

# CI/CD Pipeline

GitHub Actions setup for full-stack projects — build, test, lint, package, release, and post-deploy verification.

---

## Table of Contents

- [Quick Start](#quick-start)
- [Pipeline Strategy Decision](#pipeline-strategy-decision)
- [Workflow Templates](#workflow-templates)
- [Python Tools](#python-tools)
- [Common Pitfalls](#common-pitfalls)
- [Rollback & Failure Handling](#rollback--failure-handling)
- [Common Commands](#common-commands)
- [References](#references)

---

## Quick Start

```bash
# Validate existing pipeline config
python .kiro/skills/scripts/ci_lint.py --workflow .github/workflows/ci.yml

# Scaffold new workflow
python .kiro/skills/scripts/ci_scaffold.py --stack node --trigger push --env staging

# Check pipeline health after push
python .kiro/skills/scripts/ci_status.py --repo owner/repo --branch main

# Dry run before committing
python .kiro/skills/scripts/ci_scaffold.py --stack java --dry-run
```

---

## Pipeline Strategy Decision

### Trigger Selection

| Trigger | Use When |
|---|---|
| `push: branches: [main]` | Validate every commit to main |
| `pull_request: branches: [main]` | Gate merges with checks |
| `push: tags: [v*]` | Release on version tag |
| `workflow_dispatch` | Manual deploy (with inputs) |
| `schedule: cron` | Nightly builds / dependency audits |

### Stack-to-Workflow Matrix

| Stack | Build Tool | Recommended Template |
|---|---|---|
| Java | `javac` / Maven / Gradle | `ci-java.yml` |
| Node.js | `npm` / `pnpm` / `yarn` | `ci-node.yml` |
| Python | `pip` / `poetry` | `ci-python.yml` |
| Docker | `docker build` | `ci-docker.yml` |
| Full-stack | Monorepo | `ci-monorepo.yml` |

### Pipeline Complexity Decision

```
Is this a new project?
├── YES → Start with Minimal CI (build + test only)
└── NO  →
      Does it have a release process?
      ├── YES → Add Release Pipeline
      └── NO  →
            Does it deploy to an environment?
            ├── YES → Add Deploy Pipeline + smoke tests
            └── NO  → Minimal CI is sufficient
```

---

## Workflow Templates

### 1. Minimal CI (All Stacks)

`.github/workflows/ci.yml`:

```yaml
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
      
      - name: Set up runtime
        # Java:   uses: actions/setup-java@v4 / with: java-version: '17', distribution: 'temurin'
        # Node:   uses: actions/setup-node@v4 / with: node-version: '20'
        # Python: uses: actions/setup-python@v5 / with: python-version: '3.12'
        uses: actions/setup-node@v4
        with:
          node-version: '20'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Lint
        run: npm run lint
      
      - name: Test
        run: npm test
      
      - name: Build
        run: npm run build
      
      - name: Upload artifact
        uses: actions/upload-artifact@v4
        with:
          name: build-output
          path: dist/
          retention-days: 30
```

---

### 2. Release Pipeline

`.github/workflows/release.yml`:

```yaml
name: Release

on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    
    steps:
      - uses: actions/checkout@v4
      
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      
      - run: npm ci
      - run: npm run build
      
      - name: Create GitHub Release
        uses: softprops/action-gh-release@v2
        with:
          files: dist/**
          generate_release_notes: true
```

**Trigger:**
```bash
git tag v1.0.0
git push origin v1.0.0
```

---

### 3. Deploy Pipeline (with Smoke Test)

`.github/workflows/deploy.yml`:

```yaml
name: Deploy

on:
  workflow_dispatch:
    inputs:
      environment:
        description: 'Target environment'
        required: true
        default: 'staging'
        type: choice
        options: [staging, production]

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: ${{ github.event.inputs.environment }}
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Deploy
        run: ./infra/deploy.sh --env ${{ github.event.inputs.environment }}
        env:
          DEPLOY_TOKEN: ${{ secrets.DEPLOY_TOKEN }}
      
      - name: Smoke test
        run: python scripts/smoke_test.py --env ${{ github.event.inputs.environment }} --health --latency
      
      - name: Notify on failure
        if: failure()
        run: python scripts/ci_status.py --notify --status failed --env ${{ github.event.inputs.environment }}
```

---

## Python Tools

### `scripts/ci_lint.py`

```python
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
```

---

### `scripts/ci_scaffold.py`

```python
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
```

---

### `scripts/ci_status.py`

```python
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
```

---

## Common Pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| Wrong runtime version | Compilation fails | Pin version explicitly in setup step |
| Missing `permissions` | Release creation fails | Add `permissions: contents: write` |
| UI/Swing tests need display | Tests hang or crash | Add `DISPLAY: :99` or use headless mode |
| Hardcoded remote name | Push fails on CI | Always use `origin`, not custom names |
| Large artifact upload | Upload timeout | Exclude `node_modules/`, `.git/`, build cache |
| Secrets not set | Deploy step fails | Add secrets in repo Settings → Secrets |
| `npm install` vs `npm ci` | Non-deterministic builds | Always use `npm ci` in CI pipelines |

---

## Rollback & Failure Handling

### Failure Decision Table

| Failure Type | Severity | Action |
|---|---|---|
| Lint failure | 🟡 Warn | Fix code, re-push |
| Test failure | 🔴 Block | Do not merge/deploy |
| Build failure | 🔴 Block | Do not deploy |
| Deploy failure | 🔴 Critical | Auto-rollback or manual |
| Smoke test failure | 🔴 Critical | Rollback immediately |
| Flaky test | 🟡 Warn | Re-run job; track pattern |

### Rollback Steps

```bash
# 1. Identify last good release tag
git tag --sort=-creatordate | head -5

# 2. Revert to last good tag
git checkout v<last-good>

# 3. Re-deploy
python scripts/deploy.py --env production --feature v<last-good>

# 4. Verify
python scripts/smoke_test.py --env production --health --latency
```

---

## Common Commands

```bash
# Scaffold new CI workflow (dry run)
python .kiro/skills/scripts/ci_scaffold.py --stack node --dry-run

# Scaffold and write
python .kiro/skills/scripts/ci_scaffold.py --stack java --out .github/workflows/ci.yml

# Lint workflow before pushing
python .kiro/skills/scripts/ci_lint.py --workflow .github/workflows/ci.yml --strict

# Check latest CI status
GITHUB_TOKEN=<token> python .kiro/skills/scripts/ci_status.py --repo owner/repo --branch main

# JSON output for CI dashboards
python .kiro/skills/scripts/ci_status.py --repo owner/repo --output json
```

---

## References

- `references/ci-cd-advanced.md` — matrix builds, caching, coverage, security scanning
- `references/github-actions-secrets.md` — secrets management patterns
- `references/ci-cd-checklist.md` — pre-merge CI validation checklist
- `references/feature-deployment-checklist.md` — integrates with `feature-deployment` skill
