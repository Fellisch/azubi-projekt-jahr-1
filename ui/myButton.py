from PySide6.QtWidgets import QPushButton, QGraphicsDropShadowEffect
from PySide6.QtGui import QCursor, QFontDatabase, QFont, QColor
from PySide6.QtCore import Qt
from ui.core.confiq import Colors
import os

class MyButton(QPushButton):
    def __init__(self, text, borderWidth=7, fontSize=18, parent=None, padding='8px 16px'):
        super().__init__(text, parent)

        # Load SUBURBIA font
        font_path = os.path.join(os.path.dirname(__file__), "assets", "fonts", "SUBURBIA.ttf")
        font_id = QFontDatabase.addApplicationFont(font_path)
        if font_id != -1:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            self.setFont(QFont(font_family, fontSize))
        else:
            print("Failed to load Suburbia font")

        # Style
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setStyleSheet(f"""
            QPushButton {{
                color: {Colors.FONT_PRIMARY};
                background-color: {Colors.TERTIARY};
                border: {borderWidth}px solid {Colors.SECONDARY};
                border-radius: 10px;
                padding: {padding};
            }}
            QPushButton:hover {{
            }}
        """)

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setOffset(0, 4)
        shadow.setBlurRadius(4)
        shadow.setColor(QColor(0, 0, 0, 64))  # 64 = ~25% opacity
        self.setGraphicsEffect(shadow)
