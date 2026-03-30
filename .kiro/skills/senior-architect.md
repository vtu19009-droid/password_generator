---
name: "senior-architect"
description: Use this skill when the user asks to design system architecture, evaluate patterns, plan scalability, choose a tech stack, or make technical decisions for this project.
inclusion: manual
---

# Senior Architect

Architecture decisions, tech stack evaluation, and design patterns for this project.

---

## Current Architecture

```
PasswordGenerator.java
└── Single class (JFrame)
    ├── UI layer (Swing components)
    ├── Business logic (generatePassword, updateStrength)
    └── Utility (makeButton helper)
```

Simple and appropriate for a standalone desktop tool. No over-engineering needed.

---

## When to Refactor

Refactor the single class into multiple when:
- [ ] Adding persistent storage (password history)
- [ ] Adding multiple screens / views
- [ ] Adding network calls (e.g. breach checking via API)
- [ ] Team of 2+ developers working on it

### Suggested split (if needed)
```
PasswordService.java       — generation logic, strength scoring
PasswordGeneratorUI.java   — all Swing components
AppConfig.java             — constants (colors, fonts, char sets)
Main.java                  — entry point
```

---

## Architecture Pattern Decision

| Pattern | When to use |
|---------|-------------|
| Single class (current) | Solo tool, <300 lines, no persistence |
| MVC | Multiple views, testable logic needed |
| Layered | Persistence + business logic + UI separation |
| Microservices | Never — overkill for a desktop password tool |

---

## Tech Stack Decision Guide

| Need | Option A | Option B |
|------|----------|----------|
| Desktop UI | Swing (current, no deps) | JavaFX (modern, CSS support) |
| Packaging | Raw `.class` files | Executable JAR / `jpackage` installer |
| Persistence | `java.util.prefs` / flat file | SQLite via JDBC |
| Testing | JUnit 5 | TestNG |
| Build tool | Manual `javac` (current) | Maven / Gradle |

---

## Scalability Considerations

This is a local desktop app — scalability is not a concern. Focus instead on:
- Maintainability (clean separation of concerns)
- Portability (Java 8+ compatibility)
- Packaging (JAR for easy distribution)

---

## ADR — Architecture Decision Record

### ADR-001: Single-file Swing over JavaFX
- Context: Simple password generator, no external deps desired
- Decision: Swing, single `.java` file
- Rationale: Zero setup, ships with JDK, sufficient for the use case
- Trade-off: Less modern look vs JavaFX, but acceptable for a utility tool

### ADR-002: SecureRandom over Random
- Context: Password generation requires unpredictability
- Decision: `java.security.SecureRandom`
- Rationale: Cryptographically strong, same API as `Random`
- Trade-off: Slightly slower initialization — negligible for this use case
