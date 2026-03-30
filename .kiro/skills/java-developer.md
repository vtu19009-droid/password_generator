---
name: "java-developer"
description: "Use when building, debugging, compiling, or optimizing Java applications. Covers Swing/JavaFX UI, SecureRandom, OOP patterns, JAR packaging, performance tuning, and Java project structure. Triggers: 'compile Java', 'build Swing app', 'package JAR', 'Java performance', 'fix Java error'."
version: "1.0.0"
category: "engineering"
tier: "standard"
inclusion: "auto"
requires: []
---

# Java Developer

Expert Java development — Swing UI, security, OOP patterns, build tooling, and packaging.

---

## Table of Contents

- [Quick Start](#quick-start)
- [This Project](#this-project)
- [Build & Run Workflows](#build--run-workflows)
- [Swing UI Patterns](#swing-ui-patterns)
- [Security Best Practices](#security-best-practices)
- [OOP Design Patterns](#oop-design-patterns)
- [Performance Optimization](#performance-optimization)
- [Common Enhancements](#common-enhancements)
- [Framework Decision Guide](#framework-decision-guide)
- [Reference Documentation](#reference-documentation)

---

## Quick Start

```bash
# Compile and run
javac PasswordGenerator.java && java PasswordGenerator

# Package as executable JAR
jar cfe PasswordGenerator.jar PasswordGenerator *.class

# Run JAR
java -jar PasswordGenerator.jar

# Clean build artifacts
rm -f *.class *.jar
```

---

## This Project

| Property | Value |
|----------|-------|
| **Main file** | `PasswordGenerator.java` |
| **Type** | Single-file Swing desktop app |
| **UI Framework** | Swing with custom dark theme |
| **Security** | `SecureRandom` for password generation |
| **Dependencies** | Zero — pure JDK |
| **Java Version** | 8+ (tested on 17) |
| **Build Tool** | Manual `javac` (no Maven/Gradle) |

---

## Build & Run Workflows

### Workflow 1: Development Cycle

```
Edit → Compile → Test → Iterate
```

**Step 1: Edit code**
```bash
# Open in your editor
code PasswordGenerator.java
```

**Step 2: Compile**
```bash
javac PasswordGenerator.java
# Check for errors — zero output = success
```

**Step 3: Run**
```bash
java PasswordGenerator
# UI window should appear
```

**Step 4: Iterate**
- Make changes
- Recompile (only changed files)
- Test again

### Workflow 2: Production Build

```
Clean → Compile → Package → Verify → Distribute
```

**Step 1: Clean**
```bash
rm -f *.class *.jar
```

**Step 2: Compile with optimizations**
```bash
javac -g:none -O PasswordGenerator.java
# -g:none removes debug info
# -O enables optimizations (deprecated but still works)
```

**Step 3: Package as JAR**
```bash
jar cfe PasswordGenerator.jar PasswordGenerator *.class
# c = create, f = file, e = entry point
```

**Step 4: Verify**
```bash
java -jar PasswordGenerator.jar
# Should launch without errors
```

**Step 5: Distribute**
```bash
# JAR is now portable — runs on any system with Java 8+
```

### Workflow 3: Cross-Platform Installer

```
Build → jpackage → Test → Distribute
```

**Requirements:** Java 14+ for `jpackage`

```bash
# macOS app bundle
jpackage --input . \
  --name PasswordGenerator \
  --main-jar PasswordGenerator.jar \
  --main-class PasswordGenerator \
  --type dmg

# Windows installer
jpackage --input . \
  --name PasswordGenerator \
  --main-jar PasswordGenerator.jar \
  --main-class PasswordGenerator \
  --type msi

# Linux package
jpackage --input . \
  --name PasswordGenerator \
  --main-jar PasswordGenerator.jar \
  --main-class PasswordGenerator \
  --type deb
```

---

## Swing UI Patterns

### Pattern 1: Dark Theme Setup

```java
// Color palette as constants
private static final Color BG       = new Color(15, 17, 26);
private static final Color CARD     = new Color(24, 27, 42);
private static final Color ACCENT   = new Color(99, 102, 241);
private static final Color TEXT     = new Color(226, 232, 240);
private static final Color SUBTEXT  = new Color(148, 163, 184);
private static final Color FIELD_BG = new Color(30, 34, 54);
private static final Color BORDER_C = new Color(51, 56, 84);

// Apply to components
getContentPane().setBackground(BG);
panel.setBackground(CARD);
label.setForeground(TEXT);
field.setBackground(FIELD_BG);
```

**Why:** Centralized color management, easy theme switching.

### Pattern 2: Rounded Custom Button

```java
private JButton makeButton(String text, Color bg, Color fg) {
    JButton btn = new JButton(text) {
        @Override
        protected void paintComponent(Graphics g) {
            Graphics2D g2 = (Graphics2D) g.create();
            g2.setRenderingHint(RenderingHints.KEY_ANTIALIASING, 
                               RenderingHints.VALUE_ANTIALIAS_ON);
            
            // Hover/press states
            if (getModel().isPressed()) 
                g2.setColor(bg.darker());
            else if (getModel().isRollover()) 
                g2.setColor(bg.brighter());
            else 
                g2.setColor(bg);
            
            g2.fill(new RoundRectangle2D.Float(0, 0, getWidth(), getHeight(), 10, 10));
            g2.dispose();
            super.paintComponent(g);
        }
    };
    
    btn.setFont(new Font("SansSerif", Font.BOLD, 14));
    btn.setForeground(fg);
    btn.setBackground(bg);
    btn.setOpaque(false);
    btn.setContentAreaFilled(false);
    btn.setBorderPainted(false);
    btn.setFocusPainted(false);
    btn.setCursor(Cursor.getPredefinedCursor(Cursor.HAND_CURSOR));
    
    return btn;
}
```

**Why:** Modern look without external libraries, full control over rendering.

### Pattern 3: Copy to Clipboard

```java
import java.awt.Toolkit;
import java.awt.datatransfer.StringSelection;

// Copy text
Toolkit.getDefaultToolkit().getSystemClipboard()
    .setContents(new StringSelection(text), null);
```

**Why:** Cross-platform clipboard access, no dependencies.

### Pattern 4: Timed Button Feedback

```java
import javax.swing.Timer;

// Show "Copied!" for 1.5 seconds
btn.setText("Copied!");
Timer t = new Timer(1500, e -> btn.setText("Copy to Clipboard"));
t.setRepeats(false);
t.start();
```

**Why:** User feedback without blocking the UI thread.

### Pattern 5: Center Window on Screen

```java
setLocationRelativeTo(null);
```

**Why:** Works on any screen resolution, single line.

### Pattern 6: Spinner with Custom Styling

```java
JSpinner spinner = new JSpinner(new SpinnerNumberModel(12, 4, 128, 1));
JSpinner.DefaultEditor editor = (JSpinner.DefaultEditor) spinner.getEditor();
editor.getTextField().setBackground(FIELD_BG);
editor.getTextField().setForeground(TEXT);
editor.getTextField().setHorizontalAlignment(JTextField.CENTER);
spinner.setBackground(FIELD_BG);
spinner.setBorder(new LineBorder(BORDER_C, 1, true));
```

**Why:** Consistent styling with the rest of the dark theme.

---

## Security Best Practices

### Rule 1: Use SecureRandom, Not Random

```java
// ❌ WRONG — predictable output
private final Random random = new Random();

// ✅ CORRECT — cryptographically strong
private final SecureRandom random = new SecureRandom();
```

**Why:** `Random` uses a linear congruential generator — predictable if seed is known. `SecureRandom` uses OS entropy sources.

### Rule 2: Define Character Sets as Constants

```java
private static final String CHARS =
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()-_=+[]{}|;:,.<>?";
```

**Why:** Centralized, auditable, easy to modify.

### Rule 3: Password Generation Pattern

```java
private String generatePassword(int length) {
    StringBuilder sb = new StringBuilder(length);
    for (int i = 0; i < length; i++) {
        sb.append(CHARS.charAt(random.nextInt(CHARS.length())));
    }
    return sb.toString();
}
```

**Why:** Efficient, uniform distribution, no bias.

### Password Strength Classification

| Length | Strength     | Color (RGB)      | Rationale |
|--------|--------------|------------------|-----------|
| < 8    | Weak         | `239, 68, 68`    | Brute-forceable in hours |
| 8–13   | Good         | `234, 179, 8`    | Adequate for most uses |
| 14–19  | Strong       | `34, 197, 94`    | Resistant to offline attacks |
| 20+    | Very Strong  | `99, 102, 241`   | Overkill for most, good for master passwords |

---

## OOP Design Patterns

### When to Refactor from Single Class

Current structure is appropriate for this project. Refactor when:

- [ ] Adding persistent storage (password history)
- [ ] Adding multiple screens/views
- [ ] Adding network calls (breach checking API)
- [ ] Team of 2+ developers

### Suggested Split (if needed)

```
PasswordService.java       — generation logic, strength scoring
PasswordGeneratorUI.java   — all Swing components
AppConfig.java             — constants (colors, fonts, char sets)
Main.java                  — entry point
```

### Pattern: Single Responsibility

```java
// Before: God class
class PasswordGenerator {
    void generatePassword() { ... }
    void updateUI() { ... }
    void saveToFile() { ... }
    void checkBreaches() { ... }
}

// After: Focused classes
class PasswordService {
    String generate(int length) { ... }
    String assessStrength(int length) { ... }
}

class PasswordGeneratorUI extends JFrame {
    private final PasswordService service = new PasswordService();
    // UI code only
}
```

### Pattern: Observer for UI Updates

```java
lengthSpinner.addChangeListener(e -> updateStrengthLabel());
generateBtn.addActionListener(e -> refreshPassword());
```

**Why:** Decouples UI events from business logic.

---

## Performance Optimization

### Optimization 1: StringBuilder for String Concatenation

```java
// ❌ SLOW — creates N string objects
String result = "";
for (int i = 0; i < length; i++) {
    result += CHARS.charAt(random.nextInt(CHARS.length()));
}

// ✅ FAST — single mutable buffer
StringBuilder sb = new StringBuilder(length);
for (int i = 0; i < length; i++) {
    sb.append(CHARS.charAt(random.nextInt(CHARS.length())));
}
return sb.toString();
```

**Impact:** 10-100x faster for long passwords.

### Optimization 2: Pre-size Collections

```java
// ❌ Resizes multiple times
StringBuilder sb = new StringBuilder();

// ✅ Allocates once
StringBuilder sb = new StringBuilder(length);
```

### Optimization 3: Avoid Unnecessary Object Creation

```java
// ❌ Creates new Font every paint
label.setFont(new Font("SansSerif", Font.BOLD, 14));

// ✅ Reuse constant
private static final Font LABEL_FONT = new Font("SansSerif", Font.BOLD, 14);
label.setFont(LABEL_FONT);
```

---

## Common Enhancements

| Feature | Implementation | Complexity |
|---------|----------------|------------|
| **Slider for length** | Add `JSlider` synced with spinner | Low |
| **Character set toggles** | `JCheckBox` for uppercase/digits/symbols | Medium |
| **Password history** | `DefaultListModel` + `JList` | Medium |
| **Export to file** | `JFileChooser` + `FileWriter` | Low |
| **Visual strength bar** | `JProgressBar` mapped to length | Low |
| **Tooltip hints** | `component.setToolTipText("...")` | Low |
| **Pronounceable passwords** | Syllable-based generation algorithm | High |
| **Breach checking** | API call to HaveIBeenPwned | Medium |
| **Password manager integration** | System keychain access | High |

---

## Framework Decision Guide

| Need | Recommendation | Rationale |
|------|----------------|-----------|
| Simple desktop app, no deps | **Swing** (current) | Ships with JDK, zero setup |
| Modern CSS-like styling | **JavaFX + FXML** | Better look, CSS support |
| Cross-platform installer | **jpackage** (Java 14+) | Native installers for all platforms |
| Web UI | **Spring Boot + Thymeleaf** | Full web stack |
| Mobile | **Android SDK / Kotlin** | Native mobile development |

---

## Reference Documentation

| File | Contains | Use When |
|------|----------|----------|
| `references/swing-patterns.md` | 15 common Swing patterns | Building UI components |
| `references/java-security.md` | Security best practices | Handling sensitive data |
| `references/oop-antipatterns.md` | What NOT to do | Code review |

---

## Common Commands

```bash
# Development
javac PasswordGenerator.java
java PasswordGenerator

# Production build
javac -g:none PasswordGenerator.java
jar cfe PasswordGenerator.jar PasswordGenerator *.class

# Clean
rm -f *.class *.jar

# Check Java version
java -version
javac -version

# Run with specific Java version (if multiple installed)
/usr/libexec/java_home -V
export JAVA_HOME=$(/usr/libexec/java_home -v 17)
```
