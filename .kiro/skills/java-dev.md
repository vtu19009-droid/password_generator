---
name: "java-dev"
description: Use this skill when the user asks to build, improve, debug, compile, run, or review Java code. Covers Swing UI, JavaFX, SecureRandom, OOP patterns, JAR packaging, and Java project structure.
inclusion: auto
---

# Java Developer

Expert Java development — Swing UI, security, OOP patterns, build tooling, and packaging.

---

## This Project

- `PasswordGenerator.java` — single-file Swing app, dark-themed UI, `SecureRandom` password generation
- Compile: `javac PasswordGenerator.java`
- Run: `java PasswordGenerator`
- Package: `jar cfe PasswordGenerator.jar PasswordGenerator *.class && java -jar PasswordGenerator.jar`
- Requires: Java 8+, zero external dependencies

---

## Build & Run Workflows

### Compile and run
```bash
javac PasswordGenerator.java
java PasswordGenerator
```

### Clean build artifacts
```bash
rm -f *.class
```

### Package as executable JAR
```bash
jar cfe PasswordGenerator.jar PasswordGenerator *.class
java -jar PasswordGenerator.jar
```

### Check Java version
```bash
java -version
javac -version
```

---

## Swing UI Patterns

### Dark theme setup
```java
getContentPane().setBackground(new Color(15, 17, 26));
panel.setBackground(new Color(24, 27, 42));
label.setForeground(new Color(226, 232, 240));
field.setBackground(new Color(30, 34, 54));
```

### Rounded custom button (anti-aliased)
```java
JButton btn = new JButton(text) {
    @Override protected void paintComponent(Graphics g) {
        Graphics2D g2 = (Graphics2D) g.create();
        g2.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
        g2.setColor(getModel().isPressed() ? bg.darker() : bg);
        g2.fill(new RoundRectangle2D.Float(0, 0, getWidth(), getHeight(), 10, 10));
        g2.dispose();
        super.paintComponent(g);
    }
};
btn.setContentAreaFilled(false);
btn.setOpaque(false);
btn.setBorderPainted(false);
btn.setFocusPainted(false);
```

### Copy to clipboard
```java
Toolkit.getDefaultToolkit().getSystemClipboard()
    .setContents(new StringSelection(text), null);
```

### Timed button feedback
```java
btn.setText("Copied!");
Timer t = new Timer(1500, e -> btn.setText("Copy to Clipboard"));
t.setRepeats(false);
t.start();
```

### Center window on screen
```java
setLocationRelativeTo(null);
```

### Spinner with custom styling
```java
JSpinner spinner = new JSpinner(new SpinnerNumberModel(12, 4, 128, 1));
JSpinner.DefaultEditor editor = (JSpinner.DefaultEditor) spinner.getEditor();
editor.getTextField().setBackground(FIELD_BG);
editor.getTextField().setForeground(TEXT);
```

---

## SecureRandom Password Generation

```java
private static final String CHARS =
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()-_=+[]{}|;:,.<>?";
private final SecureRandom random = new SecureRandom();

String generate(int length) {
    StringBuilder sb = new StringBuilder(length);
    for (int i = 0; i < length; i++)
        sb.append(CHARS.charAt(random.nextInt(CHARS.length())));
    return sb.toString();
}
```

Always use `SecureRandom` over `Random` for any security-sensitive generation.

---

## Password Strength Classification

| Length | Strength     | Color (hex) |
|--------|--------------|-------------|
| < 8    | Weak         | #EF4444     |
| 8–13   | Good         | #EAB308     |
| 14–19  | Strong       | #22C55E     |
| 20+    | Very Strong  | #6366F1     |

---

## OOP Patterns for Java Swing Apps

### Single responsibility — separate concerns
```java
class PasswordService {
    String generate(int length) { ... }
    String assessStrength(int length) { ... }
}

class PasswordGeneratorUI extends JFrame {
    private final PasswordService service = new PasswordService();
    ...
}
```

### Observer pattern for UI updates
```java
lengthSpinner.addChangeListener(e -> updateStrengthLabel());
generateBtn.addActionListener(e -> refreshPassword());
```

---

## Common Enhancements

| Feature | How |
|---------|-----|
| Slider for length | Add `JSlider` synced with spinner |
| Character set toggles | `JCheckBox` for uppercase / digits / symbols |
| Password history | `DefaultListModel` + `JList` |
| Export to file | `JFileChooser` + `FileWriter` |
| Visual strength bar | `JProgressBar` mapped to length |
| Tooltip hints | `component.setToolTipText("...")` |

---

## Framework Decision Guide

| Need | Recommendation |
|------|----------------|
| Simple desktop app, no deps | Swing (current) |
| Modern CSS-like styling | JavaFX + FXML |
| Cross-platform installer | `jpackage` (Java 14+) |
| Web UI | Spring Boot + Thymeleaf |
| Mobile | Android SDK / Kotlin |
