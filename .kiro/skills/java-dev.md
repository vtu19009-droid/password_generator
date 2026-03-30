---
name: "java-dev"
description: Use this skill when the user asks to build, improve, debug, or review Java code, Swing/JavaFX UIs, compile and run Java apps, or work with Java project structure.
inclusion: auto
---

# Java Developer Skill

Expert Java development guidance for this workspace — covering Swing UI, SecureRandom, compilation, and project structure.

## This Project

- `PasswordGenerator.java` — single-file Swing app, dark-themed UI, `SecureRandom`-based password generation
- Compile: `javac PasswordGenerator.java`
- Run: `java PasswordGenerator`
- Requires: Java 8+, no external dependencies

---

## Workflows

### Build & Run
```bash
javac PasswordGenerator.java
java PasswordGenerator
```

### Clean compiled files
```bash
rm -f *.class
```

### Package as runnable JAR
```bash
jar cfe PasswordGenerator.jar PasswordGenerator *.class
java -jar PasswordGenerator.jar
```

---

## Swing UI Patterns (used in this project)

### Dark theme setup
```java
getContentPane().setBackground(new Color(15, 17, 26));
panel.setBackground(new Color(24, 27, 42));
label.setForeground(new Color(226, 232, 240));
```

### Rounded custom button
```java
JButton btn = new JButton(text) {
    @Override protected void paintComponent(Graphics g) {
        Graphics2D g2 = (Graphics2D) g.create();
        g2.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
        g2.setColor(getBackground());
        g2.fill(new RoundRectangle2D.Float(0, 0, getWidth(), getHeight(), 10, 10));
        g2.dispose();
        super.paintComponent(g);
    }
};
btn.setContentAreaFilled(false);
btn.setOpaque(false);
btn.setBorderPainted(false);
```

### Copy to clipboard
```java
Toolkit.getDefaultToolkit().getSystemClipboard()
    .setContents(new StringSelection(text), null);
```

### Timed button feedback
```java
btn.setText("Copied!");
Timer t = new Timer(1500, e -> btn.setText("Copy"));
t.setRepeats(false);
t.start();
```

---

## SecureRandom Password Generation

```java
private static final String CHARS =
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()";
private final SecureRandom random = new SecureRandom();

String generate(int length) {
    StringBuilder sb = new StringBuilder(length);
    for (int i = 0; i < length; i++)
        sb.append(CHARS.charAt(random.nextInt(CHARS.length())));
    return sb.toString();
}
```

Always prefer `SecureRandom` over `Random` for security-sensitive generation.

---

## Strength Classification

| Length | Strength |
|--------|----------|
| < 8    | Weak     |
| 8–13   | Good     |
| 14–19  | Strong   |
| 20+    | Very Strong |

---

## Common Enhancements

- Add a slider (`JSlider`) alongside the spinner for length control
- Add checkboxes to toggle character sets (uppercase, digits, symbols)
- Save history of generated passwords in a `JList`
- Export passwords to a `.txt` file using `JFileChooser`
- Add a `JProgressBar` as a visual strength meter

---

## Decision Guide

| Need | Approach |
|------|----------|
| Simple UI, no deps | Swing (current) |
| Modern look, CSS-like styling | JavaFX + CSS |
| Cross-platform packaging | jpackage (Java 14+) |
| Web-based UI | Spring Boot + Thymeleaf |
