from PySide6.QtWidgets import QLabel, QPushButton, QHBoxLayout, QWidget, QSizePolicy
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QFontDatabase, QFont
import os
from gui.menuContainer import MenuContainer
from gui.core.confiq import Colors

class GameSetupForm(MenuContainer):
    playRequested = Signal(str, int)

    def __init__(self, parent=None):
        super().__init__(parent, padding=40)

        self.font_family = QFont().family()

        current_dir = os.path.dirname(os.path.abspath(__file__))
        fonts_dir = os.path.join(current_dir, "assets", "fonts")

        bold_font_filename = "JetBrainsMono-Bold.ttf"
        bold_font_path = os.path.join(fonts_dir, bold_font_filename)
        bold_font_id = QFontDatabase.addApplicationFont(bold_font_path)
        if bold_font_id != -1:
            loaded_bold_families = QFontDatabase.applicationFontFamilies(bold_font_id)
            if loaded_bold_families:
                self.font_family = loaded_bold_families[0]
        
        self.default_font = QFont(self.font_family, 24, QFont.Bold)
        self.title_font = QFont(self.font_family, 40, QFont.Bold)
        self.start_button_font = QFont(self.font_family, 32, QFont.Bold)

        self.games = ["Dame", "TicTacToe"]
        self.difficulties = ["Easy", "Medium", "Hard"]
        self.selected_game = self.games[0]
        self.selected_difficulty = self.difficulties[1]

        self.gamemode_label = QLabel("Gamemode")
        self.gamemode_label.setFont(self.title_font)
        self.gamemode_label.setStyleSheet(f"color: {Colors.FONT_PRIMARY}; margin-bottom: 10px;")
        self.gamemode_label.setAlignment(Qt.AlignCenter)
        self.addWidget(self.gamemode_label)

        self.gamemode_buttons_layout = QHBoxLayout()
        self.gamemode_buttons_layout.setSpacing(0)
        self.gamemode_buttons_widget = QWidget()
        self.gamemode_buttons_widget.setLayout(self.gamemode_buttons_layout)
        self.game_button_group = []

        for game_name in self.games:
            button = QPushButton(game_name)
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
            button.clicked.connect(self.on_game_selected)
            self.gamemode_buttons_layout.addWidget(button)
            self.game_button_group.append(button)
        
        self.addWidget(self.gamemode_buttons_widget)
        self._update_game_button_styles()
        self.gamemode_buttons_widget.setFixedWidth(450)

        self.layout.addSpacing(30)

        self.difficulty_label = QLabel("Difficulty")
        self.difficulty_label.setFont(self.title_font)
        self.difficulty_label.setStyleSheet(f"color: {Colors.FONT_PRIMARY}; margin-bottom: 10px;")
        self.difficulty_label.setAlignment(Qt.AlignCenter)
        self.addWidget(self.difficulty_label)

        self.difficulty_buttons_layout = QHBoxLayout()
        self.difficulty_buttons_layout.setSpacing(0)
        self.difficulty_buttons_widget = QWidget()
        self.difficulty_buttons_widget.setLayout(self.difficulty_buttons_layout)
        self.difficulty_button_group = []

        for diff_name in self.difficulties:
            button = QPushButton(diff_name)
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
            button.clicked.connect(self.on_difficulty_selected)
            self.difficulty_buttons_layout.addWidget(button)
            self.difficulty_button_group.append(button)

        self.addWidget(self.difficulty_buttons_widget)
        self._update_difficulty_button_styles()
        self.difficulty_buttons_widget.setFixedWidth(450)

        game_group_height = self.gamemode_buttons_widget.sizeHint().height()
        diff_group_height = self.difficulty_buttons_widget.sizeHint().height()
        max_group_height = max(game_group_height, diff_group_height)
        
        if max_group_height > 0:
            self.gamemode_buttons_widget.setFixedHeight(max_group_height)
            self.difficulty_buttons_widget.setFixedHeight(max_group_height)
        
        self.layout.addSpacing(30) 

        self.play_button = QPushButton("Start")
        self.play_button.setFont(self.start_button_font)
        self.play_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {Colors.PRIMARY};
                color: {Colors.FONT_PRIMARY};
                padding: 14px 35px;
                border-radius: 10px; 
            }}
            QPushButton:hover {{
                background-color: {Colors.CTA_HOVER};
            }}
        """)
        target_start_button_width = 450
        target_start_button_height = 100
        self.play_button.setFixedWidth(target_start_button_width)
        self.play_button.setFixedHeight(target_start_button_height)

        self.addWidget(self.play_button)
        self.play_button.clicked.connect(self._on_play_clicked)

    def _get_button_style(self, is_selected: bool, index: int, total_buttons: int):
        bg_color = Colors.CTA_HOVER if is_selected else Colors.SECONDARY
        border_color = Colors.FONT_PRIMARY

        border_left_radius = "10px" if index == 0 else "0px"
        border_right_radius = "10px" if index == total_buttons - 1 else "0px"
        
        border_right_style = f"border-right: 1px solid {border_color};" if index == total_buttons - 1 else "border-right: none;"

        return f"""
            QPushButton {{
                background-color: {bg_color};
                color: {Colors.FONT_PRIMARY};
                border-top: 1px solid {border_color};
                border-bottom: 1px solid {border_color};
                border-left: 1px solid {border_color};
                {border_right_style}
                padding: 15px;
                border-top-left-radius: {border_left_radius};
                border-bottom-left-radius: {border_left_radius};
                border-top-right-radius: {border_right_radius};
                border-bottom-right-radius: {border_right_radius};
                min-width: 85px;
            }}
            QPushButton:hover {{
                background-color: {Colors.CTA_PRIMARY if not is_selected else Colors.CTA_HOVER};
            }}
        """

    def on_game_selected(self):
        sender_button = self.sender()
        self.selected_game = sender_button.text()
        self._update_game_button_styles()

    def _update_game_button_styles(self):
        total_buttons = len(self.game_button_group)
        for i, button in enumerate(self.game_button_group):
            is_selected = (button.text() == self.selected_game)
            button.setStyleSheet(self._get_button_style(is_selected, i, total_buttons))
            button.setFont(self.default_font)

    def on_difficulty_selected(self):
        sender_button = self.sender()
        self.selected_difficulty = sender_button.text()
        self._update_difficulty_button_styles()

    def _update_difficulty_button_styles(self):
        total_buttons = len(self.difficulty_button_group)
        for i, button in enumerate(self.difficulty_button_group):
            is_selected = (button.text() == self.selected_difficulty)
            button.setStyleSheet(self._get_button_style(is_selected, i, total_buttons))
            button.setFont(self.default_font)

    def _on_play_clicked(self):
        game = self.selected_game
        difficulty_text = self.selected_difficulty
        
        difficulty_map = {
            "Easy": 1,
            "Medium": 3,
            "Hard": 5
        }
        difficulty_value = difficulty_map.get(difficulty_text, 3)
        
        self.playRequested.emit(game, difficulty_value)