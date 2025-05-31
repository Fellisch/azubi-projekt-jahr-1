from PySide6.QtWidgets import QWidget, QGridLayout
from PySide6.QtCore import Qt
from gui.core.confiq import CellType, Constants, Colors
from gui.board_cell import BoardCell

class Board(QWidget):
    def __init__(self, board_state, possible_moves=None):
        super().__init__()
        layout = QGridLayout(self)
        layout.setSpacing(Constants.CELL_SPACING)
        layout.setContentsMargins(Constants.CELL_SPACING, Constants.CELL_SPACING,
                                  Constants.CELL_SPACING, Constants.CELL_SPACING)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet(f"""
            background-color: {Colors.CTA_HOVER};
            border-radius: 10px;
        """)

        board_size = len(board_state)
        self.cells = {}
        self.board_state = board_state

        for row in range(board_size):
            for col in range(board_size):
                cellType = CellType.LIGHT if (row + col) % 2 == 0 else CellType.DARK

                # Determine which image to show
                image_path = None
                if possible_moves and (row, col) in possible_moves:
                    image_path = "test.svg"  # Your special possible move indicator image
                else:
                    piece = board_state[row][col]
                    if piece == 'W':
                        image_path = 'whitePiece.svg'
                    elif piece == 'B':
                        image_path = 'blackPiece.svg'

                cell = BoardCell(image=image_path, cellType=cellType, position=(row, col))
                layout.addWidget(cell, row, col)
                self.cells[(row, col)] = cell

        self.setLayout(layout)

        totalSize = Constants.CELL_SIZE * board_size + Constants.CELL_SPACING * (board_size + 1)
        self.setFixedSize(totalSize, totalSize)

    def show_possible_moves(self, possible_moves):
        # Reset cells to normal piece images
        for (row, col), cell in self.cells.items():
            piece = self.board_state[row][col]
            if piece == 'W':
                image = 'whitePiece.svg'
            elif piece == 'B':
                image = 'blackPiece.svg'
            else:
                image = None
            cell.set_image(image)
            cell.update()

        # Override images on possible moves cells
        for move in possible_moves:
            if isinstance(move, (list, tuple)) and len(move) >= 3:
                end_pos = tuple(move[2])
                if end_pos in self.cells:
                    self.cells[end_pos].set_image("test.svg")
                    self.cells[end_pos].update()



        self.update()
