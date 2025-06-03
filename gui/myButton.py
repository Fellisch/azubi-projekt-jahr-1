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
    def __init__(self, text, button_type=ButtonType.NORMAL, borderWidth=7, fontSize=18, parent=None, padding='8px 16px',
                 background_color=None, border_color=None, text_color=Colors.FONT_PRIMARY, font='jbmono'):
        super().__init__(text, parent)

        if font == 'jbmono':
            font_path = os.path.join(os.path.dirname(__file__), "assets", "fonts", "JetBrainsMono-Bold.ttf")
        elif font == 'suburbia':
            font_path = os.path.join(os.path.dirname(__file__), "assets", "fonts", "SUBURBIA.ttf")
        else:
            raise ValueError("Invalid font type")

        font_id = QFontDatabase.addApplicationFont(font_path)
        if font_id != -1:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            self.setFont(QFont(font_family, fontSize))
        else:
            print("Failed to load font")

        self.setCursor(QCursor(Qt.PointingHandCursor))

        if button_type == ButtonType.NORMAL:
            # Use provided colors or default
            bg_color = background_color if background_color else Colors.TERTIARY
            final_border_color = border_color if border_color else Colors.SECONDARY
            final_text_color = text_color # Already has a default

            self.setStyleSheet(f"""
                QPushButton {{
                    color: {final_text_color};
                    background-color: {bg_color};
                    border: {borderWidth}px solid {final_border_color};
                    border-radius: 10px;
                    padding: {padding};
                }}
            """)
            if borderWidth > 0: # Only add shadow if there's a border that implies elevation
                shadow = QGraphicsDropShadowEffect(self)
                shadow.setOffset(0, 4)
                shadow.setBlurRadius(4)
                shadow.setColor(QColor(0, 0, 0, 64))
                self.setGraphicsEffect(shadow)
            else:
                self.setGraphicsEffect(None) # No shadow if no border width

        elif button_type == ButtonType.LINK:
            link_text_color = text_color if text_color != Colors.FONT_PRIMARY else "#0023C7" # Default to blue if not overridden
            self.setStyleSheet(f"""
                QPushButton {{
                    color: {link_text_color};
                    background: transparent;
                    border: none;
                    padding: 0;
                    text-decoration: underline;
                }}
                QPushButton:hover {{
                    color: {Colors.CTA_HOVER}; /* Or another hover color for links */
                }}
            """)
            self.setGraphicsEffect(None)
