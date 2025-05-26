from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame, QSizePolicy, QHBoxLayout
from PySide6.QtCore import Qt
from enum import Enum, auto
from ui.core.confiq import Colors
from PySide6.QtGui import QFontDatabase, QFont
import os

class Pivot(Enum):
    TOP_LEFT = auto()
    TOP_RIGHT = auto()
    BOTTOM_LEFT = auto()
    BOTTOM_RIGHT = auto()
    CENTER = auto()

class WindowModule(QWidget):
    NAVBAR_HEIGHT = 80

    def __init__(self, parent=None):
        super().__init__(parent)

        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)  # no outer margins
        self.mainLayout.setSpacing(0)
        self.setLayout(self.mainLayout)

        # Navbar container widget
        self.navbar = QWidget()
        self.navbar.setFixedHeight(self.NAVBAR_HEIGHT)
        self.navbar.setStyleSheet(f"background-color: {Colors.SECONDARY};")

        # Layout for navbar content (to add padding)
        navbarLayout = QHBoxLayout(self.navbar)
        navbarLayout.setContentsMargins(20, 0, 20, 0)  # left/right padding only
        navbarLayout.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)

        # Create label for app name
        self.navbarLabel = QLabel("NOTEPADGAMES")
        self.navbarLabel.setStyleSheet(f"""
            color: {Colors.FONT_PRIMARY};
            font-size: 32px;
        """)

        # Load the SUBURBIA font relative to this file location
        current_dir = os.path.dirname(os.path.abspath(__file__))
        font_path = os.path.join(current_dir, "assets", "fonts", "SUBURBIA.ttf")
        font_id = QFontDatabase.addApplicationFont(font_path)
        if font_id != -1:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            custom_font = QFont(font_family, 18)
            self.navbarLabel.setFont(custom_font)
        else:
            print("Failed to load Suburbia font")

        navbarLayout.addWidget(self.navbarLabel)

        # Content frame below navbar
        self.contentFrame = QFrame()
        self.contentFrame.setStyleSheet("background-color: transparent;")
        self.contentFrame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Add navbar and content to main layout
        self.mainLayout.addWidget(self.navbar)
        self.mainLayout.addWidget(self.contentFrame)

    def addChildWidget(self, widget: QWidget, x: int, y: int, pivot: Pivot = Pivot.CENTER):
        widget.setParent(self.contentFrame)

        # Adjust y by navbar height
        y -= self.NAVBAR_HEIGHT

        if pivot == Pivot.CENTER:
            pos_x = x - widget.width() // 2
            pos_y = y - widget.height() // 2
        elif pivot == Pivot.TOP_LEFT:
            pos_x = x
            pos_y = y
        elif pivot == Pivot.TOP_RIGHT:
            pos_x = x - widget.width()
            pos_y = y
        elif pivot == Pivot.BOTTOM_LEFT:
            pos_x = x
            pos_y = y - widget.height()
        elif pivot == Pivot.BOTTOM_RIGHT:
            pos_x = x - widget.width()
            pos_y = y - widget.height()
        else:
            pos_x = x
            pos_y = y

        widget.move(pos_x, pos_y)
        widget.show()
