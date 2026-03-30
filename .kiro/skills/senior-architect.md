---
name: "senior-architect"
description: "Use when designing system architecture, evaluating patterns, planning scalability, choosing tech stacks, or making technical decisions. Triggers: 'design architecture', 'choose tech stack', 'scalability planning', 'architecture review', 'technical decision'."
version: "1.0.0"
category: "engineering"
tier: "POWERFUL"
inclusion: "manual"
requires: []
---

# Senior Architect

Architecture decisions, tech stack evaluation, design patterns, and scalability planning for this project.

---

## Table of Contents

- [Quick Start](#quick-start)
- [Current Architecture](#current-architecture)
- [Architecture Decision Records](#architecture-decision-records)
- [When to Refactor](#when-to-refactor)
- [Architecture Pattern Decision](#architecture-pattern-decision)
- [Tech Stack Decision Guide](#tech-stack-decision-guide)
- [Scalability Considerations](#scalability-considerations)
- [Reference Documentation](#reference-documentation)

---

## Quick Start

```
1. Assess current architecture
2. Identify constraints (team size, timeline, budget)
3. Evaluate patterns against requirements
4. Document decision in ADR format
5. Plan migration path if needed
```

---

## Current Architecture

```
PasswordGenerator.java (Single Class)
├── UI Layer (Swing components)
│   ├── JFrame setup
│   ├── Component creation (buttons, fields, labels)
│   └── Event listeners
├── Business Logic
│   ├── generatePassword()
│   └── updateStrength()
└── Utility Methods
    └── makeButton()
```

**Pattern:** Monolithic single-class application  
**Rationale:** Appropriate for standalone desktop tool with <300 lines  
**Trade-offs:** Simple to understand, but harder to test and extend

---

## Architecture Decision Records

### ADR-001: Single-File Swing over JavaFX

**Status:** Accepted  
**Date:** 2026-03-30

**Context:**
- Need simple password generator desktop app
- No external dependencies desired
- Target Java 8+ compatibility
- Solo developer, 1-week timeline

**Decision:**
Use Swing in a single `.java` file, no build tool.

**Rationale:**
- Swing ships with JDK — zero setup
- Single file = easy distribution
- Sufficient for utility tool UI
- Team already knows Swing

**Consequences:**
- ✅ Fast development
- ✅ No dependency management
- ✅ Works on any Java 8+ system
- ❌ Less modern look than JavaFX
- ❌ No CSS-like styling
- ❌ Harder to test (UI tightly coupled)

**Alternatives Considered:**
| Option | Pros | Cons | Verdict |
|--------|------|------|---------|
| JavaFX | Modern look, CSS support | Requires separate download on some JDKs | Rejected — added complexity |
| Electron | Web tech, cross-platform | 100MB+ bundle size | Rejected — overkill |
| Web app | Accessible anywhere | Requires server | Rejected — not needed |

---

### ADR-002: SecureRandom over Random

**Status:** Accepted  
**Date:** 2026-03-30

**Context:**
- Generating passwords for user security
- Need unpredictable output
- Performance not critical (generates 1 password at a time)

**Decision:**
Use `java.security.SecureRandom` for password generation.

**Rationale:**
- Cryptographically strong random number generator
- Uses OS entropy sources (not predictable seed)
- Same API as `Random` — easy to use
- Slight performance overhead acceptable for this use case

**Consequences:**
- ✅ Secure password generation
- ✅ No predictability attacks
- ❌ Slightly slower initialization (~100ms first call)
- ❌ Not suitable for high-throughput scenarios (not relevant here)

**Alternatives Considered:**
| Option | Pros | Cons | Verdict |
|--------|------|------|---------|
| `Random` | Fast | Predictable if seed known | Rejected — security risk |
| `ThreadLocalRandom` | Fast, thread-safe | Not cryptographically secure | Rejected — security risk |
| External library | More features | Dependency | Rejected — unnecessary |

---

### ADR-003: No Build Tool (Manual javac)

**Status:** Accepted  
**Date:** 2026-03-30

**Context:**
- Single-file project
- No external dependencies
- Target audience: developers who can run `javac`

**Decision:**
Use manual `javac` compilation, no Maven/Gradle.

**Rationale:**
- Zero configuration
- No build file to maintain
- Compilation is one command
- Distribution is one `.jar` file

**Consequences:**
- ✅ Simplest possible build process
- ✅ No build tool learning curve
- ❌ No dependency management (not needed)
- ❌ No automated testing framework integration
- ❌ Manual version management

**When to Revisit:**
- Adding external dependencies
- Adding unit tests
- Multi-module project
- Team of 2+ developers

---

## When to Refactor

### Refactor Triggers

Current single-class structure is appropriate. Refactor when:

| Trigger | Threshold | Suggested Pattern |
|---------|-----------|-------------------|
| **File size** | >500 lines | Split into UI + Service classes |
| **Feature count** | >5 distinct features | Extract feature modules |
| **Persistence needed** | Adding database/file storage | Introduce Repository pattern |
| **Multiple screens** | >1 window/dialog | MVC or MVP pattern |
| **Network calls** | API integration | Layered architecture |
| **Team size** | 2+ developers | Modular monolith |
| **Testing required** | Unit test coverage needed | Dependency injection |

### Suggested Refactoring (if needed)

```
Before (current):
PasswordGenerator.java (300 lines)

After (if triggers met):
├── Main.java (entry point)
├── ui/
│   ├── PasswordGeneratorUI.java (Swing components)
│   └── UIConstants.java (colors, fonts)
├── service/
│   ├── PasswordService.java (generation logic)
│   └── StrengthAssessor.java (strength calculation)
└── model/
    └── Password.java (data class)
```

**Migration Path:**
1. Extract `PasswordService` with generation logic
2. Extract `UIConstants` for colors/fonts
3. Refactor `PasswordGenerator` to use service
4. Add tests for `PasswordService`
5. Extract additional services as needed

---

## Architecture Pattern Decision

### Pattern Decision Matrix

| Pattern | Team Size | Complexity | Testability | When to Use |
|---------|-----------|------------|-------------|-------------|
| **Single Class** (current) | 1 | Low | Low | <300 lines, solo dev, utility tool |
| **Modular Monolith** | 1-5 | Medium | High | Multiple features, needs testing |
| **MVC** | 2-10 | Medium | High | Multiple views, clear separation |
| **Layered** | 3-15 | High | High | Persistence + business logic + UI |
| **Microservices** | 10+ | Very High | High | Never for desktop app |

### Pattern Evaluation for This Project

**Current State:**
- Team: 1 developer
- Lines of code: ~250
- Features: 1 (password generation)
- Persistence: None
- Network: None

**Recommendation:** ✅ **Single Class** (current pattern is correct)

**When to Upgrade:**
- To **Modular Monolith**: When adding 2+ features (history, breach checking, etc.)
- To **MVC**: When adding multiple windows/dialogs
- To **Layered**: When adding database persistence

---

## Tech Stack Decision Guide

### UI Framework Decision

| Framework | Pros | Cons | Use When |
|-----------|------|------|----------|
| **Swing** (current) | Ships with JDK, mature, stable | Dated look, verbose | Utility tools, internal apps |
| **JavaFX** | Modern look, CSS styling, FXML | Separate download on some JDKs | Customer-facing apps |
| **SWT** | Native widgets, fast | Platform-specific JARs | Eclipse plugins |
| **Web (Spring Boot)** | Accessible anywhere, modern | Requires server, overkill | Multi-user apps |

**Decision for this project:** ✅ **Swing** — appropriate for standalone utility.

### Packaging Decision

| Method | Pros | Cons | Use When |
|--------|------|------|----------|
| **Raw .class files** | Simplest | Requires Java installed, multiple files | Development only |
| **Executable JAR** (current) | Single file, portable | Requires Java installed | Distribution to developers |
| **jpackage** | Native installer, bundles JRE | Large size (50MB+), Java 14+ | End-user distribution |
| **GraalVM Native Image** | Fast startup, small size | Complex build, limited reflection | Performance-critical CLI tools |

**Decision for this project:** ✅ **Executable JAR** — best balance for developer audience.

### Persistence Decision (if needed)

| Option | Pros | Cons | Use When |
|--------|------|------|----------|
| **java.util.prefs** | Built-in, cross-platform | Limited to key-value | Simple settings |
| **Flat file (JSON/CSV)** | Human-readable, simple | No querying, manual parsing | Small datasets |
| **SQLite (JDBC)** | SQL queries, relational | Requires JDBC driver | Structured data |
| **H2 Database** | Pure Java, embedded | Larger than SQLite | Complex queries |

**Recommendation:** If adding password history, use **flat file (JSON)** for simplicity.

---

## Scalability Considerations

### This is a Local Desktop App

Scalability is **not a concern** for this project. Focus instead on:

1. **Maintainability** — clean code, clear separation of concerns
2. **Portability** — runs on Windows, macOS, Linux
3. **Usability** — responsive UI, clear feedback
4. **Security** — secure password generation

### If This Were a Web App

Hypothetical scalability considerations:

| Concern | Solution |
|---------|----------|
| Concurrent users | Stateless API, horizontal scaling |
| Password storage | Encrypted at rest, hashed with bcrypt |
| Rate limiting | Token bucket per IP |
| Availability | Load balancer + multiple instances |

**But:** This is a desktop app — none of this applies.

---

## Reference Documentation

| File | Contains | Use When |
|------|----------|----------|
| `references/architecture-patterns.md` | 9 patterns with trade-offs | Choosing architecture |
| `references/adr-template.md` | ADR format and examples | Documenting decisions |
| `references/refactoring-guide.md` | Step-by-step refactoring | Restructuring code |

---

## Decision Framework

### Step-by-Step Architecture Decision Process

**Step 1: Define Constraints**
- Team size: [X developers]
- Timeline: [X weeks]
- Budget: [$X]
- Scale: [X users]

**Step 2: List Requirements**
- Functional: [what it must do]
- Non-functional: [performance, security, etc.]

**Step 3: Evaluate Options**
- List 2-3 candidate architectures
- Score each against requirements
- Document trade-offs

**Step 4: Make Decision**
- Choose one option
- Document in ADR format
- Plan migration path if changing

**Step 5: Validate**
- Build proof-of-concept
- Measure against requirements
- Iterate if needed

---

## Quick Reference

```
Current: Single-class Swing app
Appropriate for: Utility tools, <300 lines, solo dev
Refactor when: >500 lines, 2+ features, testing needed
Next step: Extract PasswordService if adding features
```
