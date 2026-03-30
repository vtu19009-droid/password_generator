import javax.swing.*;
import javax.swing.border.*;
import java.awt.*;
import java.awt.datatransfer.StringSelection;
import java.awt.geom.RoundRectangle2D;
import java.security.SecureRandom;

public class PasswordGenerator extends JFrame {

    private static final String CHARS =
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()-_=+[]{}|;:,.<>?";

    private static final Color BG       = new Color(15, 17, 26);
    private static final Color CARD     = new Color(24, 27, 42);
    private static final Color ACCENT   = new Color(99, 102, 241);
    private static final Color TEXT     = new Color(226, 232, 240);
    private static final Color SUBTEXT  = new Color(148, 163, 184);
    private static final Color FIELD_BG = new Color(30, 34, 54);
    private static final Color BORDER_C = new Color(51, 56, 84);

    private final SecureRandom random = new SecureRandom();
    private JSpinner lengthSpinner;
    private JTextField passwordField;
    private JLabel strengthLabel;

    public PasswordGenerator() {
        setTitle("Password Generator");
        setDefaultCloseOperation(EXIT_ON_CLOSE);
        setResizable(false);
        getContentPane().setBackground(BG);
        setLayout(new BorderLayout());
        add(buildMainPanel());
        pack();
        setMinimumSize(new Dimension(460, 420));
        setLocationRelativeTo(null);
    }

    private JPanel buildMainPanel() {
        JPanel outer = new JPanel(new GridBagLayout());
        outer.setBackground(BG);
        outer.setBorder(new EmptyBorder(30, 30, 30, 30));

        JPanel card = new JPanel();
        card.setLayout(new BoxLayout(card, BoxLayout.Y_AXIS));
        card.setBackground(CARD);
        card.setBorder(new CompoundBorder(
            new LineBorder(BORDER_C, 1, true),
            new EmptyBorder(32, 36, 32, 36)
        ));

        JLabel title = new JLabel("Password Generator");
        title.setFont(new Font("SansSerif", Font.BOLD, 24));
        title.setForeground(TEXT);
        title.setAlignmentX(CENTER_ALIGNMENT);

        JLabel subtitle = new JLabel("Secure  |  Fast  |  Simple");
        subtitle.setFont(new Font("SansSerif", Font.PLAIN, 13));
        subtitle.setForeground(SUBTEXT);
        subtitle.setAlignmentX(CENTER_ALIGNMENT);

        JSeparator sep = new JSeparator();
        sep.setForeground(BORDER_C);
        sep.setMaximumSize(new Dimension(Integer.MAX_VALUE, 1));

        JPanel lengthRow = new JPanel(new BorderLayout(12, 0));
        lengthRow.setBackground(CARD);
        lengthRow.setMaximumSize(new Dimension(Integer.MAX_VALUE, 44));

        JLabel lenLabel = new JLabel("Password Length");
        lenLabel.setFont(new Font("SansSerif", Font.PLAIN, 14));
        lenLabel.setForeground(TEXT);

        lengthSpinner = new JSpinner(new SpinnerNumberModel(12, 4, 128, 1));
        JSpinner.DefaultEditor editor = (JSpinner.DefaultEditor) lengthSpinner.getEditor();
        editor.getTextField().setFont(new Font("Monospaced", Font.BOLD, 14));
        editor.getTextField().setForeground(TEXT);
        editor.getTextField().setBackground(FIELD_BG);
        editor.getTextField().setBorder(new EmptyBorder(4, 8, 4, 8));
        editor.getTextField().setHorizontalAlignment(JTextField.CENTER);
        lengthSpinner.setBackground(FIELD_BG);
        lengthSpinner.setBorder(new LineBorder(BORDER_C, 1, true));
        lengthSpinner.setPreferredSize(new Dimension(80, 36));
        lengthSpinner.addChangeListener(e -> updateStrength());

        lengthRow.add(lenLabel, BorderLayout.WEST);
        lengthRow.add(lengthSpinner, BorderLayout.EAST);

        passwordField = new JTextField("Click generate to create a password");
        passwordField.setFont(new Font("Monospaced", Font.PLAIN, 15));
        passwordField.setEditable(false);
        passwordField.setForeground(SUBTEXT);
        passwordField.setBackground(FIELD_BG);
        passwordField.setHorizontalAlignment(JTextField.CENTER);
        passwordField.setBorder(new CompoundBorder(
            new LineBorder(BORDER_C, 1, true),
            new EmptyBorder(12, 14, 12, 14)
        ));
        passwordField.setMaximumSize(new Dimension(Integer.MAX_VALUE, 50));

        strengthLabel = new JLabel(" ");
        strengthLabel.setFont(new Font("SansSerif", Font.BOLD, 12));
        strengthLabel.setAlignmentX(CENTER_ALIGNMENT);
        updateStrength();

        JButton generateBtn = makeButton("Generate Password", ACCENT, Color.WHITE);
        generateBtn.addActionListener(e -> generatePassword());

        JButton copyBtn = makeButton("Copy to Clipboard", FIELD_BG, SUBTEXT);
        copyBtn.setBorder(new CompoundBorder(
            new LineBorder(BORDER_C, 1, true),
            new EmptyBorder(10, 20, 10, 20)
        ));
        copyBtn.addActionListener(e -> {
            String pwd = passwordField.getText();
            if (!pwd.isEmpty() && !pwd.startsWith("Click")) {
                Toolkit.getDefaultToolkit().getSystemClipboard()
                    .setContents(new StringSelection(pwd), null);
                copyBtn.setText("Copied!");
                Timer t = new Timer(1500, ev -> copyBtn.setText("Copy to Clipboard"));
                t.setRepeats(false);
                t.start();
            }
        });

        card.add(title);
        card.add(Box.createVerticalStrut(4));
        card.add(subtitle);
        card.add(Box.createVerticalStrut(20));
        card.add(sep);
        card.add(Box.createVerticalStrut(20));
        card.add(lengthRow);
        card.add(Box.createVerticalStrut(16));
        card.add(passwordField);
        card.add(Box.createVerticalStrut(6));
        card.add(strengthLabel);
        card.add(Box.createVerticalStrut(16));
        card.add(generateBtn);
        card.add(Box.createVerticalStrut(10));
        card.add(copyBtn);

        outer.add(card);
        return outer;
    }

    private JButton makeButton(String text, Color bg, Color fg) {
        JButton btn = new JButton(text) {
            @Override
            protected void paintComponent(Graphics g) {
                Graphics2D g2 = (Graphics2D) g.create();
                g2.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
                if (getModel().isPressed()) g2.setColor(bg.darker());
                else if (getModel().isRollover()) g2.setColor(bg.brighter());
                else g2.setColor(bg);
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
        btn.setAlignmentX(CENTER_ALIGNMENT);
        btn.setMaximumSize(new Dimension(Integer.MAX_VALUE, 44));
        btn.setBorder(new EmptyBorder(10, 20, 10, 20));
        return btn;
    }

    private void generatePassword() {
        int length = (int) lengthSpinner.getValue();
        StringBuilder sb = new StringBuilder(length);
        for (int i = 0; i < length; i++)
            sb.append(CHARS.charAt(random.nextInt(CHARS.length())));
        passwordField.setText(sb.toString());
        passwordField.setForeground(TEXT);
        updateStrength();
    }

    private void updateStrength() {
        int len = (int) lengthSpinner.getValue();
        if (len < 8) {
            strengthLabel.setText("Strength: Weak");
            strengthLabel.setForeground(new Color(239, 68, 68));
        } else if (len < 14) {
            strengthLabel.setText("Strength: Good");
            strengthLabel.setForeground(new Color(234, 179, 8));
        } else if (len < 20) {
            strengthLabel.setText("Strength: Strong");
            strengthLabel.setForeground(new Color(34, 197, 94));
        } else {
            strengthLabel.setText("Strength: Very Strong");
            strengthLabel.setForeground(new Color(99, 102, 241));
        }
    }

    public static void main(String[] args) {
        try { UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName()); }
        catch (Exception ignored) {}
        SwingUtilities.invokeLater(() -> new PasswordGenerator().setVisible(true));
    }
}
