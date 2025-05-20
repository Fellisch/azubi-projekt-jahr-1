from PySide6.QtWidgets import QWidget, QGridLayout, QHBoxLayout, QVBoxLayout
from ui.board_cell import BoardCell

class Board(QWidget):
    def __init__(self):
        super().__init__()

        # Centering layout
        outer_layout = QVBoxLayout()
        outer_layout.addStretch()

        h_layout = QHBoxLayout()
        h_layout.addStretch()

        # The actual board layout
        board_layout = QGridLayout()
        board_layout.setSpacing(10)

        for row in range(6):
            for col in range(6):
                cell = BoardCell("x-symbol-svgrepo-com.svg")
                board_layout.addWidget(cell, row, col)

        h_layout.addLayout(board_layout)
        h_layout.addStretch()
        outer_layout.addLayout(h_layout)
        outer_layout.addStretch()

        self.setLayout(outer_layout)
