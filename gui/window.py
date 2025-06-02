from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame, QSizePolicy, QHBoxLayout
from PySide6.QtCore import Qt
from enum import Enum, auto
from gui.core.confiq import Colors
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
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(0)
        self.setLayout(self.mainLayout)

        # Navbar container widget
        self.navbar = QWidget()
        self.navbar.setFixedHeight(self.NAVBAR_HEIGHT)
        self.navbar.setStyleSheet(f"background-color: {Colors.SECONDARY};")

        navbarLayout = QHBoxLayout(self.navbar)
        navbarLayout.setContentsMargins(20, 0, 20, 0)
        navbarLayout.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)

        self.navbarLabel = QLabel("NOTEPADGAMES")
        self.navbarLabel.setStyleSheet(f"""
            color: {Colors.FONT_PRIMARY};
            font-size: 32px;
        """)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        font_path = os.path.join(current_dir, "assets", "fonts", "SUBURBIA.ttf")
        font_id = QFontDatabase.addApplicationFont(font_path)
        if font_id != -1:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            custom_font = QFont(font_family, 18) # Font size for navbar label
            self.navbarLabel.setFont(custom_font)
        else:
            print("Failed to load Suburbia font")
        navbarLayout.addWidget(self.navbarLabel)

        self.contentFrame = QFrame() # Children are added here
        self.contentFrame.setStyleSheet("background-color: transparent;")
        self.contentFrame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # It's crucial that contentFrame actually resizes and has a layout for reliable width/height
        # If contentFrame itself doesn't have a layout and items are just parented to it with move(),
        # its own size might be minimal. Let's give it a layout too for robustness, though children use move().
        contentFrameLayout = QVBoxLayout(self.contentFrame) # Basic layout for the frame itself
        contentFrameLayout.setContentsMargins(0,0,0,0)
        self.contentFrame.setLayout(contentFrameLayout)

        self.mainLayout.addWidget(self.navbar)
        self.mainLayout.addWidget(self.contentFrame)

    def addChildWidget(self, widget: QWidget, x: int, y: int, pivot: Pivot = Pivot.TOP_LEFT):
        # x and y are now ALWAYS relative to the contentFrame's top-left corner.
        # The caller is responsible for calculating these, including navbar offsets.
        widget.setParent(self.contentFrame)
        
        # Determine widget dimensions
        # Using fixed size from MenuContainer if widget is a MenuContainer (like LoginForm)
        # MenuContainer instances (like LoginForm) have a fixed size set internally.
        if hasattr(widget, '_fixed_width') and hasattr(widget, '_fixed_height'):
            width = widget._fixed_width
            height = widget._fixed_height
        else:
            widget.adjustSize() # Ensure sizeHint is up-to-date for other widgets
            hint = widget.sizeHint()
            width = hint.width() if hint.isValid() else widget.width()
            height = hint.height() if hint.isValid() else widget.height()
            # If still zero, let Qt decide or it might be an issue with widget's size policy
            if width == 0 or height == 0: # Last resort, make it visible at least
                print(f"Warning: Widget {widget} has zero dimensions. Forcing a small default.")
                width = max(width, 100) # Avoid division by zero, ensure some size
                height = max(height, 30)

        actual_pos_x = 0
        actual_pos_y = 0

        if pivot == Pivot.CENTER:
            # x, y are the desired center point within contentFrame for the widget
            actual_pos_x = x - width // 2
            actual_pos_y = y - height // 2
        elif pivot == Pivot.TOP_LEFT:
            actual_pos_x = x
            actual_pos_y = y
        elif pivot == Pivot.TOP_RIGHT:
            actual_pos_x = x - width
            actual_pos_y = y
        elif pivot == Pivot.BOTTOM_LEFT:
            actual_pos_x = x
            actual_pos_y = y - height
        elif pivot == Pivot.BOTTOM_RIGHT:
            actual_pos_x = x - width
            actual_pos_y = y - height
        else: # Default to top-left if pivot is not recognized
            actual_pos_x = x
            actual_pos_y = y

        widget.move(int(actual_pos_x), int(actual_pos_y))
        widget.show()

    def removeWidget(self, widget: QWidget):
        if widget and widget.parent() == self.contentFrame:
            widget.hide()
            widget.setParent(None)
            widget.deleteLater() # Ensure it's cleaned up
            print(f"DEBUG: Widget {widget} removed from WindowModule's contentFrame.")
        elif widget:
            print(f"DEBUG: Widget {widget} to be removed is not child of contentFrame or is None.")
        else:
            print("DEBUG: removeWidget called with None.")

    # Add a method to get the center of the contentFrame, useful for callers
    def getContentFrameCenter(self):
        # Ensure layout has taken effect by processing events or waiting if necessary,
        # but for most cases, accessing width/height directly should be fine after show.
        # However, during initial __init__, sizes might not be final.
        # This is best called after the window is shown or in a resizeEvent.
        center_x = self.contentFrame.width() / 2
        center_y = self.contentFrame.height() / 2
        return center_x, center_y
