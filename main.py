import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtGui import QPainter, QPen, QColor
from PySide6.QtCore import Qt

from ui.board import Board
from ui.core.confiq import Colors, Constants
from ui.window import WindowModule, Pivot
from ui.rules import RulesToggle
from ui.imageWidget import ImageWidget
from ui.myButton import MyButton

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

        self.windowModule = GridWindowModule()
        self.setCentralWidget(self.windowModule)

        # # Create your widgets
        # self.board = Board()

        # # Add widgets at specific positions inside windowModule
        # self.windowModule.addChildWidget(self.board, Constants.BOARD_WIDTH / 2, Constants.BOARD_HEIGHT / 2 + 40, Pivot.CENTER)

        # self.rulesToggle = RulesToggle()
        # self.windowModule.addChildWidget(self.rulesToggle, Constants.BOARD_WIDTH - 30, Constants.BOARD_HEIGHT - 30, Pivot.BOTTOM_RIGHT)

        self.image = ImageWidget("notepad.svg", max_size=(300, 300))
        # self.windowModule.addChildWidget(self.image, Constants.BOARD_WIDTH / 2, Constants.BOARD_HEIGHT / 2 + 40, Pivot.CENTER)
        self.windowModule.addChildWidget(self.image, Constants.BOARD_WIDTH / 2,Constants.BOARD_HEIGHT / 2, Pivot.CENTER)
        btn = MyButton(text='LETS PLAY!',fontSize=46, padding='52px 70px')
        self.windowModule.addChildWidget(btn, Constants.BOARD_WIDTH / 2,Constants.BOARD_HEIGHT / 2 + 250, Pivot.CENTER)

        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
