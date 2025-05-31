import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox, QPushButton, QHBoxLayout, QWidget
from PySide6.QtGui import QPainter, QPen, QColor
from PySide6.QtCore import Qt
from gui.board import Board
from gui.core.confiq import Colors, Constants
from gui.window import WindowModule, Pivot
from gui.signalBus import bus
from gui.gameController import GameController

class GridWindowModule(WindowModule):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.gridSpacing = getattr(Constants, 'GRID_SPACING', 20)
        self.gridColor = QColor(Colors.SECONDARY)
        self.gridColor.setAlpha(78)

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        pen = QPen(self.gridColor)
        pen.setWidth(1)
        painter.setPen(pen)
        width = self.width()
        height = self.height()
        x = 0
        while x < width:
            painter.drawLine(x, 0, x, height)
            x += self.gridSpacing
        y = 0
        while y < height:
            painter.drawLine(0, y, width, y)
            y += self.gridSpacing

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Stress Game Prototype")
        self.setFixedSize(Constants.BOARD_WIDTH, Constants.BOARD_HEIGHT)
        self.setStyleSheet(f"background-color: {Colors.TERTIARY};")
        bus.cellClicked.connect(self.handle_cell_click)
        self.windowModule = GridWindowModule()
        self.setCentralWidget(self.windowModule)
        self.controller = GameController(game_type="TicTacToe")
        self.board = Board(self.controller.get_board(), is_dame=False)
        self.windowModule.addChildWidget(self.board, Constants.BOARD_WIDTH / 2, Constants.BOARD_HEIGHT / 2 + 40, Pivot.CENTER)

        # Game selection UI
        # self.game_container = QWidget()
        # self.game_layout = QHBoxLayout(self.game_container)
        # self.game_layout.setSpacing(10)
        # self.game_layout.setContentsMargins(10, 10, 10, 10)
        # dame_button = QPushButton("Dame")
        # tictactoe_button = QPushButton("TicTacToe")
        # dame_button.setStyleSheet(f"background-color: {Colors.PRIMARY}; color: {Colors.FONT_PRIMARY};")
        # tictactoe_button.setStyleSheet(f"background-color: {Colors.PRIMARY}; color: {Colors.FONT_PRIMARY};")
        # dame_button.clicked.connect(lambda: self.set_game("Dame"))
        # tictactoe_button.clicked.connect(lambda: self.set_game("TicTacToe"))
        # self.game_layout.addWidget(dame_button)
        # self.game_layout.addWidget(tictactoe_button)
        # self.windowModule.addChildWidget(self.game_container, Constants.BOARD_WIDTH / 2, 50, Pivot.CENTER)

        # Difficulty selection UI
        # self.difficulty_container = QWidget()
        # self.difficulty_layout = QHBoxLayout(self.difficulty_container)
        # self.difficulty_layout.setSpacing(10)
        # self.difficulty_layout.setContentsMargins(10, 10, 10, 10)
        # easy_button = QPushButton("Easy")
        # medium_button = QPushButton("Medium")
        # hard_button = QPushButton("Hard")
        # easy_button.setStyleSheet(f"background-color: {Colors.PRIMARY}; color: {Colors.FONT_PRIMARY};")
        # medium_button.setStyleSheet(f"background-color: {Colors.PRIMARY}; color: {Colors.FONT_PRIMARY};")
        # hard_button.setStyleSheet(f"background-color: {Colors.PRIMARY}; color: {Colors.FONT_PRIMARY};")
        # easy_button.clicked.connect(lambda: self.controller.set_difficulty(1))
        # medium_button.clicked.connect(lambda: self.controller.set_difficulty(3))
        # hard_button.clicked.connect(lambda: self.controller.set_difficulty(5))
        # self.difficulty_layout.addWidget(easy_button)
        # self.difficulty_layout.addWidget(medium_button)
        # self.difficulty_layout.addWidget(hard_button)
        # self.windowModule.addChildWidget(self.difficulty_container, Constants.BOARD_WIDTH / 2, Constants.BOARD_HEIGHT - 50, Pivot.CENTER)

    def set_game(self, game_type):
        self.controller = GameController(game_type=game_type, difficulty=self.controller.difficulty)
        self.board = Board(self.controller.get_board(), is_dame=(game_type == "Dame"))
        self.windowModule.addChildWidget(self.board, Constants.BOARD_WIDTH / 2, Constants.BOARD_HEIGHT / 2 + 40, Pivot.CENTER)

    def handle_cell_click(self, position):
        possible_moves, win_status = self.controller.handle_cell_click(position)
        if possible_moves:
            self.board.show_possible_moves(possible_moves)
        else:
            self.board.update_board(self.controller.get_board())
        if win_status:
            self.show_game_over(win_status)

    def show_game_over(self, win_status):
        msg = "Human wins!" if win_status == "human_wins" else "AI wins!" if win_status == "ai_wins" else "Draw!"
        QMessageBox.information(self, "Game Over", msg)
        self.controller.reset_game()
        self.board.update_board(self.controller.get_board())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())