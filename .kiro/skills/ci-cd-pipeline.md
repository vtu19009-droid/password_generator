---
name: "ci-cd-pipeline"
description: "Use when setting up CI/CD, GitHub Actions, automating builds, testing, or deploying Java applications. Triggers: 'setup CI/CD', 'GitHub Actions', 'automate build', 'continuous integration', 'deploy automation'."
version: "1.0.0"
category: "engineering"
tier: "standard"
inclusion: "manual"
requires: []
---

# CI/CD Pipeline

GitHub Actions setup for Java projects — build, test, package, and release automation.

---

## Table of Contents

- [Quick Start](#quick-start)
- [Minimal CI Pipeline](#minimal-ci-pipeline)
- [Release Pipeline](#release-pipeline)
- [Setup Steps](#setup-steps)
- [Common Pitfalls](#common-pitfalls)
- [Advanced Workflows](#advanced-workflows)

---

## Quick Start

```bash
# Create workflows directory
mkdir -p .github/workflows

# Add CI workflow
# (see Minimal CI Pipeline below)

# Commit and push
git add .github/workflows/
git commit -m "ci: add GitHub Actions workflow"
git push password_origin main

# Check Actions tab on GitHub
```

---

## Minimal CI Pipeline

Create `.github/workflows/ci.yml`:

```yaml
name: Build

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Java
        uses: actions/setup-java@v4
        with:
          java-version: '17'
          distribution: 'temurin'

      - name: Compile
        run: javac PasswordGenerator.java

      - name: Package JAR
        run: jar cfe PasswordGenerator.jar PasswordGenerator *.class

      - name: Upload JAR artifact
        uses: actions/upload-artifact@v4
        with:
          name: PasswordGenerator
          path: PasswordGenerator.jar
          retention-days: 30
```

**What this does:**
- Triggers on push to `main` or PR
- Compiles Java code
- Packages as JAR
- Uploads artifact (downloadable from Actions tab)

---

## Release Pipeline

Create `.github/workflows/release.yml`:

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
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Java
        uses: actions/setup-java@v4
        with:
          java-version: '17'
          distribution: 'temurin'

      - name: Compile
        run: javac PasswordGenerator.java

      - name: Package JAR
        run: jar cfe PasswordGenerator.jar PasswordGenerator *.class

      - name: Create GitHub Release
        uses: softprops/action-gh-release@v2
        with:
          files: PasswordGenerator.jar
          generate_release_notes: true
```

**How to trigger:**
```bash
git tag v1.0.0
git push password_origin v1.0.0
```

**What this does:**
- Triggers on version tags (v1.0.0, v2.1.3, etc.)
- Builds JAR
- Creates GitHub Release
- Attaches JAR to release
- Auto-generates release notes from commits

---

## Setup Steps

**Step 1: Create workflows directory**
```bash
mkdir -p .github/workflows
```

**Step 2: Add CI workflow**
```bash
# Copy ci.yml content from above
```

**Step 3: Commit and push**
```bash
git add .github/workflows/
git commit -m "ci: add GitHub Actions workflow"
git push password_origin main
```

**Step 4: Verify**
- Go to GitHub repository
- Click "Actions" tab
- See workflow run

**Step 5: Download artifact**
- Click on workflow run
- Scroll to "Artifacts" section
- Download `PasswordGenerator.jar`

---

## Common Pitfalls

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| **Wrong Java version** | Compilation fails | Pin version in `setup-java` step |
| **Missing permissions** | Release creation fails | Add `permissions: contents: write` |
| **Swing needs display** | UI tests fail | Add `DISPLAY` env or use headless mode |
| **.class files in repo** | Conflicts | Already handled by `.gitignore` |
| **Artifact too large** | Upload fails | Check file size, exclude unnecessary files |

---

## Advanced Workflows

See references/ci-cd-advanced.md for:
- Matrix builds (multiple Java versions)
- Caching dependencies
- Code coverage reporting
- Security scanning
- Multi-platform builds
```
