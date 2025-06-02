from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QFrame
from gui.rule import Rule  # import Rule class
from gui.core.confiq import Colors

class RulesToggle(QWidget):
    def __init__(self, game, violated_ids=None):
        super().__init__()
        self.game = game  # Store the BaseGame instance
        self.violated_ids = violated_ids or []

        self.setFixedSize(250, 250)
        self.setStyleSheet("background-color: transparent;")

        self.container = QFrame(self)
        self.container.setGeometry(0, 0, 250, 250)
        self.container.setStyleSheet("background-color: transparent;")

        self.rulesWidget = QWidget(self.container)
        self.rulesWidget.setGeometry(0, 0, 231, 180)
        self.rulesWidget.setStyleSheet(f"""
            background-color: {Colors.SECONDARY};
            border-radius: 8px;
        """)
        self.rulesLayout = QVBoxLayout(self.rulesWidget)
        self.rulesLayout.setContentsMargins(10, 10, 10, 10)
        self.rulesLayout.setSpacing(8)

        self.rules = []
        # Fetch rules dynamically from the game instance
        rules_text = self.game.get_rules()
        rule_lines = rules_text.strip().split('\n')  # Split into individual lines
        for idx, rule_text in enumerate(rule_lines):
            # Assuming Rule can take a rule_id and text, using index as a simple ID
            rule = Rule(rule_id=idx, text=rule_text.strip(), bold=False)
            self.rules.append(rule)
            self.rulesLayout.addWidget(rule)

        self.rulesWidget.setVisible(False)

        self.toggleButton = QPushButton("!", self.container)
        self.toggleButton.setFixedSize(30, 30)
        self.toggleButton.setStyleSheet(f"""
            QPushButton {{
                background-color: {Colors.SECONDARY};
                color: white;
                border-radius: 15px;
                font-weight: bold;
                font-size: 18px;
            }}
        """)

        self.toggleButton.move(215, 215)  # bottom right inside container
        self.toggleButton.clicked.connect(self.toggleRules)

    def toggleRules(self):
        self.rulesWidget.setVisible(not self.rulesWidget.isVisible())

    def setViolatedRules(self, violated_ids):
        """Update which rules are violated to change their styling dynamically."""
        self.violated_ids = violated_ids
        for rule in self.rules:
            rule.setBold(rule.rule_id in violated_ids)