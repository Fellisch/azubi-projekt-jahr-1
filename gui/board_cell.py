import os
from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout, QGraphicsDropShadowEffect
from PySide6.QtGui import QPixmap, QColor, QMouseEvent
from PySide6.QtCore import Qt, QSize
from gui.core.confiq import Constants, Colors, CellType
from gui.signalBus import bus

class BoardCell(QFrame):
    def __init__(self, image=None, cellType=CellType.LIGHT, position=None):
        super().__init__()
        self.position = position
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

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setOffset(0, 4)
        shadow.setBlurRadius(4)
        shadow.setColor(QColor(0, 0, 0, 64))
        self.setGraphicsEffect(shadow)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(Constants.PADDING, Constants.PADDING, Constants.PADDING, Constants.PADDING)
        layout.setAlignment(Qt.AlignCenter)

        self.imageLabel = QLabel(self)
        layout.addWidget(self.imageLabel)

        self.setLayout(layout)

        if image:
            self.set_image(image)
        else:
            self.imageLabel.clear()

    def _find_image_path(self, root_dir, image_name):
        for dirpath, _, filenames in os.walk(root_dir):
            if image_name in filenames:
                return os.path.join(dirpath, image_name)
        return None

    def set_image(self, image):
        if not image:
            self.imageLabel.clear()
            return

        base_dir = os.path.dirname(os.path.abspath(__file__))
        assets_dir = os.path.join(base_dir, "assets")
        imagePath = self._find_image_path(assets_dir, image)
        if not imagePath:
            self.imageLabel.clear()
            return

        pixmap = QPixmap(imagePath)
        if pixmap.isNull():
            self.imageLabel.clear()
            return

        scaledSize = Constants.CELL_SIZE - 2 * Constants.PADDING
        scaledPixmap = pixmap.scaled(scaledSize, scaledSize, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.imageLabel.setPixmap(scaledPixmap)
        self.imageLabel.setFixedSize(scaledPixmap.size())
        self.imageLabel.setAlignment(Qt.AlignCenter)
        self.update()

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            bus.cellClicked.emit(self.position)
