from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Signal, Qt
from gui.menuContainer import MenuContainer
from gui.customListWidget import CustomListWidget
from gui.myButton import MyButton, ButtonType
from gui.core.confiq import Colors

class GameSetupForm(MenuContainer):
    # Define signals
    playRequested = Signal(str, int)

    def __init__(self, parent=None):
        # MenuContainer default background is Colors.SECONDARY
        super().__init__(parent, padding=40)

        # Game Selection Label
        self.game_label = QLabel("Select Game:")
        self.game_label.setStyleSheet(f"color: {Colors.FONT_PRIMARY}; font-size: 16px;")
        self.addWidget(self.game_label)

        # Game List Widget (Custom Dropdown)
        self.game_list = CustomListWidget(["TicTacToe", "Dame"])
        self.addWidget(self.game_list)

        # Add some spacing after game selection
        self.layout.addSpacing(20)

        # Difficulty Selection Label
        self.difficulty_label = QLabel("Select Difficulty:")
        self.difficulty_label.setStyleSheet(f"color: {Colors.FONT_PRIMARY}; font-size: 16px;")
        self.addWidget(self.difficulty_label)

        # Difficulty List Widget (Custom Dropdown)
        self.difficulty_list = CustomListWidget(["Easy (1)", "Medium (3)", "Hard (5)"])
        self.addWidget(self.difficulty_list)

        # Set default selections
        self.game_list.set_selected_index(0)
        self.difficulty_list.set_selected_index(1)

        # Add spacing before the Play button
        self.layout.addSpacing(20)

        # Play Button - styled to match LoginForm's buttons
        self.play_button = MyButton(
            text='Play',
            button_type=ButtonType.NORMAL,
            borderWidth=0,
            fontSize=24,
            padding='15px 30px',
            background_color=Colors.PRIMARY,
            text_color=Colors.FONT_PRIMARY
        )
        self.addWidget(self.play_button)

        # Connect button to handler
        self.play_button.clicked.connect(self._on_play_clicked)

    def _on_play_clicked(self):
        game = self.game_list.get_selected_item_text()
        difficulty_text = self.difficulty_list.get_selected_item_text()
        difficulty_map = {
            "Easy (1)": 1,
            "Medium (3)": 3,
            "Hard (5)": 5
        }
        difficulty = difficulty_map.get(difficulty_text, 3)
        print(f"Play requested: Game: {game}, Difficulty: {difficulty}")
        self.playRequested.emit(game, difficulty)