from PySide6.QtWidgets import QWidget, QGridLayout
from ui.core.confiq import CellType, Constants, Colors
from ui.board_cell import BoardCell
from PySide6.QtCore import Qt

class Board(QWidget):
    def __init__(self):
        super().__init__()
        layout = QGridLayout(self)
        layout.setSpacing(Constants.CELL_SPACING)  # Uniform spacing between cells
        layout.setContentsMargins(Constants.CELL_SPACING, Constants.CELL_SPACING, Constants.CELL_SPACING, Constants.CELL_SPACING)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet(f"""
            background-color: {Colors.CTA_HOVER};
            border-radius: 10px;
        """)

        for row in range(6):
            for col in range(6):
                cellType = CellType.LIGHT if (row + col) % 2 == 0 else CellType.DARK
                cell = BoardCell(image='test.svg', cellType=cellType)

                # Apply background color per cell here
                backgroundColor = Colors.PRIMARY if cellType == CellType.LIGHT else Colors.SECONDARY
                layout.addWidget(cell, row, col)

        self.setLayout(layout)
        totalSize = Constants.CELL_SIZE * 6 + Constants.CELL_SPACING * 6  # 5 gaps between 6 cells
        self.setFixedSize(totalSize, totalSize)
