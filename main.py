import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QHBoxLayout, QWidget
from PySide6.QtGui import QPainter, QPen, QColor
from PySide6.QtCore import Qt
from gui.board import Board
from gui.core.confiq import Colors, Constants
from gui.window import WindowModule, Pivot
from gui.signalBus import bus
from gui.gameController import GameController
from gui.gameOverDialog import GameOverDialog
from gui.loginForm import LoginForm
from gui.signupForm import SignupForm
import bcrypt

# Simple mapping for gamemode to integer for the database
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
        
        self.windowModule = GridWindowModule()
        self.setCentralWidget(self.windowModule)

        self.controller = None
        self.board = None
        self.current_difficulty = 3
        self.current_user_id = None # To store logged-in user's ID

        self._setup_login_form()
        self._setup_signup_form()
        self._setup_game_selection_ui()

        bus.cellClicked.connect(self.handle_cell_click)
        
        # Connect LoginForm signals
        self.login_form.loginAttempt.connect(self._handle_user_login_attempt) # Changed from loginSuccessful
        self.login_form.guestAccessRequested.connect(self._handle_guest_access) # New handler for clarity
        self.login_form.signupRequested.connect(self._show_signup_view)

        # Connect SignupForm signals
        self.signup_form.signupAttempted.connect(self._handle_user_signup_attempt)
        self.signup_form.loginLinkActivated.connect(self._show_login_view)
        self.signup_form.guestAccessRequested.connect(self._handle_guest_access)

        #homescreen setup and show

        self._show_login_view()

    def _setup_login_form(self):
        self.login_form = LoginForm()
        content_frame_height = Constants.BOARD_HEIGHT - self.windowModule.NAVBAR_HEIGHT
        content_frame_width = Constants.BOARD_WIDTH
        center_x = content_frame_width / 2
        center_y = content_frame_height / 2
        self.windowModule.addChildWidget(self.login_form, center_x, center_y, Pivot.CENTER)

    def _setup_signup_form(self):
        self.signup_form = SignupForm()
        content_frame_height = Constants.BOARD_HEIGHT - self.windowModule.NAVBAR_HEIGHT
        content_frame_width = Constants.BOARD_WIDTH
        center_x = content_frame_width / 2
        center_y = content_frame_height / 2
        self.windowModule.addChildWidget(self.signup_form, center_x, center_y, Pivot.CENTER)

    def _setup_game_selection_ui(self):
        self.game_container = QWidget()
        game_layout = QHBoxLayout(self.game_container)
        game_layout.setSpacing(10)
        game_layout.setContentsMargins(10, 10, 10, 10)
        dame_button = QPushButton("Dame")
        tictactoe_button = QPushButton("TicTacToe")
        dame_button.setStyleSheet(f"background-color: {Colors.PRIMARY}; color: {Colors.FONT_PRIMARY};")
        tictactoe_button.setStyleSheet(f"background-color: {Colors.PRIMARY}; color: {Colors.FONT_PRIMARY};")
        dame_button.clicked.connect(lambda: (print("Dame button clicked"), self.set_game("Dame")))
        tictactoe_button.clicked.connect(lambda: (print("TicTacToe button clicked"), self.set_game("TicTacToe")))
        game_layout.addWidget(dame_button)
        game_layout.addWidget(tictactoe_button)
        game_container_y_in_content = 120 - self.windowModule.NAVBAR_HEIGHT 
        self.windowModule.addChildWidget(self.game_container, Constants.BOARD_WIDTH / 2, game_container_y_in_content, Pivot.CENTER)

        self.difficulty_container = QWidget()
        difficulty_layout = QHBoxLayout(self.difficulty_container)
        difficulty_layout.setSpacing(10)
        difficulty_layout.setContentsMargins(10, 10, 10, 10)
        easy_button = QPushButton("Easy")
        medium_button = QPushButton("Medium")
        hard_button = QPushButton("Hard")
        easy_button.setStyleSheet(f"background-color: {Colors.PRIMARY}; color: {Colors.FONT_PRIMARY};")
        medium_button.setStyleSheet(f"background-color: {Colors.PRIMARY}; color: {Colors.FONT_PRIMARY};")
        hard_button.setStyleSheet(f"background-color: {Colors.PRIMARY}; color: {Colors.FONT_PRIMARY};")
        easy_button.clicked.connect(lambda: self.set_difficulty(1))
        medium_button.clicked.connect(lambda: self.set_difficulty(3))
        hard_button.clicked.connect(lambda: self.set_difficulty(5))
        difficulty_layout.addWidget(easy_button)
        difficulty_layout.addWidget(medium_button)
        difficulty_layout.addWidget(hard_button)
        difficulty_container_y_in_content = (Constants.BOARD_HEIGHT - 130) - self.windowModule.NAVBAR_HEIGHT
        self.windowModule.addChildWidget(self.difficulty_container, Constants.BOARD_WIDTH / 2, difficulty_container_y_in_content, Pivot.CENTER)

    def _show_login_view(self):
        self.login_form.show()
        self.signup_form.hide()
        self.game_container.hide()
        self.difficulty_container.hide()
        if self.board: self.board.hide()

    def _show_signup_view(self):
        self.login_form.hide()
        self.signup_form.show()
        self.signup_form.clear_error()
        self.game_container.hide()
        self.difficulty_container.hide()
        if self.board: self.board.hide()

    def _show_game_selection_view(self):
        self.login_form.hide()
        self.signup_form.hide()
        self.game_container.show()
        self.difficulty_container.show()
        if self.board: 
            self.windowModule.removeWidget(self.board)
            self.board = None
        if self.controller:
            self.controller = None

    def _show_board_view(self):
        self.login_form.hide()
        self.signup_form.hide()
        self.game_container.hide()
        self.difficulty_container.hide()
        if self.board: self.board.show()

    def _handle_guest_access(self):
        print("Guest access requested. Showing game selection.")
        self.current_user_id = None # Explicitly set no user for guest
        self._show_game_selection_view()

    def _handle_user_login_attempt(self, username, password):
        print(f"Attempting to log in user: {username}")
        from database.auth import login_user # Use the existing login_user

        auth_result = login_user(username, password)

        if auth_result.code is None: # Success is code None, id will be user_id
            self.current_user_id = auth_result.id
            print(f"User '{username}' (ID: {self.current_user_id}) logged in successfully. Showing game selection.")
            self.login_form.clear_error() # Clear any previous login errors
            self._show_game_selection_view()
        else:
            self.current_user_id = None
            error_message = "Login failed."
            if auth_result.code == 102:
                error_message = "User not found."
            elif auth_result.code == 103:
                error_message = "Incorrect password."
            print(f"Login failed for {username}: {error_message} (Code: {auth_result.code})")
            self.login_form.display_error(error_message)
    
    def _handle_user_signup_attempt(self, username, password):
        print(f"Attempting to sign up user: {username} using register_user.")
        # No need to hash password here, register_user does it.
        
        from database.auth import register_user # Use the existing register_user

        auth_result = register_user(username, password) # Pass plain password

        if auth_result.code is None: # Success is indicated by code being None
            print(f"User '{username}' (ID: {auth_result.id}) created successfully via register_user. Navigating to login.")
            # Optionally, pass a success message to login form to display
            # self.login_form.display_message("Signup successful! Please log in.")
            self._show_login_view()
        else:
            # Map error codes to messages if desired, or use a generic one
            error_message = "Signup failed."
            if auth_result.code == 101:
                error_message = "Username already exists."
            # Add more specific messages for other codes if register_user has them
            
            print(f"Signup failed for {username} via register_user: {error_message} (Code: {auth_result.code})")
            self.signup_form.display_error(error_message)

    def _handle_signup_request(self):
        print("Signup link on login form clicked. Showing signup view.")
        self.login_form.clear_error() # Clear login errors when switching to signup
        self._show_signup_view()

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
        
        board_center_x = Constants.BOARD_WIDTH / 2
        content_frame_height = Constants.BOARD_HEIGHT - self.windowModule.NAVBAR_HEIGHT
        board_y_target_in_content_frame = (Constants.BOARD_HEIGHT / 2 + 40) - self.windowModule.NAVBAR_HEIGHT

        self.windowModule.addChildWidget(self.board, board_center_x, board_y_target_in_content_frame, Pivot.CENTER)
        self._show_board_view()

    def handle_cell_click(self, position):
        if not self.controller or not self.board:
            return
        possible_moves, win_status = self.controller.handle_cell_click(position)
        if possible_moves:
            self.board.show_possible_moves(possible_moves)
        else:
            self.board.update_board(self.controller.get_board())
        if win_status:
            self.show_game_over(win_status)

    def show_game_over(self, win_status):
        if not self.controller: return
        msg = "Human wins!" if win_status == "human_wins" else "AI wins!" if win_status == "ai_wins" else "It's a Draw!"
        
        # Pass current_user_id to GameOverDialog if it needs to record score for a specific user
        # For now, GameOverDialog only uses gamemode and difficulty for fetching general scoreboard.
        # If we enhance DataQueries.increaseWins/Losses to take user_id, this is where it'd be passed.
        # print(f"Game over for user_id: {self.current_user_id}") 

        gamemode_int = GAMEMODE_MAP.get(self.controller.game_type, 0)
        difficulty_int = self.controller.difficulty
        dialog = GameOverDialog(msg, gamemode_int, difficulty_int, self)
        dialog.restartClicked.connect(self.handle_restart_game)
        dialog.mainMenuClicked.connect(self._show_game_selection_view)
        dialog.exec()

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