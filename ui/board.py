from PySide6.QtWidgets import QWidget, QGridLayout
from ui.core.confiq import CellType
from ui.board_cell import BoardCell

class Board(QWidget):
    def __init__(self):
        super().__init__()
        layout = QGridLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        for row in range(6):
            for col in range(6):
                cellType = CellType.LIGHT if (row + col) % 2 == 0 else CellType.DARK
                cell = BoardCell(cellType=cellType)
                layout.addWidget(cell, row, col)

        self.setLayout(layout)