---
name: "ci-cd"
description: Use this skill when the user asks to set up CI/CD, GitHub Actions, automate builds, or deploy the Java app.
inclusion: manual
---

# CI/CD Pipeline

GitHub Actions setup for the Java Password Generator.

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
      - uses: actions/checkout@v4

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
```

---

## Release Pipeline (on tag push)

```yaml
name: Release

on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-java@v4
        with:
          java-version: '17'
          distribution: 'temurin'

      - run: javac PasswordGenerator.java
      - run: jar cfe PasswordGenerator.jar PasswordGenerator *.class

      - name: Create GitHub Release
        uses: softprops/action-gh-release@v2
        with:
          files: PasswordGenerator.jar
```

---

## Setup Steps

1. Create `.github/workflows/` folder in repo
2. Add `ci.yml` from above
3. Push to `main` — Actions tab on GitHub shows the run
4. Download the JAR artifact from the Actions run

---

## Common Pitfalls

| Pitfall | Fix |
|---------|-----|
| Swing apps need display | Add `DISPLAY` env or use headless mode for tests |
| `.class` files in repo | Already handled by `.gitignore` |
| Wrong Java version | Pin version in `setup-java` step |
