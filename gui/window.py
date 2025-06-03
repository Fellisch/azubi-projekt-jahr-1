from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame, QSizePolicy, QHBoxLayout, QPushButton
from PySide6.QtCore import Qt, Signal, QSize
from enum import Enum, auto
from gui.core.confiq import Colors
from PySide6.QtGui import QFontDatabase, QFont, QIcon, QPixmap, QPainter
from PySide6.QtSvg import QSvgRenderer
import os

class Pivot(Enum):
    TOP_LEFT = auto()
    TOP_RIGHT = auto()
    BOTTOM_LEFT = auto()
    BOTTOM_RIGHT = auto()
    CENTER = auto()

class WindowModule(QWidget):
    NAVBAR_HEIGHT = 80
    homeButtonClicked = Signal()
    logoutButtonClicked = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(0)
        self.setLayout(self.mainLayout)

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
            custom_font = QFont(font_family, 18)
            self.navbarLabel.setFont(custom_font)
        else:
            pass # Failed to load Suburbia font
        navbarLayout.addWidget(self.navbarLabel)

        navbarLayout.addStretch(1)

        self.usernameLabel = QLabel()
        self.usernameLabel.setStyleSheet(f"""
            color: {Colors.FONT_PRIMARY};
            font-size: 20px;
            margin-right: 10px;
        """)
        if font_id != -1:
            font_family_suburbia = QFontDatabase.applicationFontFamilies(font_id)[0]
            username_font = QFont(font_family_suburbia, 20)
            self.usernameLabel.setFont(username_font)
        else:
            pass # Failed to apply Suburbia font to username label - font not loaded.
        navbarLayout.addWidget(self.usernameLabel)
        self.usernameLabel.hide()

        pm_size = 50 
        icon_display_size = 40
        current_dir_svg = os.path.dirname(os.path.abspath(__file__))

        self.logoutButton = QPushButton()
        logout_svg_path = os.path.join(current_dir_svg, "assets", "svg", "logoutButton.svg")
        
        logout_renderer = QSvgRenderer(logout_svg_path)
        logout_pixmap = QPixmap(pm_size, pm_size)
        logout_pixmap.fill(Qt.transparent)
        logout_painter = QPainter(logout_pixmap)
        logout_renderer.render(logout_painter)
        logout_painter.end()

        logout_icon = QIcon(logout_pixmap)
        self.logoutButton.setIcon(logout_icon)
        self.logoutButton.setIconSize(QSize(icon_display_size, icon_display_size))
        self.logoutButton.setFixedSize(QSize(pm_size, pm_size))
        self.logoutButton.setStyleSheet("QPushButton { background-color: transparent; border: none; margin-left: 5px; }")
        self.logoutButton.setCursor(Qt.PointingHandCursor)
        self.logoutButton.setToolTip("Logout")
        self.logoutButton.clicked.connect(self.logoutButtonClicked)
        navbarLayout.addWidget(self.logoutButton) 
        self.logoutButton.hide()

        self.homeButton = QPushButton()
        home_svg_path = os.path.join(current_dir_svg, "assets", "svg", "homeButton.svg")
        
        home_renderer = QSvgRenderer(home_svg_path)
        home_pixmap = QPixmap(pm_size, pm_size)
        home_pixmap.fill(Qt.transparent)
        home_painter = QPainter(home_pixmap)
        home_renderer.render(home_painter)
        home_painter.end()
        
        home_icon = QIcon(home_pixmap)
        self.homeButton.setIcon(home_icon)
        self.homeButton.setIconSize(QSize(icon_display_size, icon_display_size))
        self.homeButton.setFixedSize(QSize(pm_size, pm_size))
        self.homeButton.setStyleSheet("QPushButton { background-color: transparent; border: none; margin-left: 5px; }") 
        self.homeButton.setCursor(Qt.PointingHandCursor)
        self.homeButton.setToolTip("Go to Homepage")
        self.homeButton.clicked.connect(self.homeButtonClicked)
        navbarLayout.addWidget(self.homeButton) 
        self.homeButton.hide()

        self.contentFrame = QFrame()
        self.contentFrame.setStyleSheet("background-color: transparent;")
        self.contentFrame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        contentFrameLayout = QVBoxLayout(self.contentFrame)
        contentFrameLayout.setContentsMargins(0,0,0,0)
        self.contentFrame.setLayout(contentFrameLayout)

        self.mainLayout.addWidget(self.navbar)
        self.mainLayout.addWidget(self.contentFrame)

    def addChildWidget(self, widget: QWidget, x: int, y: int, pivot: Pivot = Pivot.TOP_LEFT):
        widget.setParent(self.contentFrame)
        
        if hasattr(widget, '_fixed_width') and hasattr(widget, '_fixed_height'):
            width = widget._fixed_width
            height = widget._fixed_height
        else:
            widget.adjustSize()
            hint = widget.sizeHint()
            width = hint.width() if hint.isValid() else widget.width()
            height = hint.height() if hint.isValid() else widget.height()
            if width == 0 or height == 0:
                width = max(width, 100)
                height = max(height, 30)

        actual_pos_x = 0
        actual_pos_y = 0

        if pivot == Pivot.CENTER:
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
        else:
            actual_pos_x = x
            actual_pos_y = y

        widget.move(int(actual_pos_x), int(actual_pos_y))
        widget.show()

    def showHomeButton(self):
        self.homeButton.show()

    def hideHomeButton(self):
        self.homeButton.hide()

    def update_username_display(self, username: str | None):
        if username:
            self.usernameLabel.setText(username)
            self.usernameLabel.show()
            self.logoutButton.show()
        else:
            self.usernameLabel.clear()
            self.usernameLabel.hide()
            self.logoutButton.hide()

    def removeWidget(self, widget: QWidget):
        if widget and widget.parent() == self.contentFrame:
            widget.hide()
            widget.setParent(None)
            widget.deleteLater()
        elif widget:
            pass
        else:
            pass

    def getContentFrameCenter(self):
        center_x = self.contentFrame.width() / 2
        center_y = self.contentFrame.height() / 2
        return center_x, center_y
