from PySide6.QtWidgets import QLabel
from gui.core.confiq import Colors
class Rule(QLabel):
    def __init__(self, rule_id: int, text: str, bold=False, parent=None):
        super().__init__(parent)
        self.rule_id = rule_id
        self.text = text
        self.bold = bold
        self.setWordWrap(True)
        self.updateStyle()

    def updateStyle(self):
        self.setText(self.text)
        self.setStyleSheet(f"""
            color: {Colors.FONT_PRIMARY};
            background-color: transparent;
            font-weight: {'bold' if self.bold else 'normal'};
        """)

    def setBold(self, bold: bool):
        self.bold = bold
        self.updateStyle()
