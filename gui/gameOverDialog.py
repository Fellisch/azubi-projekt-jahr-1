from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QFontDatabase
import os
from database.DataQueries import getPlayersWithMostWins 
from gui.core.confiq import Colors, Constants

class GameOverOverlayWidget(QWidget):
    restartClicked = Signal()
    mainMenuClicked = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(400, 350)

        # --- Font Setup ---
        self.font_family = QFont().family() # Fallback default
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Assuming assets are in gui/assets/fonts relative to this file (gui/gameOverDialog.py)
        fonts_dir = os.path.join(current_dir, "assets", "fonts") 

        bold_font_filename = "JetBrainsMono-Bold.ttf"
        bold_font_path = os.path.join(fonts_dir, bold_font_filename)
        
        bold_font_id = QFontDatabase.addApplicationFont(bold_font_path)
        if bold_font_id != -1:
            loaded_bold_families = QFontDatabase.applicationFontFamilies(bold_font_id)
            if loaded_bold_families:
                self.font_family = loaded_bold_families[0]
        else:
            print(f"Warning: Failed to load font from {bold_font_path} in GameOverDialog")

        self.status_label_font = QFont(self.font_family, 20, QFont.Bold)
        self.title_font = QFont(self.font_family, 16, QFont.Bold)
        self.table_header_font = QFont(self.font_family, 14, QFont.Bold)
        self.table_content_font = QFont(self.font_family, 12, QFont.Bold)
        self.button_font = QFont(self.font_family, 16, QFont.Bold)

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
            QHeaderView {{ /* Horizontal header container */
                background-color: {Colors.PRIMARY}; /* Background of the entire header bar */
                border-top: 1px solid {Colors.SECONDARY};
                border-left: 1px solid {Colors.SECONDARY};
                border-right: 1px solid {Colors.SECONDARY};
                border-bottom: 1px solid {Colors.SECONDARY}; /* Line above table cells, completes the QHeaderView box */
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                border-bottom-left-radius: 0px; /* Flat bottom for QHeaderView itself */
                border-bottom-right-radius: 0px; /* Flat bottom for QHeaderView itself */
            }}
            QHeaderView::section {{ /* Individual header sections: Player, Wins, Losses */
                background-color: transparent; /* Make sections transparent to show QHeaderView's background */
                color: {Colors.FONT_PRIMARY};
                padding: 4px;
                border: none; /* Remove default borders for sections */
                /* border-bottom: 1px solid {Colors.SECONDARY}; Removed, QHeaderView handles its own bottom border */
                border-right: 1px solid {Colors.SECONDARY}; /* Vertical separator line */
            }}
            QHeaderView::section:last {{
                border-right: none; /* Last section should not have a right separator line */
            }}
            QPushButton {{
                background-color: {Colors.PRIMARY};
                color: {Colors.FONT_PRIMARY};
                border: 1px solid {Colors.SECONDARY};
                padding: 10px;
                /* font-size: 16px; */ /* Removed as font is set directly */
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
        self.statusLabel.setFont(self.status_label_font) 
        self.statusLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.statusLabel)

        # Scoreboard Title
        self.scoreboardTitleLabel = QLabel("Leaderboard")
        self.scoreboardTitleLabel.setFont(self.title_font) 
        self.scoreboardTitleLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.scoreboardTitleLabel)

        # Scoreboard Table
        self.scoreboardTable = QTableWidget()
        self.scoreboardTable.setColumnCount(3)
        self.scoreboardTable.setHorizontalHeaderLabels(["Player", "Wins", "Losses"])
        self.scoreboardTable.horizontalHeader().setFont(self.table_header_font) 
        self.scoreboardTable.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch) # Ensured this line is present
        self.scoreboardTable.verticalHeader().setVisible(False) 
        self.scoreboardTable.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.scoreboardTable.setMaximumHeight(150)
        layout.addWidget(self.scoreboardTable)

        # Buttons
        button_layout = QHBoxLayout()
        self.restartButton = QPushButton("Restart Game")
        self.mainMenuButton = QPushButton("Game Select")

        self.restartButton.setFont(self.button_font) 
        self.mainMenuButton.setFont(self.button_font) 

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
                        item.setFont(self.table_content_font)
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