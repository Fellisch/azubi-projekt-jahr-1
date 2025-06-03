import os
from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QFrame
from PySide6.QtGui import QIcon # Added QIcon
from PySide6.QtCore import QSize # Added QSize
from gui.rule import Rule  # import Rule class
from gui.core.confiq import Colors

class RulesToggle(QWidget):
    def __init__(self, game, violated_ids=None):
        super().__init__()
        self.game = game  # Store the BaseGame instance
        self.violated_ids = violated_ids or []

        self.setFixedSize(250, 290)
        self.setStyleSheet("background-color: transparent;")

        self.container = QFrame(self)
        self.container.setGeometry(0, 0, 250, 290)
        self.container.setStyleSheet("background-color: transparent;")

        self.rulesWidget = QWidget(self.container)
        self.rulesWidget.setGeometry(0, 0, 231, 235)
        self.rulesWidget.setStyleSheet(f"""
            background-color: {Colors.SECONDARY};
            border-radius: 8px;
        """)
        self.rulesLayout = QVBoxLayout(self.rulesWidget)
        self.rulesLayout.setContentsMargins(10, 10, 10, 10)
        self.rulesLayout.setSpacing(8)

        self.rules = []
        # Fetch rules dynamically from the game instance
        rules_text_list = self.game.get_rules() # Expecting a list of strings now
        for idx, rule_text in enumerate(rules_text_list):
            # Assuming Rule can take a rule_id and text, using index as a simple ID
            rule = Rule(rule_id=idx, text=rule_text.strip(), bold=False)
            self.rules.append(rule)
            self.rulesLayout.addWidget(rule)

        self.rulesWidget.setVisible(False)

        self.toggleButton = QPushButton("", self.container) # Text changed to empty
        self.toggleButton.setFixedSize(46, 46)

        # Construct path to SVG icon
        base_dir = os.path.dirname(os.path.abspath(__file__))
        assets_svg_dir = os.path.join(base_dir, "assets", "svg")
        icon_path = os.path.join(assets_svg_dir, "rulesButton.svg")

        if os.path.exists(icon_path):
            icon = QIcon(icon_path)
            self.toggleButton.setIcon(icon)
            self.toggleButton.setIconSize(QSize(40, 40)) # Set icon size
        else:
            print(f"Warning: Rules button icon not found at {icon_path}. Using fallback text.")
            self.toggleButton.setText("!") # Fallback text

        self.toggleButton.setStyleSheet(f""" # Stylesheet modified
            QPushButton {{
                background-color: transparent;
                border: none;
                padding: 0px; /* Remove padding that might affect icon placement */
            }}
            QPushButton:hover {{
                /* Optional: Add a hover effect if desired, e.g., slight tint */
                /* background-color: rgba(255, 255, 255, 20); */ 
            }}
        """)

        self.toggleButton.move(188, 242) # X-coordinate changed from 215 to 201, Y is 240
        self.toggleButton.clicked.connect(self.toggleRules)

    def toggleRules(self):
        self.rulesWidget.setVisible(not self.rulesWidget.isVisible())

    def setViolatedRules(self, violated_ids):
        """Update which rules are violated to change their styling dynamically."""
        self.violated_ids = violated_ids
        for rule in self.rules:
            rule.setBold(rule.rule_id in violated_ids)