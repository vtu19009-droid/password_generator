---
name: "code-reviewer"
description: "Use when reviewing, auditing, or improving code quality. Covers code smells, security issues, SOLID violations, naming conventions, and Java-specific antipatterns. Triggers: 'review code', 'code quality check', 'find bugs', 'security audit', 'refactor suggestions'."
version: "1.0.0"
category: "engineering"
tier: "standard"
inclusion: "manual"
requires: []
---

# Code Reviewer

Structured code review for Java — quality checks, security, antipatterns, and improvement guidance.

---

## Table of Contents

- [Quick Start](#quick-start)
- [Review Workflows](#review-workflows)
- [Review Checklist](#review-checklist)
- [Severity Levels](#severity-levels)
- [Common Java Antipatterns](#common-java-antipatterns)
- [Security Patterns](#security-patterns)
- [Code Quality Metrics](#code-quality-metrics)
- [Review Verdict Guide](#review-verdict-guide)
- [This Project Assessment](#this-project-assessment)

---

## Quick Start

```bash
# Run automated checks (if available)
javac -Xlint:all PasswordGenerator.java

# Manual review checklist
# 1. Read through code top-to-bottom
# 2. Check against security checklist
# 3. Identify code smells
# 4. Assess SOLID compliance
# 5. Generate verdict and recommendations
```

---

## Review Workflows

### Workflow 1: Pre-Commit Review

```
Self-Review → Checklist → Fix → Commit
```

**Step 1: Self-review**
- Read your own code as if someone else wrote it
- Check for obvious issues

**Step 2: Run checklist**
- Use [Review Checklist](#review-checklist) below
- Mark each item pass/fail

**Step 3: Fix issues**
- Address all Critical and High severity items
- Document why Medium/Low items are deferred

**Step 4: Commit**
```bash
git add .
git commit -m "feat: add feature X (reviewed)"
```

### Workflow 2: Pull Request Review

```
Read → Analyze → Test → Comment → Verdict
```

**Step 1: Read the diff**
```bash
git diff main..feature-branch
```

**Step 2: Analyze against checklist**
- Run through [Review Checklist](#review-checklist)
- Note issues with line numbers

**Step 3: Test locally**
```bash
git checkout feature-branch
javac PasswordGenerator.java
java PasswordGenerator
# Test the feature manually
```

**Step 4: Comment on PR**
- Group comments by severity
- Provide specific fixes, not vague advice

**Step 5: Verdict**
- ✅ Approve
- 💬 Approve with suggestions
- ❌ Request changes
- 🚫 Block (critical issues)

### Workflow 3: Codebase Audit

```
Scan → Categorize → Prioritize → Report
```

**Step 1: Scan all files**
```bash
find . -name "*.java" -exec javac -Xlint:all {} \;
```

**Step 2: Categorize issues**
- Security
- Performance
- Maintainability
- Style

**Step 3: Prioritize**
- Critical → High → Medium → Low

**Step 4: Generate report**
- See [references/audit-report-template.md](references/audit-report-template.md)

---

## Review Checklist

### Correctness

- [ ] Logic handles edge cases (empty input, null, min/max values)
- [ ] No off-by-one errors in loops
- [ ] Exception handling is present and meaningful
- [ ] No silent failures (catch without logging)
- [ ] Return values are checked where necessary

### Security

- [ ] No hardcoded secrets or credentials
- [ ] User input is validated before use
- [ ] Sensitive data not logged or exposed
- [ ] `SecureRandom` used instead of `Random` for security-sensitive operations
- [ ] No SQL injection vulnerabilities (if database access exists)
- [ ] No command injection (if executing shell commands)
- [ ] Clipboard operations don't expose sensitive data unnecessarily

### Code Quality

- [ ] Methods are focused (single responsibility)
- [ ] No god classes (>20 methods)
- [ ] No functions >50 lines
- [ ] No magic numbers — use named constants
- [ ] Meaningful variable and method names
- [ ] No commented-out code
- [ ] No unused imports or variables
- [ ] Consistent naming convention (camelCase for variables/methods, PascalCase for classes)

### UI / Swing Specific

- [ ] UI built on Event Dispatch Thread (`SwingUtilities.invokeLater`)
- [ ] Long operations not blocking the EDT
- [ ] Components properly disposed on close
- [ ] Fonts and colors defined as constants, not inline
- [ ] No hardcoded pixel values — use layout managers
- [ ] Keyboard shortcuts defined for common actions

### Performance

- [ ] No unnecessary object creation in loops
- [ ] StringBuilder used for string concatenation in loops
- [ ] Collections pre-sized when size is known
- [ ] No N+1 query patterns (if database access exists)
- [ ] Resources (files, streams) properly closed

### Maintainability

- [ ] Code is self-documenting (clear names, simple logic)
- [ ] Complex logic has explanatory comments
- [ ] Public API has Javadoc
- [ ] No deep nesting (>3 levels)
- [ ] No long parameter lists (>5 parameters)

---

## Severity Levels

| Level | Examples | Action Required |
|-------|----------|-----------------|
| 🔴 **Critical** | Hardcoded secrets, SQL injection, data exposure, `Random` for passwords | Block — fix before merge |
| 🟡 **High** | No input validation, god class, methods >50 lines, magic numbers | Request changes |
| 🟠 **Medium** | Missing Javadoc, deep nesting, long parameter lists | Approve with suggestions |
| ⚪ **Low** | Naming inconsistencies, missing comments, unused imports | Approve — fix in follow-up |

---

## Common Java Antipatterns

### Antipattern 1: Using Random for Security

```java
// ❌ WRONG — predictable output
private final Random random = new Random();
String password = generatePassword(random);

// ✅ CORRECT — cryptographically strong
private final SecureRandom random = new SecureRandom();
String password = generatePassword(random);
```

**Severity:** 🔴 Critical  
**Fix:** Replace `Random` with `SecureRandom`

### Antipattern 2: Magic Numbers

```java
// ❌ WRONG — unclear intent
if (length < 8) {
    return "Weak";
}

// ✅ CORRECT — self-documenting
private static final int WEAK_THRESHOLD = 8;
if (length < WEAK_THRESHOLD) {
    return "Weak";
}
```

**Severity:** 🟡 High  
**Fix:** Extract to named constants

### Antipattern 3: God Class

```java
// ❌ WRONG — too many responsibilities
class PasswordGenerator {
    void generatePassword() { ... }
    void saveToDatabase() { ... }
    void sendEmail() { ... }
    void logAnalytics() { ... }
    void checkBreaches() { ... }
    // 20+ more methods
}

// ✅ CORRECT — focused classes
class PasswordService {
    String generate(int length) { ... }
}
class PasswordRepository {
    void save(Password p) { ... }
}
class EmailService {
    void send(String to, String body) { ... }
}
```

**Severity:** 🟠 Medium  
**Fix:** Split into focused classes

### Antipattern 4: Blocking EDT

```java
// ❌ WRONG — UI freezes during operation
button.addActionListener(e -> {
    Thread.sleep(5000); // Blocks UI
    updateLabel();
});

// ✅ CORRECT — background thread
button.addActionListener(e -> {
    SwingWorker<Void, Void> worker = new SwingWorker<>() {
        @Override
        protected Void doInBackground() throws Exception {
            Thread.sleep(5000); // Runs in background
            return null;
        }
        @Override
        protected void done() {
            updateLabel(); // Updates UI on EDT
        }
    };
    worker.execute();
});
```

**Severity:** 🟡 High  
**Fix:** Use `SwingWorker` for long operations

### Antipattern 5: Catching Exception Broadly

```java
// ❌ WRONG — hides bugs
try {
    riskyOperation();
} catch (Exception e) {
    // Silent failure
}

// ✅ CORRECT — specific exceptions
try {
    riskyOperation();
} catch (IOException e) {
    logger.error("File operation failed", e);
    showErrorDialog("Could not save file");
} catch (SecurityException e) {
    logger.error("Permission denied", e);
    showErrorDialog("Access denied");
}
```

**Severity:** 🟡 High  
**Fix:** Catch specific exceptions, log errors

### Antipattern 6: Public Fields

```java
// ❌ WRONG — breaks encapsulation
class User {
    public String name;
    public int age;
}

// ✅ CORRECT — private with getters
class User {
    private String name;
    private int age;
    
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
}
```

**Severity:** 🟠 Medium  
**Fix:** Make fields private, add getters/setters

---

## Security Patterns

### Pattern 1: Input Validation

```java
// Validate spinner input (already handled by SpinnerNumberModel)
JSpinner lengthSpinner = new JSpinner(
    new SpinnerNumberModel(12, 4, 128, 1)
    // min=4, max=128 enforced automatically
);

// Validate text input
String input = textField.getText();
if (input == null || input.trim().isEmpty()) {
    showError("Input cannot be empty");
    return;
}
if (input.length() > MAX_LENGTH) {
    showError("Input too long");
    return;
}
```

### Pattern 2: Secure Random Initialization

```java
// ✅ CORRECT — initialized once, reused
private final SecureRandom random = new SecureRandom();

// ❌ WRONG — re-initializing in loop (slow)
for (int i = 0; i < 100; i++) {
    SecureRandom r = new SecureRandom(); // Don't do this
    passwords.add(generate(r));
}
```

### Pattern 3: No Sensitive Data in Logs

```java
// ❌ WRONG — password in logs
logger.info("Generated password: " + password);

// ✅ CORRECT — log metadata only
logger.info("Generated password of length: " + password.length());
```

---

## Code Quality Metrics

### Thresholds

| Metric | Threshold | Severity if Exceeded |
|--------|-----------|---------------------|
| Method length | >50 lines | 🟡 High |
| Class length | >500 lines | 🟠 Medium |
| Method count per class | >20 | 🟠 Medium |
| Parameter count | >5 | 🟠 Medium |
| Nesting depth | >3 levels | 🟠 Medium |
| Cyclomatic complexity | >10 | 🟡 High |
| Duplicate code | >5 lines repeated | 🟠 Medium |

### Calculating Cyclomatic Complexity

```
Complexity = (decision points) + 1

Decision points:
- if, else if
- for, while, do-while
- case in switch
- catch
- &&, ||, ?:
```

**Example:**
```java
public String assess(int length) {
    if (length < 8) {           // +1
        return "Weak";
    } else if (length < 14) {   // +1
        return "Good";
    } else if (length < 20) {   // +1
        return "Strong";
    } else {
        return "Very Strong";
    }
}
// Complexity = 3 + 1 = 4 (acceptable)
```

---

## Review Verdict Guide

### Verdict Decision Table

| Condition | Verdict | Action |
|-----------|---------|--------|
| No issues | ✅ **Approve** | Merge immediately |
| Low issues only | ✅ **Approve** | Merge, fix in follow-up |
| Medium issues | 💬 **Approve with suggestions** | Merge, create follow-up issues |
| High issues | ❌ **Request changes** | Fix before merge |
| Critical issues | 🚫 **Block** | Do not merge until fixed |

### Verdict Template

```markdown
## Review Verdict: [Approve / Approve with suggestions / Request changes / Block]

### Summary
[One sentence summary of the change]

### Issues Found
🔴 Critical: [count]
🟡 High: [count]
🟠 Medium: [count]
⚪ Low: [count]

### Critical Issues
1. [Issue description] — Line [X]
   - **Fix:** [Specific remediation]

### High Issues
1. [Issue description] — Line [X]
   - **Fix:** [Specific remediation]

### Suggestions
- [Optional improvement]
- [Optional improvement]

### Verdict Rationale
[Why this verdict was chosen]
```

---

## This Project Assessment

### PasswordGenerator.java — Current State

✅ **Strengths:**
- `SecureRandom` used correctly
- UI constants defined (colors, fonts)
- EDT-safe via `SwingUtilities.invokeLater`
- Input validation handled by `SpinnerNumberModel` bounds
- Single responsibility maintained (for current scope)
- No hardcoded secrets
- Clean separation of UI and logic within single class

⚠️ **Potential Improvements:**
- Could extract `PasswordService` class if adding more features
- Add Javadoc for public methods
- Consider adding unit tests (requires refactoring for testability)
- Add keyboard shortcuts (e.g., Ctrl+G to generate)

**Overall Verdict:** ✅ **Approve** — well-structured for current scope, no blocking issues.
