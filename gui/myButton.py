from PySide6.QtWidgets import QPushButton, QGraphicsDropShadowEffect
from PySide6.QtGui import QCursor, QFontDatabase, QFont, QColor
from PySide6.QtCore import Qt
from enum import Enum, auto
from gui.core.confiq import Colors
import os

class ButtonType(Enum):
    NORMAL = auto()
    LINK = auto()

class MyButton(QPushButton):
    def __init__(self, text, button_type=ButtonType.NORMAL, borderWidth=7, fontSize=18, parent=None, padding='8px 16px'):
        super().__init__(text, parent)

        font_path = os.path.join(os.path.dirname(__file__), "assets", "fonts", "SUBURBIA.ttf")
        font_id = QFontDatabase.addApplicationFont(font_path)
        if font_id != -1:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            self.setFont(QFont(font_family, fontSize))
        else:
            print("Failed to load Suburbia font")

        self.setCursor(QCursor(Qt.PointingHandCursor))

        if button_type == ButtonType.NORMAL:
            self.setStyleSheet(f"""
                QPushButton {{
                    color: {Colors.FONT_PRIMARY};
                    background-color: {Colors.TERTIARY};
                    border: {borderWidth}px solid {Colors.SECONDARY};
                    border-radius: 10px;
                    padding: {padding};
                }}
            """)
            shadow = QGraphicsDropShadowEffect(self)
            shadow.setOffset(0, 4)
            shadow.setBlurRadius(4)
            shadow.setColor(QColor(0, 0, 0, 64))
            self.setGraphicsEffect(shadow)
        elif button_type == ButtonType.LINK:
            self.setStyleSheet(f"""
                QPushButton {{
                    color: #0023C7;
                    background: transparent;
                    border: none;
                    padding: 0;
                }}
            """)
            self.setGraphicsEffect(None)
