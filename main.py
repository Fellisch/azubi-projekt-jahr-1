import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QGraphicsColorizeEffect
from PySide6.QtGui import QPainter, QPen, QColor, QFont
from PySide6.QtCore import Qt, QTimer
from gui.board import Board
from gui.core.confiq import Colors, Constants
from gui.window import WindowModule, Pivot
from gui.signalBus import bus
from gui.gameController import GameController
from gui.loginForm import LoginForm
from gui.signupForm import SignupForm
from gui.gameSetupForm import GameSetupForm
from database.DataQueries import increaseWins, increaseLosses, getPlayersWithMostWins # Added getPlayersWithMostWins
from gui.rules import RulesToggle  # Import RulesToggle
from gui.myButton import MyButton  # Import MyButton
from gui.imageWidget import ImageWidget  # Import ImageWidget
from gui.gameOverDialog import GameOverOverlayWidget # Import the new overlay widget

GAMEMODE_MAP = {
    "TicTacToe": 1,
    "Dame": 2
}

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
        for x in range(0, width, self.gridSpacing):
            painter.drawLine(x, 0, x, height)
        for y in range(0, height, self.gridSpacing):
            painter.drawLine(0, y, width, y)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Stress Game Prototype")
        self.setFixedSize(Constants.BOARD_WIDTH, Constants.BOARD_HEIGHT)
        self.setStyleSheet(f"background-color: {Colors.TERTIARY};")

        self.windowModule = GridWindowModule()
        self.setCentralWidget(self.windowModule)

        self.controller = None
        self.board = None
        self.current_difficulty = 3
        self.current_user_id = None
        self.rules_toggle = None
        self.image = None
        self.play_button = None
        self.is_ai_thinking = False
        
        self.game_over_overlay = None # Initialize for the new overlay widget

        self._setup_homepage()
        self._setup_login_form()
        self._setup_signup_form()
        self._setup_game_selection_ui()
        self._setup_game_over_overlay() # NEW: Setup the overlay instance

        bus.cellClicked.connect(self.handle_cell_click)

        self.login_form.loginAttempt.connect(self._handle_user_login_attempt)
        self.login_form.guestAccessRequested.connect(self._handle_guest_access)
        self.login_form.signupRequested.connect(self._show_signup_view)

        self.signup_form.signupAttempted.connect(self._handle_user_signup_attempt)
        self.signup_form.loginLinkActivated.connect(self._show_login_view)
        self.signup_form.guestAccessRequested.connect(self._handle_guest_access)

        self.play_button.clicked.connect(self._show_login_view)  # Connect play button to login view

        self._show_homepage()  # Show homepage initially

    def _setup_homepage(self):
        # Setup ImageWidget with notepad.svg
        self.image = ImageWidget("notepad.svg", max_size=(300, 300))
        self.windowModule.addChildWidget(
            self.image,
            Constants.BOARD_WIDTH / 2,
            Constants.BOARD_HEIGHT / 2 - 150,
            Pivot.CENTER
        )

        # Setup "LETS PLAY!" button
        self.play_button = MyButton(text='LETS PLAY!', fontSize=46, padding='52px 70px')
        self.windowModule.addChildWidget(
            self.play_button,
            Constants.BOARD_WIDTH / 2,
            Constants.BOARD_HEIGHT / 2 + 100,
            Pivot.CENTER
        )

    def _setup_login_form(self):
        self.login_form = LoginForm()
        self.windowModule.addChildWidget(
            self.login_form,
            Constants.BOARD_WIDTH / 2,
            (Constants.BOARD_HEIGHT - self.windowModule.NAVBAR_HEIGHT) / 2,
            Pivot.CENTER
        )

    def _setup_signup_form(self):
        self.signup_form = SignupForm()
        self.windowModule.addChildWidget(
            self.signup_form,
            Constants.BOARD_WIDTH / 2,
            (Constants.BOARD_HEIGHT - self.windowModule.NAVBAR_HEIGHT) / 2,
            Pivot.CENTER
        )

    def _setup_game_selection_ui(self):
        self.game_setup_form = GameSetupForm()
        self.windowModule.addChildWidget(
            self.game_setup_form,
            Constants.BOARD_WIDTH / 2,
            (Constants.BOARD_HEIGHT - self.windowModule.NAVBAR_HEIGHT) / 2,
            Pivot.CENTER
        )
        self.game_setup_form.playRequested.connect(self._handle_game_start)

    def _setup_rules_toggle(self):
        if self.rules_toggle:
            self.windowModule.removeWidget(self.rules_toggle)
        if self.controller and self.controller.game:
            self.rules_toggle = RulesToggle(game=self.controller.game, violated_ids=[])
            self.windowModule.addChildWidget(
                self.rules_toggle,
                Constants.BOARD_WIDTH - 125,
                Constants.BOARD_HEIGHT - 157.5 - self.windowModule.NAVBAR_HEIGHT,
                Pivot.CENTER
            )
        else:
            self.rules_toggle = None

    def _setup_game_over_overlay(self):
        self.game_over_overlay = GameOverOverlayWidget(parent=self.windowModule) 
        
        # Add the widget to contentFrame. Actual positioning will be done when shown.
        # Pass (0,0) and TOP_LEFT as initial placement as it will be moved before showing.
        self.windowModule.addChildWidget(
            self.game_over_overlay, 
            0, 
            0, 
            Pivot.TOP_LEFT 
        )

        self.game_over_overlay.restartClicked.connect(self._handle_restart_from_overlay)
        self.game_over_overlay.mainMenuClicked.connect(self._handle_main_menu_from_overlay)
        # GameOverOverlayWidget hides itself in its __init__

    def _handle_restart_from_overlay(self):
        self.game_over_overlay.hide()
        if self.board and hasattr(self, 'board_colorize_effect') and self.board.graphicsEffect() == self.board_colorize_effect:
            self.board.setGraphicsEffect(None)
            del self.board_colorize_effect
        self.handle_restart_game()

    def _handle_main_menu_from_overlay(self):
        self.game_over_overlay.hide()
        if self.board and hasattr(self, 'board_colorize_effect') and self.board.graphicsEffect() == self.board_colorize_effect:
            self.board.setGraphicsEffect(None)
            del self.board_colorize_effect
        self._show_game_selection_view()

    def _show_homepage(self):
        self.image.show()
        self.play_button.show()
        self.login_form.hide()
        self.signup_form.hide()
        self.game_setup_form.hide()
        if self.board: self.board.hide()
        if self.rules_toggle: self.rules_toggle.hide()
        if self.game_over_overlay: self.game_over_overlay.hide() # Ensure overlay is hidden

    def _show_login_view(self):
        self.image.hide()
        self.play_button.hide()
        self.login_form.show()
        self.signup_form.hide()
        self.game_setup_form.hide()
        if self.board: self.board.hide()
        if self.rules_toggle: self.rules_toggle.hide()
        if self.game_over_overlay: self.game_over_overlay.hide()

    def _show_signup_view(self):
        self.image.hide()
        self.play_button.hide()
        self.login_form.hide()
        self.signup_form.show()
        self.signup_form.clear_error()
        self.game_setup_form.hide()
        if self.board: self.board.hide()
        if self.rules_toggle: self.rules_toggle.hide()
        if self.game_over_overlay: self.game_over_overlay.hide()

    def _show_game_selection_view(self):
        self.image.hide()
        self.play_button.hide()
        self.login_form.hide()
        self.signup_form.hide()
        self.game_setup_form.show()
        if self.board:
            self.windowModule.removeWidget(self.board)
            self.board = None
        if self.controller:
            self.controller = None
        if self.rules_toggle: self.rules_toggle.hide()
        if self.game_over_overlay: self.game_over_overlay.hide()

    def _show_board_view(self):
        self.image.hide()
        self.play_button.hide()
        self.login_form.hide()
        self.signup_form.hide()
        self.game_setup_form.hide()
        if self.board: self.board.show()
        self._setup_rules_toggle()
        if self.rules_toggle:
            self.rules_toggle.show()
            self._update_violated_rules()
        if self.game_over_overlay: self.game_over_overlay.hide()

    def _handle_guest_access(self):
        print("Guest access requested. Showing game selection.")
        self.current_user_id = None
        self._show_game_selection_view()

    def _handle_user_login_attempt(self, username, password):
        print(f"Attempting to log in user: {username}")
        from database.auth import login_user
        auth_result = login_user(username, password)

        if auth_result.code is None:
            self.current_user_id = auth_result.id
            print(f"User '{username}' (ID: {self.current_user_id}) logged in successfully.")
            self.login_form.clear_error()
            self._show_game_selection_view()
        else:
            self.current_user_id = None
            error_message = {
                102: "User not found.",
                103: "Incorrect password."
            }.get(auth_result.code, "Login failed.")
            print(f"Login failed for {username}: {error_message}")
            self.login_form.display_error(error_message)

    def _handle_user_signup_attempt(self, username, password):
        print(f"Attempting to sign up user: {username}")
        from database.auth import register_user
        auth_result = register_user(username, password)

        if auth_result.code is None:
            print(f"User '{username}' created successfully.")
            self._show_login_view()
        else:
            error_message = {
                101: "Username already exists."
            }.get(auth_result.code, "Signup failed.")
            print(f"Signup failed for {username}: {error_message}")
            self.signup_form.display_error(error_message)

    def _handle_game_start(self, game_type, difficulty):
        print(f"Starting game: {game_type} at difficulty {difficulty}")
        self.set_difficulty(difficulty)
        self.set_game(game_type)

    def set_difficulty(self, difficulty):
        self.current_difficulty = difficulty
        if self.controller:
            self.controller.set_difficulty(difficulty)
        print(f"Difficulty set to: {self.current_difficulty}")

    def set_game(self, game_type):
        print(f"set_game called with type: {game_type}")
        if self.board:
            self.windowModule.removeWidget(self.board)
            self.board = None

        self.controller = GameController(game_type=game_type, difficulty=self.current_difficulty)
        self.board = Board(self.controller.get_board(), is_dame=(game_type == "Dame"))

        self.windowModule.addChildWidget(
            self.board,
            Constants.BOARD_WIDTH / 2,
            (Constants.BOARD_HEIGHT / 2 + 40 - self.windowModule.NAVBAR_HEIGHT),
            Pivot.CENTER
        )
        self._show_board_view()

    def handle_cell_click(self, position):
        if self.is_ai_thinking: # Ignore clicks if AI is processing
            print("AI is thinking, click ignored.")
            return

        if not self.controller or not self.board:
            return
        possible_moves, win_status = self.controller.handle_cell_click(position)
        if possible_moves:
            self.board.show_possible_moves(possible_moves)
        else:
            self.board.update_board(self.controller.get_board())
        
        if win_status == "ai_turn_pending":
            self.is_ai_thinking = True # Set flag
            QTimer.singleShot(1000, self._process_ai_move) # 1-second delay
        elif win_status:
            self.show_game_over(win_status)
        self._update_violated_rules() # Moved here to update after human move or AI move processed immediately

    def _process_ai_move(self):
        if not self.controller or not self.board:
            self.is_ai_thinking = False # Reset flag in case of error
            return

        win_status_after_ai, ai_has_more_moves = self.controller.make_ai_move()
        
        self.board.update_board(self.controller.get_board())
        self.board.show_possible_moves([]) # Clear any previous possible moves
        self._update_violated_rules() # Update rules after AI move

        if win_status_after_ai:
            self.show_game_over(win_status_after_ai)
            self.is_ai_thinking = False # Game is over, AI stops thinking
        elif ai_has_more_moves:
            # AI has more moves (e.g., multi-capture in Dame), schedule next step
            QTimer.singleShot(1000, self._process_ai_move) # Keep self.is_ai_thinking = True
        else:
            # AI turn is fully complete
            self.is_ai_thinking = False # Reset flag

    def _update_violated_rules(self):
        if not self.controller or not self.rules_toggle:
            return
        violated_ids = self._get_violated_rule_ids()
        print(f"Updating violated rules: {violated_ids}")
        self.rules_toggle.setViolatedRules(violated_ids)

    def _get_violated_rule_ids(self):
        # Placeholder method to determine violated rules
        violated_ids = []
        if not self.controller or not self.controller.game:
            return violated_ids

        if self.controller.game_type == "TicTacToe":
            pass

        elif self.controller.game_type == "Dame":
            if self.controller.game.current_player == "human":
                all_moves = self.controller.game.get_all_possible_moves(self.controller.game.human_player_piece)
                has_captures = any(move[0] == "capture" for move in all_moves if isinstance(move, list) and len(move) > 0)
                if has_captures:
                    violated_ids.append(1) # Add rule ID for "Schlagen (Pflicht)"
        return violated_ids

    def show_game_over(self, win_status):
        if not self.controller: return
        msg = "You win!" if win_status == "human_wins" else "AI wins!" if win_status == "ai_wins" else "It's a Draw!"

        gamemode_int = GAMEMODE_MAP.get(self.controller.game_type, 0)
        difficulty_int = self.controller.difficulty

        if self.current_user_id is not None:
            if win_status == "human_wins":
                increaseWins(id=self.current_user_id, gamemode=gamemode_int, difficulty=difficulty_int)
                print(f"Recorded win for user {self.current_user_id} in {self.controller.game_type} (diff: {difficulty_int})")
            elif win_status == "ai_wins":
                increaseLosses(id=self.current_user_id, gamemode=gamemode_int, difficulty=difficulty_int)
                print(f"Recorded loss for user {self.current_user_id} in {self.controller.game_type} (diff: {difficulty_int})")
        else:
            print("Guest player. Score not recorded.")

        if self.board:
            self.board_colorize_effect = QGraphicsColorizeEffect()
            self.board_colorize_effect.setColor(Qt.GlobalColor.gray)
            self.board_colorize_effect.setStrength(0.8)
            self.board.setGraphicsEffect(self.board_colorize_effect)

        self.game_over_overlay.update_contents(msg, gamemode_int, difficulty_int)
        
        # Calculate position just before showing, when parent (contentFrame) dimensions are stable
        if self.windowModule and self.windowModule.contentFrame and self.game_over_overlay:
            content_w = self.windowModule.contentFrame.width()
            content_h = self.windowModule.contentFrame.height()
            overlay_s = self.game_over_overlay.size() # This is its fixed size (400x350)

            if content_w > 0 and content_h > 0: # Ensure content frame has valid dimensions
                pos_x = (content_w - overlay_s.width()) / 2
                pos_y = (content_h - overlay_s.height()) / 2
                self.game_over_overlay.move(int(pos_x), int(pos_y))
            else:
                print("Warning: contentFrame has zero dimensions when trying to position game_over_overlay.")
        
        # if self.board: self.board.hide() # DO NOT hide the board (already commented out)
        # if self.rules_toggle: self.rules_toggle.hide() # DO NOT hide rules toggle (already commented out)
        
        # Still hide other main views that are not part of the game screen itself
        self.login_form.hide()
        self.signup_form.hide()
        self.game_setup_form.hide()
        self.image.hide()
        self.play_button.hide()

        self.game_over_overlay.show()
        self.game_over_overlay.raise_() # Bring to front

    def handle_restart_game(self):
        if self.controller:
            self.controller.reset_game()
            self.board.update_board(self.controller.get_board())
            self.board.show_possible_moves([])
            self._show_board_view()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())