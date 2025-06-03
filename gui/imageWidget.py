from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
import os

DEBUGGING = False

class ImageWidget(QLabel):
    def __init__(self, image_name, scaled=True, max_size=None, alignment=Qt.AlignCenter, parent=None):
        super().__init__(parent)

        base_dir = os.path.dirname(os.path.abspath(__file__))
        assets_dir = os.path.join(base_dir, "assets")

        image_path = self._find_image_path(assets_dir, image_name)
        if not image_path:
            return

        pixmap = QPixmap(image_path)
        if pixmap.isNull():
            return

        if max_size:
            pixmap = pixmap.scaled(max_size[0], max_size[1], Qt.KeepAspectRatio, Qt.SmoothTransformation)

        self.setPixmap(pixmap)
        self.setAlignment(alignment)
        self.setScaledContents(scaled)

        if DEBUGGING:
            self.setStyleSheet("border: 2px solid red;")

    def _find_image_path(self, root_dir, image_name):
        for dirpath, _, filenames in os.walk(root_dir):
            if image_name in filenames:
                return os.path.join(dirpath, image_name)
        return None
