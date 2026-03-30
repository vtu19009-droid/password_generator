---
name: "code-reviewer"
description: Use this skill when the user asks to review, audit, or improve code quality. Covers code smells, security issues, SOLID violations, naming, and Java-specific antipatterns.
inclusion: manual
---

# Code Reviewer

Structured code review for Java — quality checks, security, antipatterns, and improvement guidance.

---

## Review Checklist

### Correctness
- [ ] Logic handles edge cases (empty input, null, min/max values)
- [ ] No off-by-one errors in loops
- [ ] Exception handling is present and meaningful
- [ ] Random generation uses `SecureRandom`, not `Random`

### Security
- [ ] No hardcoded secrets or credentials
- [ ] User input is validated before use
- [ ] Clipboard operations don't expose sensitive data unnecessarily
- [ ] No `System.out.println` leaking sensitive values

### Code Quality
- [ ] Methods are focused (single responsibility)
- [ ] No god classes (>20 methods)
- [ ] No functions >50 lines
- [ ] No magic numbers — use named constants
- [ ] Meaningful variable and method names

### UI / Swing Specific
- [ ] UI built on Event Dispatch Thread (`SwingUtilities.invokeLater`)
- [ ] Long operations not blocking the EDT
- [ ] Components properly disposed on close
- [ ] Fonts and colors defined as constants, not inline

---

## Common Java Antipatterns

| Antipattern | Problem | Fix |
|-------------|---------|-----|
| `new Random()` for passwords | Predictable output | Use `SecureRandom` |
| Magic numbers (`length < 8`) | Unclear intent | `private static final int WEAK_THRESHOLD = 8` |
| God class | Hard to maintain | Split into service + UI classes |
| Blocking EDT | UI freezes | Use `SwingWorker` for heavy tasks |
| Catching `Exception` broadly | Hides bugs | Catch specific exceptions |
| `public` fields | Breaks encapsulation | Use `private` + getters |

---

## Severity Levels

| Level | Examples |
|-------|---------|
| Critical | Hardcoded secrets, SQL injection, data exposure |
| High | `Random` instead of `SecureRandom`, no input validation |
| Medium | God class, methods >50 lines, magic numbers |
| Low | Naming issues, missing comments, unused imports |

---

## Review Verdict Guide

| Score | Verdict |
|-------|---------|
| No issues | Approve |
| Low issues only | Approve with suggestions |
| Medium issues | Request changes |
| High / Critical | Block — fix before merge |

---

## PasswordGenerator.java — Current State

- `SecureRandom` ✅
- Single class — could benefit from extracting `PasswordService`
- UI constants defined ✅
- EDT-safe via `SwingUtilities.invokeLater` ✅
- No input validation on spinner (handled by `SpinnerNumberModel` bounds) ✅
