import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from ui.board import Board
from ui.core.confiq import Colors, Constants

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Stress Game Prototype")
        self.setFixedSize(Constants.BOARD_WIDTH, Constants.BOARD_HEIGHT)
        self.setStyleSheet(f"background-color: {Colors.BACKGROUND};")

        self.board = Board()
        self.setCentralWidget(self.board)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
