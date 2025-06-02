from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
from database.DataQueries import getPlayersWithMostWins # Assuming this path is correct relative to project root
from gui.core.confiq import Colors

class GameOverDialog(QDialog):
    restartClicked = Signal()
    mainMenuClicked = Signal()

    def __init__(self, win_status_message, gamemode_int, difficulty_int, parent=None, data_fetch_func=None):
        super().__init__(parent)
        self.setWindowTitle("Game Over")
        self.setModal(True) # Make it a modal dialog
        self.setStyleSheet(f"background-color: {Colors.TERTIARY}; color: {Colors.FONT_PRIMARY};")

        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # Win Status Message
        self.statusLabel = QLabel(win_status_message)
        font = QFont()
        font.setPointSize(20)
        font.setBold(True)
        self.statusLabel.setFont(font)
        self.statusLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.statusLabel)

        # Scoreboard Title
        self.scoreboardTitleLabel = QLabel("Scoreboard")
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
        self.scoreboardTable.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers) # Read-only
        self.scoreboardTable.setMaximumHeight(150) # Limit height
        
        # Use the provided data_fetch_func or the default imported one
        self._data_fetch_func = data_fetch_func if data_fetch_func else getPlayersWithMostWins
        self.populate_scoreboard(gamemode_int, difficulty_int)
        layout.addWidget(self.scoreboardTable)

        # Buttons
        button_layout = QHBoxLayout()
        self.restartButton = QPushButton("Restart Game")
        self.gameMenuButton = QPushButton("Game Select")

        # Corrected button_style definition
        raw_button_style = '''
            QPushButton {{
                background-color: {primary_color};
                color: {font_primary_color};
                border: 1px solid {secondary_color};
                padding: 10px;
                font-size: 16px;
                border-radius: 5px;
            }}
            QPushButton:hover {{
                background-color: {cta_hover_color};
            }}
        '''
        button_style = raw_button_style.format(
            primary_color=Colors.PRIMARY,
            font_primary_color=Colors.FONT_PRIMARY,
            secondary_color=Colors.SECONDARY,
            cta_hover_color=Colors.CTA_HOVER
        )

        self.restartButton.setStyleSheet(button_style)
        self.gameMenuButton.setStyleSheet(button_style)

        self.restartButton.clicked.connect(self.handle_restart)
        self.gameMenuButton.clicked.connect(self.handle_main_menu)

        button_layout.addWidget(self.restartButton)
        button_layout.addWidget(self.gameMenuButton)
        layout.addLayout(button_layout)

        self.setFixedSize(400, 350)


    def populate_scoreboard(self, gamemode, difficulty):
        try:
            # Assuming gamemode and difficulty are already integers.
            scores = self._data_fetch_func(gamemode=gamemode, difficulty=difficulty) # Call via self._data_fetch_func
            
            # Sort by wins (descending), then by losses (ascending)
            scores.sort(key=lambda x: (x[1], -x[2]), reverse=True) 
            
            self.scoreboardTable.setRowCount(min(len(scores), 5)) # Show top 5 or fewer

            for i, (username, wins, losses) in enumerate(scores[:5]):
                self.scoreboardTable.setItem(i, 0, QTableWidgetItem(str(username)))
                self.scoreboardTable.setItem(i, 1, QTableWidgetItem(str(wins)))
                self.scoreboardTable.setItem(i, 2, QTableWidgetItem(str(losses)))
                for col in range(3):
                    self.scoreboardTable.item(i, col).setTextAlignment(Qt.AlignmentFlag.AlignCenter)

        except Exception as e:
            print(f"Error populating scoreboard: {e}")
            # Optionally, display an error in the dialog
            self.scoreboardTable.setRowCount(1)
            item = QTableWidgetItem("Could not load scoreboard.")
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.scoreboardTable.setItem(0, 0, item)
            self.scoreboardTable.setSpan(0,0,1,3)


    def handle_restart(self):
        self.restartClicked.emit()
        self.accept() # Close the dialog

    def handle_main_menu(self):
        self.mainMenuClicked.emit()
        self.accept() # Close the dialog

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
    dialog = GameOverDialog(mock_win_status, mock_gamemode, mock_difficulty, data_fetch_func=mock_getPlayersWithMostWins_for_test)
    
    def on_restart():
        print("Restart chosen")
    def on_main_menu():
        print("Main Menu chosen")

    dialog.restartClicked.connect(on_restart)
    dialog.mainMenuClicked.connect(on_main_menu)
    
    dialog.show()
    
    exit_code = app.exec()
    
    sys.exit(exit_code) 