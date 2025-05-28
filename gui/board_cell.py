import os
from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout, QGraphicsDropShadowEffect
from PySide6.QtGui import QPixmap, QColor
from PySide6.QtCore import Qt, QSize
from ui.core.confiq import Constants, Colors, CellType

class BoardCell(QFrame):
    def __init__(self, image=None, cellType=CellType.LIGHT):
        super().__init__()
        self.setFixedSize(QSize(Constants.CELL_SIZE, Constants.CELL_SIZE))
        self.setCursor(Qt.PointingHandCursor)

        backgroundColor = Colors.PRIMARY if cellType == CellType.LIGHT else Colors.SECONDARY
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {backgroundColor};
                border-radius: 10px;
            }}
            QLabel {{
                border: none;
                background: transparent;
            }}
        """)

        # Add shadow effect (box-shadow: 0px 4px 4px 0px #00000040)
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setOffset(0, 4)                      # vertical offset 4px, horizontal 0
        shadow.setBlurRadius(4)                     # blur radius 4px
        shadow.setColor(QColor(0, 0, 0, 64))       # black color with ~25% opacity (64 out of 255)
        self.setGraphicsEffect(shadow)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(Constants.PADDING, Constants.PADDING, Constants.PADDING, Constants.PADDING)
        layout.setAlignment(Qt.AlignCenter)

        if image:
            imagePath = os.path.join(os.path.dirname(__file__), "assets", image)
            pixmap = QPixmap(imagePath)
            if pixmap.isNull():
                print(f"Failed to load image: {imagePath}")
                return

            scaledSize = Constants.CELL_SIZE - 2 * (Constants.PADDING)
            scaledPixmap = pixmap.scaled(scaledSize, scaledSize, Qt.KeepAspectRatio, Qt.SmoothTransformation)

            self.imageLabel = QLabel(self)
            self.imageLabel.setPixmap(scaledPixmap)
            self.imageLabel.setFixedSize(scaledPixmap.size())
            self.imageLabel.setAlignment(Qt.AlignCenter)
            layout.addWidget(self.imageLabel)

        self.setLayout(layout)
