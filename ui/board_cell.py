import os
from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QSize
from ui.core.confiq import Constants, Colors, CellType

class BoardCell(QFrame):
    def __init__(self, image=None, cellType=CellType.LIGHT):
        super().__init__()
        self.setFixedSize(QSize(Constants.CELL_SIZE, Constants.CELL_SIZE))
        self.setFrameStyle(QFrame.Box | QFrame.Plain)
        self.setLineWidth(Constants.BORDER_WIDTH)
        backgroundColor = Colors.CELL_BG_LIGHT if cellType == CellType.LIGHT else Colors.CELL_BG_DARK
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {backgroundColor};
                border: {Constants.BORDER_WIDTH}px solid {Colors.PRIMARY};
            }}
            QLabel {{
                border: none;
                background: transparent;
            }}
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(Constants.PADDING, Constants.PADDING, Constants.PADDING, Constants.PADDING)
        layout.setAlignment(Qt.AlignCenter)

        if image:
            imagePath = os.path.join(os.path.dirname(__file__), "assets", image)
            pixmap = QPixmap(imagePath)
            if pixmap.isNull():
                print(f"Failed to load image: {imagePath}")
                return

            scaledSize = Constants.CELL_SIZE - 2 * (Constants.PADDING + Constants.BORDER_WIDTH)
            scaledPixmap = pixmap.scaled(scaledSize, scaledSize, Qt.KeepAspectRatio, Qt.SmoothTransformation)

            self.imageLabel = QLabel(self)
            self.imageLabel.setPixmap(scaledPixmap)
            self.imageLabel.setFixedSize(scaledPixmap.size())
            self.imageLabel.setAlignment(Qt.AlignCenter)
            layout.addWidget(self.imageLabel)

        self.setLayout(layout)
