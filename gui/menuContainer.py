from PySide6.QtWidgets import QFrame, QVBoxLayout
from PySide6.QtCore import Qt, QSize
from gui.core.confiq import Colors  # Use your color palette

class MenuContainer(QFrame):
    def __init__(self, parent=None, padding=50, background=Colors.SECONDARY):
        super().__init__(parent)
        self._fixed_width = 600
        self._fixed_height = 608

        self.setFixedSize(self._fixed_width, self._fixed_height)

        self.setStyleSheet(f"""
            QFrame {{
                background-color: {background};
                border-radius: 10px;
            }}
        """)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(padding, padding, padding, padding)
        self.layout.setSpacing(15)
        self.layout.setAlignment(Qt.AlignTop)

    def addWidget(self, widget):
        self.layout.addWidget(widget, alignment=Qt.AlignHCenter)

    def sizeHint(self) -> QSize:
        # Return the fixed size explicitly to ensure correct layout behavior
        return QSize(self._fixed_width, self._fixed_height)
