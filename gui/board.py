from PySide6.QtWidgets import QWidget, QGridLayout
from PySide6.QtCore import Qt
from gui.core.confiq import CellType, Constants, Colors
from gui.board_cell import BoardCell

class Board(QWidget):
    def __init__(self, board_state, is_dame=False, possible_moves=None):
        super().__init__()
        self.is_dame = is_dame
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
            visual_row = board_size - 1 - row if is_dame else row
            for col in range(board_size):
                cellType = CellType.LIGHT if (row + col) % 2 == 0 else CellType.DARK
                image_path = None
                if possible_moves and (row, col) in possible_moves:
                    image_path = "test.svg"
                else:
                    piece = board_state[row][col]
                    if is_dame:
                        if piece == 'W':
                            image_path = 'whitePiece.svg'
                        elif piece == 'B':
                            image_path = 'blackPiece.svg'
                    else:
                        if piece == 'X':
                            image_path = 'test.svg'
                        elif piece == 'O':
                            image_path = 'test.svg'
                cell = BoardCell(image=image_path, cellType=cellType, position=(row, col))
                layout.addWidget(cell, visual_row, col)
                self.cells[(row, col)] = cell

        self.setLayout(layout)
        totalSize = Constants.CELL_SIZE * board_size + Constants.CELL_SPACING * (board_size + 1)
        self.setFixedSize(totalSize, totalSize)

    def show_possible_moves(self, possible_moves):
        for (row, col), cell in self.cells.items():
            piece = self.board_state[row][col]
            if self.is_dame:
                image = 'whitePiece.svg' if piece == 'W' else 'blackPiece.svg' if piece == 'B' else None
            else:
                image = 'xMark.svg' if piece == 'X' else 'oMark.svg' if piece == 'O' else None
            cell.set_image(image)
            cell.update()

        for move in possible_moves or []:
            if isinstance(move, (list, tuple)) and len(move) >= 3:
                end_pos = tuple(move[2])
                if end_pos in self.cells:
                    self.cells[end_pos].set_image("test.svg")
                    self.cells[end_pos].update()
            elif isinstance(move, tuple) and len(move) == 2:
                if move in self.cells:
                    self.cells[move].set_image("test.svg")
                    self.cells[move].update()

    def update_board(self, new_board_state):
        self.board_state = new_board_state
        for row in range(len(new_board_state)):
            for col in range(len(new_board_state[row])):
                piece = new_board_state[row][col]
                if self.is_dame:
                    image = 'whitePiece.svg' if piece == 'W' else 'blackPiece.svg' if piece == 'B' else None
                else:
                    image = 'test.svg' if piece == 'X' else 'test.svg' if piece == 'O' else None
                self.cells[(row, col)].set_image(image)
        self.update()