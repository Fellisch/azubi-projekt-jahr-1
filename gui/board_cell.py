import os
from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout, QGraphicsDropShadowEffect
from PySide6.QtGui import QPixmap, QColor, QMouseEvent
from PySide6.QtCore import Qt, QSize
from gui.core.confiq import Constants, Colors, CellType
from gui.signalBus import bus

PLAYER_PIECE_FILES = ['xMark.svg', 'oMark.svg', 'whitePiece.svg', 'blackPiece.svg']

class BoardCell(QFrame):
    def __init__(self, image=None, cellType=CellType.LIGHT, position=None):
        super().__init__()
        self.position = position
        self.setFixedSize(QSize(Constants.CELL_SIZE, Constants.CELL_SIZE))
        self.setCursor(Qt.PointingHandCursor)

        current_image_area_dimension = Constants.CELL_SIZE - 2 * Constants.PADDING
        self.target_image_dimension = int(current_image_area_dimension * 1.4)
        if self.target_image_dimension > Constants.CELL_SIZE:
            self.target_image_dimension = Constants.CELL_SIZE
        
        new_layout_padding = (Constants.CELL_SIZE - self.target_image_dimension) // 2
        if new_layout_padding < 0:
            new_layout_padding = 0

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
        layout.setContentsMargins(new_layout_padding, new_layout_padding + 5, new_layout_padding, new_layout_padding)
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

        image_filename = os.path.basename(imagePath)

        if image_filename in PLAYER_PIECE_FILES:
            scaledPixmap = pixmap.scaled(self.target_image_dimension, self.target_image_dimension, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        else:
            if pixmap.width() <= self.target_image_dimension and pixmap.height() <= self.target_image_dimension:
                scaledPixmap = pixmap
            else:
                scaledPixmap = pixmap.scaled(self.target_image_dimension, self.target_image_dimension, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        self.imageLabel.setPixmap(scaledPixmap)
        self.imageLabel.setFixedSize(scaledPixmap.size())
        self.imageLabel.setAlignment(Qt.AlignCenter)
        self.update()

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            bus.cellClicked.emit(self.position)
