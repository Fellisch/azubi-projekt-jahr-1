import os
from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QSize

CELL_SIZE = 60
PADDING = 20
BORDER_WIDTH = 3

class BoardCell(QFrame):
    def __init__(self, image_filename=None):
        super().__init__()
        # Set fixed size for the cell
        self.setFixedSize(QSize(CELL_SIZE, CELL_SIZE))
        # Use QFrame's built-in border
        self.setFrameStyle(QFrame.Box | QFrame.Plain)
        self.setLineWidth(BORDER_WIDTH)
        # Apply stylesheet for background and rounded corners
        self.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 8px;
                border: 3px solid #2c3e50;
            }
            QLabel {
                border: none;
                background: transparent;
            }
        """)

        # Create layout to center the image
        layout = QVBoxLayout(self)
        layout.setContentsMargins(PADDING, PADDING, PADDING, PADDING)
        layout.setAlignment(Qt.AlignCenter)

        if image_filename:
            # Load the image
            image_path = os.path.join(os.path.dirname(__file__), "assets", image_filename)
            pixmap = QPixmap(image_path)
            if pixmap.isNull():
                print(f"Failed to load image: {image_path}")
                return

            # Scale the image to fit within the cell, accounting for padding and border
            scaled_size = CELL_SIZE - 2 * (PADDING + BORDER_WIDTH)
            scaled_pixmap = pixmap.scaled(
                scaled_size,
                scaled_size,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )

            # Create and configure the image label
            self.image_label = QLabel(self)
            self.image_label.setPixmap(scaled_pixmap)
            self.image_label.setFixedSize(scaled_pixmap.size())
            self.image_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(self.image_label)

        self.setLayout(layout)