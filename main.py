import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel
from PySide6.QtGui import QPainter, QPen, QColor
from PySide6.QtCore import Qt

from gui.board import Board
from gui.core.confiq import Colors, Constants
from gui.window import WindowModule, Pivot
from gui.rules import RulesToggle
from gui.imageWidget import ImageWidget
from gui.myButton import MyButton, ButtonType
from gui.menuContainer import MenuContainer
from gui.inputField import InputField
from gui.loginForm import LoginForm
from games.dame import Dame
from gui.signalBus import bus

class GridWindowModule(WindowModule):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Use constants or fallback values
        self.gridSpacing = getattr(Constants, 'GRID_SPACING', 20)
        self.gridColor = QColor(Colors.SECONDARY)  
        self.gridColor.setAlpha(78)  # 128 out of 255 = ~50% opacity

    def paintEvent(self, event):
        super().paintEvent(event)

        painter = QPainter(self)
        pen = QPen(self.gridColor)
        pen.setWidth(1)
        painter.setPen(pen)

        width = self.width()
        height = self.height()

        # Draw vertical lines
        x = 0
        while x < width:
            painter.drawLine(x, 0, x, height)
            x += self.gridSpacing

        # Draw horizontal lines
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
        self.game = Dame()

        # Create your widgets
        self.board = Board(self.game.board)

        # self.game.make_move()
        # Add widgets at specific positions inside windowModule
        self.windowModule.addChildWidget(self.board, Constants.BOARD_WIDTH / 2, Constants.BOARD_HEIGHT / 2 + 40, Pivot.CENTER)



        # self.rulesToggle = RulesToggle()
        # self.windowModule.addChildWidget(self.rulesToggle, Constants.BOARD_WIDTH - 30, Constants.BOARD_HEIGHT - 30, Pivot.BOTTOM_RIGHT)

        # self.windowModule.addChildWidget(self.image, Constants.BOARD_WIDTH / 2, Constants.BOARD_HEIGHT / 2 + 40, Pivot.CENTER)
        # btn = MyButton(text='LETS PLAY!',fontSize=46, padding='52px 70px')
        # self.windowModule.addChildWidget(btn, Constants.BOARD_WIDTH / 2,Constants.BOARD_HEIGHT / 2 + 250, Pivot.CENTER)
        # test = LoginForm()
        # self.windowModule.addChildWidget(test, Constants.BOARD_WIDTH / 2 ,Constants.BOARD_HEIGHT / 2, Pivot.CENTER)
    def handle_cell_click(self, position):
        possible_moves = self.game.get_possible_moves(position)
        self.board.show_possible_moves(possible_moves)
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
    