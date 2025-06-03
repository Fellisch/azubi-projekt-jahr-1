from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
from database.DataQueries import getPlayersWithMostWins 
from gui.core.confiq import Colors, Constants

class GameOverOverlayWidget(QWidget):
    restartClicked = Signal()
    mainMenuClicked = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(400, 350)
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {Colors.TERTIARY}; 
                color: {Colors.FONT_PRIMARY}; 
                border: 1px solid {Colors.SECONDARY}; 
                border-radius: 10px;
            }}
            QTableWidget {{
                background-color: {Colors.BACKGROUND_SECONDARY};
                border: none;
                gridline-color: {Colors.SECONDARY}; 
            }}
            QHeaderView::section {{
                background-color: {Colors.PRIMARY};
                color: {Colors.FONT_PRIMARY};
                padding: 4px;
                border: 1px solid {Colors.SECONDARY};
            }}
            QPushButton {{
                background-color: {Colors.PRIMARY};
                color: {Colors.FONT_PRIMARY};
                border: 1px solid {Colors.SECONDARY};
                padding: 10px;
                font-size: 16px;
                border-radius: 5px;
            }}
            QPushButton:hover {{
                background-color: {Colors.CTA_HOVER};
            }}
        """)

        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # Win Status Message
        self.statusLabel = QLabel("Game Over Placeholder")
        font = QFont()
        font.setPointSize(20)
        font.setBold(True)
        self.statusLabel.setFont(font)
        self.statusLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.statusLabel)

        # Scoreboard Title
        self.scoreboardTitleLabel = QLabel("Leaderboard")
        font_title = QFont()
        font_title.setPointSize(16)
        self.scoreboardTitleLabel.setFont(font_title)
        self.scoreboardTitleLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.scoreboardTitleLabel)

        # Scoreboard Table
        self.scoreboardTable = QTableWidget()
        self.scoreboardTable.setColumnCount(3)
        self.scoreboardTable.setHorizontalHeaderLabels(["Player", "Wins", "Losses"])
        self.scoreboardTable.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.scoreboardTable.verticalHeader().setVisible(False) # Hide row numbers
        self.scoreboardTable.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.scoreboardTable.setMaximumHeight(150)
        layout.addWidget(self.scoreboardTable)

        # Buttons
        button_layout = QHBoxLayout()
        self.restartButton = QPushButton("Restart Game")
        self.mainMenuButton = QPushButton("Game Select")

        self.restartButton.clicked.connect(self.restartClicked.emit)
        self.mainMenuButton.clicked.connect(self.mainMenuClicked.emit)

        button_layout.addWidget(self.restartButton)
        button_layout.addWidget(self.mainMenuButton)
        layout.addLayout(button_layout)
        
        self.hide() # Initially hidden

    def _populate_scoreboard(self, gamemode, difficulty):
        try:
            scores = getPlayersWithMostWins(gamemode=gamemode, difficulty=difficulty)
            scores.sort(key=lambda x: (x[1], -x[2]), reverse=True) 
            
            self.scoreboardTable.setRowCount(min(len(scores), 5))

            for i, (username, wins, losses) in enumerate(scores[:5]):
                self.scoreboardTable.setItem(i, 0, QTableWidgetItem(str(username)))
                self.scoreboardTable.setItem(i, 1, QTableWidgetItem(str(wins)))
                self.scoreboardTable.setItem(i, 2, QTableWidgetItem(str(losses)))
                for col in range(3):
                    item = self.scoreboardTable.item(i, col)
                    if item:
                        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

        except Exception as e:
            print(f"Error populating scoreboard in GameOverOverlayWidget: {e}")
            self.scoreboardTable.setRowCount(1)
            self.scoreboardTable.setColumnCount(1)
            error_item = QTableWidgetItem("Could not load scoreboard.")
            error_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.scoreboardTable.setItem(0, 0, error_item)
            self.scoreboardTable.setSpan(0, 0, 1, 1) # Span across the single column
            # Ensure a reset for next time if needed
            # self.scoreboardTable.setColumnCount(3) 
            # self.scoreboardTable.setHorizontalHeaderLabels(["Player", "Wins", "Losses"])


    def update_contents(self, status_message, gamemode_int, difficulty_int):
        self.statusLabel.setText(status_message)
         # Reset table before populating
        self.scoreboardTable.clearContents()
        self.scoreboardTable.setRowCount(0)
        self.scoreboardTable.setColumnCount(3) 
        self.scoreboardTable.setHorizontalHeaderLabels(["Player", "Wins", "Losses"])
        self._populate_scoreboard(gamemode_int, difficulty_int)


if __name__ == '__main__':
    # For testing the dialog independently
    from PySide6.QtWidgets import QApplication
    import sys

    # Mock data and parameters for testing
    mock_win_status = "You Won!"
    mock_gamemode = 1 # Example gamemode int
    mock_difficulty = 2 # Example difficulty int

    # Mocking the database function for standalone testing
    def mock_getPlayersWithMostWins_for_test(gamemode, difficulty): # Renamed for clarity
        print(f"Mock mock_getPlayersWithMostWins_for_test called with gamemode={{gamemode}}, difficulty={{difficulty}}")
        return [
            ("PlayerA", 10, 2),
            ("PlayerB", 8, 1),
            ("PlayerC", 12, 5),
            ("PlayerD", 8, 3),
            ("PlayerE", 9, 0),
            ("PlayerF", 10, 1),
        ]
    
    app = QApplication(sys.argv)
    # Pass the mock function to the dialog
    dialog = GameOverOverlayWidget()
    
    def on_restart():
        print("Restart chosen")
    def on_main_menu():
        print("Main Menu chosen")

    dialog.restartClicked.connect(on_restart)
    dialog.mainMenuClicked.connect(on_main_menu)
    
    dialog.show()
    
    exit_code = app.exec()
    
    sys.exit(exit_code) 