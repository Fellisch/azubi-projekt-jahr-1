import os
from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QFrame, QScrollArea
from PySide6.QtGui import QIcon, QFontDatabase, QFont
from PySide6.QtCore import QSize, Qt
from gui.rule import Rule
from gui.core.confiq import Colors

class RulesToggle(QWidget):
    def __init__(self, game, violated_ids=None):
        super().__init__()
        self.game = game
        self.violated_ids = violated_ids or []

        self.setFixedSize(250, 290)
        self.setStyleSheet("background-color: transparent;")

        self.container = QFrame(self)
        self.container.setGeometry(0, 0, 250, 290)
        self.container.setStyleSheet("background-color: transparent;")

        self.rulesWidget = QScrollArea(self.container)
        self.rulesWidget.setGeometry(0, 0, 231, 235)
        self.rulesWidget.setWidgetResizable(True)
        self.rulesWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.rulesWidget.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.rulesWidget.setStyleSheet(f"""
            QScrollArea {{
                background-color: {Colors.SECONDARY};
                border-radius: 8px;
                border: none; 
            }}
            QScrollBar:vertical {{
                border: none;
                background: transparent; 
                width: 8px;
                margin: 0px 0px 0px 0px; 
            }}
            QScrollBar::handle:vertical {{
                background: {Colors.PRIMARY}; 
                min-height: 20px;
                border-radius: 4px;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
                border: none;
                background: none;
            }}
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
                background: none;
            }}
        """)
        
        self.rulesContentHolder = QWidget() 
        self.rulesContentHolder.setStyleSheet("background-color: transparent;")

        self.rulesLayout = QVBoxLayout(self.rulesContentHolder)
        self.rulesLayout.setContentsMargins(10, 10, 10, 10)
        self.rulesLayout.setSpacing(8)

        self.rule_font_family = QFont().family()
        current_font_dir = os.path.dirname(os.path.abspath(__file__))
        fonts_dir = os.path.join(current_font_dir, "assets", "fonts")
        
        rule_bold_font_filename = "JetBrainsMono-Bold.ttf"
        rule_bold_font_path = os.path.join(fonts_dir, rule_bold_font_filename)

        rule_bold_font_id = QFontDatabase.addApplicationFont(rule_bold_font_path)
        if rule_bold_font_id != -1:
            loaded_rule_bold_families = QFontDatabase.applicationFontFamilies(rule_bold_font_id)
            if loaded_rule_bold_families:
                self.rule_font_family = loaded_rule_bold_families[0]
        
        self.rules_text_qfont = QFont(self.rule_font_family, 12, QFont.Bold)

        self.rules = []
        rules_text_list = self.game.get_rules()
        for idx, rule_text in enumerate(rules_text_list):
            rule = Rule(rule_id=idx, text=rule_text.strip(), bold=False)
            rule.setFont(self.rules_text_qfont)
            self.rules.append(rule)
            self.rulesLayout.addWidget(rule)

        self.rulesWidget.setWidget(self.rulesContentHolder)

        self.rulesWidget.setVisible(False)

        self.toggleButton = QPushButton("", self.container)
        self.toggleButton.setFixedSize(46, 46)

        base_dir = os.path.dirname(os.path.abspath(__file__))
        assets_svg_dir = os.path.join(base_dir, "assets", "svg")
        icon_path = os.path.join(assets_svg_dir, "rulesButton.svg")

        if os.path.exists(icon_path):
            icon = QIcon(icon_path)
            self.toggleButton.setIcon(icon)
            self.toggleButton.setIconSize(QSize(40, 40))
        else:
            self.toggleButton.setText("!")

        self.toggleButton.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                border: none;
                padding: 0px;
            }}
        """)

        self.toggleButton.move(188, 242)
        self.toggleButton.clicked.connect(self.toggleRules)

    def toggleRules(self):
        self.rulesWidget.setVisible(not self.rulesWidget.isVisible())

    def setViolatedRules(self, violated_ids):
        self.violated_ids = violated_ids
        for rule in self.rules:
            rule.setBold(rule.rule_id in violated_ids)