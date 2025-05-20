# import tkinter as tk # GUI Team will handle GUI library
# from tkinter import simpledialog, messagebox, scrolledtext # GUI Team will handle GUI library

from .games.tic_tac_toe import TicTacToe
from .games.dame import Dame, HUMAN_PIECE as DAME_HUMAN_PIECE, AI_PIECE as DAME_AI_PIECE
from .ai.minimax import Minimax
from .database.database_manager import DatabaseManager
from .database.user_management import UserManagement

# --- Placeholder for GUI Team's Implementation ---
class GUIManagerPlaceholder:
    def __init__(self, app_controller):
        self.app_controller = app_controller # To call back to App for logic
        print("[GUI Placeholder] GUIManager initialized. Waiting for GUI team to implement.")
        # self.root = tk.Tk() # GUI team will manage the root window

    def display_main_menu(self, user_status):
        print(f"[GUI Placeholder] Displaying Main Menu. User Status: {user_status}")
        # GUI team: Implement main menu with game selection, login, register buttons

    def display_game_view(self, game_name, board_string, current_player_text, difficulty):
        print(f"[GUI Placeholder] Displaying Game View for {game_name} (Difficulty: {difficulty})")
        print(f"[GUI Placeholder] Board:\n{board_string}")
        print(f"[GUI Placeholder] Status: {current_player_text}")
        # GUI team: Implement game board display, move input fields, status labels, rules, quit buttons

    def get_user_credentials(self, prompt_type): # "Login" or "Register"
        print(f"[GUI Placeholder] Requesting user credentials for {prompt_type}.")
        # GUI team: Implement dialogs to get username/password
        # For placeholder, returning fixed values or None
        if prompt_type == "Login":
            # Simulating user input for testing flow
            # username = input(f"[Placeholder Input] Enter {prompt_type} username: ") 
            # password = input(f"[Placeholder Input] Enter {prompt_type} password: ")
            # return username, password
            return "testuser", "password" # Auto-input for faster testing
        return None, None # Default for register or if no input simulated

    def get_human_move(self, game_name):
        print(f"[GUI Placeholder] Requesting human move for {game_name}.")
        # GUI team: Implement graphical move input (e.g., clicking board) or text field
        # Simulating user input for testing flow
        # move_str = input("[Placeholder Input] Enter your move: ")
        # return move_str
        if game_name == "TicTacToe": return "0,0" # Auto-input for TTT
        if game_name == "Dame": return "1,1,2,0" # Auto-input for Dame simple move (example)
        return "" # Default
    
    def get_difficulty_selection(self):
        print(f"[GUI Placeholder] Requesting AI difficulty selection (1-5).")
        # GUI team: Implement a scale or input for difficulty
        # return int(input("[Placeholder Input] Enter AI difficulty (1-5): ") or "3")
        return 3 # Default difficulty

    def show_message(self, title, message, msg_type="info"): # msg_type: "info", "error", "warning"
        print(f"[GUI Placeholder] [{msg_type.upper()}] {title}: {message}")
        # GUI team: Implement message boxes / notifications

    def ask_yes_no(self, title, question):
        print(f"[GUI Placeholder] ASK YES/NO: {title} - {question}")
        # GUI team: Implement yes/no dialog
        # return input(f"[Placeholder Input] {question} (yes/no): ").lower() == 'yes'
        return True # Default to yes for flows like "play as guest?"

    def update_user_status_display(self, status_text):
        print(f"[GUI Placeholder] Updating user status display: {status_text}")
        # GUI team: Update the part of the UI that shows login status

    def switch_to_main_menu_view(self):
        print(f"[GUI Placeholder] Switching view to Main Menu.")
        # GUI team: Code to hide game view and show main menu

    def switch_to_game_view(self, game_name, difficulty):
        print(f"[GUI Placeholder] Switching view to Game for {game_name} (Difficulty: {difficulty})")
        # GUI team: Code to hide main menu and show game view

    def run_main_loop(self):
        print("[GUI Placeholder] Starting GUI main loop (placeholder). GUI team will implement real loop.")
        # GUI team: This will be their tk.mainloop() or equivalent
        # For this placeholder, we might simulate a simple command-line interaction loop
        # or just allow the AppController to drive a few state changes.
        self.app_controller.start_application() # Trigger initial state

    def close_gui(self):
        print("[GUI Placeholder] Closing GUI.")

# --- Application Controller (Manages game logic, AI, and interacts with GUI Manager) ---
class App:
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.user_manager = UserManagement(self.db_manager)
        self.gui_manager = GUIManagerPlaceholder(self) # GUI Team provides their implementation
        
        self.current_game_instance = None
        self.ai_opponent = None
        self.game_name = None
        self.current_difficulty = 3
        print("[App Controller] Initialized.")

    def start_application(self):
        print("[App Controller] Application started. Displaying main menu.")
        self.update_user_status_for_gui()
        self.gui_manager.display_main_menu(self.user_manager.get_current_user() or "Not Logged In")
        # In a real scenario, GUI would now wait for user actions (handled by GUI team)
        # For placeholder, we can simulate some actions if needed for testing, or assume GUI calls back

    def update_user_status_for_gui(self):
        user = self.user_manager.get_current_user()
        status = f"Logged in as: {user}" if user and user != "Guest" else "Playing as Guest / Not Logged In"
        self.gui_manager.update_user_status_display(status)

    # --- Callbacks from GUI Placeholder (simulated) ---
    def handle_login_request(self):
        username, password = self.gui_manager.get_user_credentials("Login")
        if username and password:
            if self.user_manager.login_user(username, password):
                self.gui_manager.show_message("Login Successful", f"Welcome back, {username}!")
            else:
                self.gui_manager.show_message("Login Failed", "Invalid username or password.", "error")
        self.update_user_status_for_gui()
        # GUI would typically refresh part of the menu or re-display it
        self.gui_manager.display_main_menu(self.user_manager.get_current_user() or "Not Logged In") 

    def handle_register_request(self):
        username, password = self.gui_manager.get_user_credentials("Register")
        # For placeholder, let's simulate a successful registration for flow
        if not username: username = "newuser"
        if not password: password = "newpass"
        
        if username and password:
            if self.user_manager.register_user(username, password):
                self.gui_manager.show_message("Registration Successful", f"User {username} registered. You can now log in.")
            else:
                self.gui_manager.show_message("Registration Failed", "Username might already exist.", "error")
        self.update_user_status_for_gui()
        self.gui_manager.display_main_menu(self.user_manager.get_current_user() or "Not Logged In")

    def handle_guest_play_request(self):
        self.user_manager.logout_user() # Clear any existing login
        self.user_manager.current_user = "Guest"
        self.gui_manager.show_message("Guest Mode", "Playing as Guest. Scores will not be saved.")
        self.update_user_status_for_gui()
        self.gui_manager.display_main_menu(self.user_manager.get_current_user() or "Not Logged In")

    def handle_logout_request(self):
        self.user_manager.logout_user()
        self.gui_manager.show_message("Logout", "You have been logged out.")
        self.update_user_status_for_gui()
        self.gui_manager.display_main_menu(self.user_manager.get_current_user() or "Not Logged In")

    def handle_game_selection(self, game_choice):
        if self.user_manager.get_current_user() is None:
            if self.gui_manager.ask_yes_no("Login Required", "Play as Guest?"):
                self.handle_guest_play_request() # This will also update GUI status
            else:
                return # Stay on main menu
        
        self.game_name = game_choice
        self.current_difficulty = self.gui_manager.get_difficulty_selection()
        
        if game_choice == "TicTacToe":
            self.current_game_instance = TicTacToe()
        elif game_choice == "Dame":
            self.current_game_instance = Dame()
        else:
            self.gui_manager.show_message("Error", f"Unknown game: {game_choice}", "error")
            return

        self.ai_opponent = Minimax(self.current_game_instance, max_depth=self.current_difficulty)
        self.current_game_instance.current_player = "human" # Ensure human starts (LF4040)
        
        self.gui_manager.switch_to_game_view(self.game_name, self.current_difficulty)
        self.update_gui_game_state("Your turn (Human).")

    def update_gui_game_state(self, status_message):
        if self.current_game_instance:
            board_str = str(self.current_game_instance)
            self.gui_manager.display_game_view(self.game_name, board_str, status_message, self.current_difficulty)

    def handle_human_move_submission(self):
        if not self.current_game_instance or self.current_game_instance.current_player != "human":
            self.gui_manager.show_message("Game Error", "Not your turn or game not started.", "warning")
            return

        move_str = self.gui_manager.get_human_move(self.game_name)
        valid_move_made = False
        human_player_mark = self.current_game_instance.human_player_mark if self.game_name == "TicTacToe" else DAME_HUMAN_PIECE

        try:
            if self.game_name == "TicTacToe":
                parts = move_str.split(',')
                if len(parts) == 2:
                    row, col = int(parts[0]), int(parts[1])
                    if self.current_game_instance.make_move((row, col), human_player_mark):
                        valid_move_made = True
            elif self.game_name == "Dame":
                # Dame move parsing logic is complex. For placeholder, assume get_human_move from GUI
                # returns a pre-validated move structure or a simple string that can be looked up.
                # The current get_human_move placeholder returns a simple string.
                # We'll try to find this specific move in possible_moves for simplicity.
                possible_moves = self.current_game_instance.get_possible_moves(human_player_mark)
                selected_move = None
                parts = [p.strip() for p in move_str.split(',')]
                
                if len(parts) == 4: # Simple move: fr,fc,tr,tc
                    fr,fc,tr,tc = map(int, parts)
                    for p_move in possible_moves:
                        if p_move[0] == 'move' and p_move[1] == (fr,fc) and p_move[2] == (tr,tc):
                            selected_move = p_move
                            break
                elif len(parts) == 6: # Simple capture: fr,fc,tr,tc,cr,cc
                    fr,fc,tr,tc,cr,cc = map(int, parts)
                    for p_move in possible_moves:
                         if p_move[0] == 'capture' and p_move[1] == (fr,fc) and p_move[2] == (tr,tc) and \
                            len(p_move[3]) == 1 and p_move[3][0] == (cr,cc):
                            selected_move = p_move
                            break
                
                if selected_move:
                    if self.current_game_instance.make_move(selected_move, human_player_mark):
                        valid_move_made = True
            
            if not valid_move_made:
                 self.gui_manager.show_message("Invalid Move", f"The move '{move_str}' is not valid. Please try again.", "warning")

        except Exception as e:
            self.gui_manager.show_message("Move Error", f"Error processing move '{move_str}': {e}", "error")
            return

        if valid_move_made:
            winner = self.current_game_instance.check_win_condition()
            if winner:
                self.handle_game_end_logic(winner)
            else:
                self.update_gui_game_state("AI is thinking...")
                self.trigger_ai_turn() # AI's turn
        else:
            self.update_gui_game_state("Invalid move. Your turn (Human).") # Stay on human's turn

    def trigger_ai_turn(self):
        if not self.current_game_instance or self.current_game_instance.current_player != "ai":
            return

        self.ai_opponent.max_depth = self.current_difficulty # Ensure AI difficulty is up-to-date
        ai_piece = self.current_game_instance.ai_player_mark if self.game_name == "TicTacToe" else DAME_AI_PIECE
        
        print(f"[App Controller] AI ({ai_piece}) is thinking for {self.game_name} (depth: {self.ai_opponent.max_depth})...")
        # Corrected call to find_best_move, it now only takes the AI's piece.
        # The Minimax instance already knows the game_logic_instance and its own max_depth.
        best_move = self.ai_opponent.find_best_move(ai_piece)
        print(f"[App Controller] AI chose move: {best_move}")

        if best_move:
            if self.game_name == "TicTacToe":
                self.current_game_instance.make_move(best_move, self.current_game_instance.ai_player_mark)
            elif self.game_name == "Dame":
                self.current_game_instance.make_move(best_move, ai_piece)
            
            winner = self.current_game_instance.check_win_condition()
            if winner:
                self.handle_game_end_logic(winner)
            else:
                self.update_gui_game_state("Your turn (Human).")
        else:
            # AI has no moves. This should lead to a win condition for human.
            print("[App Controller] AI has no moves. Checking game state.")
            winner = self.current_game_instance.check_win_condition()
            if winner: # Should be human_wins or draw
                self.handle_game_end_logic(winner)
            else:
                # This state should ideally not be reached if win logic is correct
                self.gui_manager.show_message("Game Error", "AI has no moves, but game not over?", "error")
                self.update_gui_game_state("Error: AI has no moves. Your turn (Human).")

    def handle_game_end_logic(self, winner_status):
        current_user = self.user_manager.get_current_user()
        is_truly_guest = self.user_manager.is_guest() # Checks for None or "Guest"

        message = ""
        if winner_status == "human_wins":
            message = "Congratulations! You won!"
            if not is_truly_guest and current_user:
                self.db_manager.update_score(current_user, self.game_name, self.current_difficulty, True)
        elif winner_status == "ai_wins":
            message = "AI wins! Better luck next time."
            if not is_truly_guest and current_user:
                self.db_manager.update_score(current_user, self.game_name, self.current_difficulty, False)
        elif winner_status == "draw":
            message = "It's a draw!"
        
        self.update_gui_game_state(message) # Update board one last time with final message
        self.gui_manager.show_message("Game Over", message)
        # GUI team would disable move input here.

    def handle_rules_request(self):
        if self.current_game_instance:
            rules = self.current_game_instance.get_rules()
            self.gui_manager.show_message(f"{self.game_name} Rules", rules)
        else:
            self.gui_manager.show_message("No Game", "No game selected to show rules for.", "warning")

    def handle_quit_game_request(self):
        # Optional: show high scores (LF4100). DB team would provide data.
        # high_scores = self.db_manager.get_high_scores(self.game_name, self.current_difficulty)
        # self.gui_manager.show_high_scores_view(high_scores) 
        
        self.current_game_instance = None
        self.ai_opponent = None
        self.game_name = None
        self.gui_manager.switch_to_main_menu_view()
        self.update_user_status_for_gui()
        self.gui_manager.display_main_menu(self.user_manager.get_current_user() or "Not Logged In")

    def handle_app_exit_request(self):
        if self.gui_manager.ask_yes_no("Quit", "Do you want to quit SpieleSammlung?"):
            print("[App Controller] Application closing.")
            self.db_manager.close() # DB team ensures this properly closes connections
            self.gui_manager.close_gui() # GUI team ensures this closes their window
            return True # Allow exit
        return False # Veto exit

# --- Main execution (conceptual) ---
if __name__ == "__main__":
    app_controller = App()
    # The GUI Manager would start its own main loop (e.g., Tkinter's mainloop())
    # and call methods on app_controller based on user interactions.
    app_controller.gui_manager.run_main_loop() 

    # For non-GUI testing of the flow, we can simulate some calls:
    print("\n--- SIMULATING APP FLOW (NO ACTUAL GUI) ---")
    # app_controller.start_application() # Already called by run_main_loop placeholder
    
    # Simulate user trying to log in
    print("\nSimulating Login...")
    app_controller.handle_login_request()
    
    # Simulate selecting TicTacToe
    print("\nSimulating Game Selection: TicTacToe...")
    app_controller.handle_game_selection("TicTacToe")
    
    # Simulate a few moves if a game is running (TicTacToe)
    if app_controller.current_game_instance and app_controller.game_name == "TicTacToe":
        print("\nSimulating Human Move for TTT (0,0)...")
        # GUIManager.get_human_move is hardcoded to return "0,0" for TTT for this simulation
        app_controller.handle_human_move_submission()
        
        # If AI didn't win, simulate another human move (e.g., "0,1")
        if app_controller.current_game_instance and app_controller.current_game_instance.current_player == "human":
             # Need to make GUIManager.get_human_move return something different or make it interactive
             # For now, the AI will play its turn, then it will be human again, but get_human_move will return 0,0 again.
             # This part of simulation needs refinement if we want to test longer game plays without real GUI.
             print("\nSimulating another Human Move for TTT (0,1) - (Note: placeholder input might be fixed)...")
             # To make this work better, GUIManagerPlaceholder.get_human_move should be more flexible for simulation
             # For now, it will likely try to play 0,0 again if not handled.
    
    # Simulate quitting game
    print("\nSimulating Quit Game...")
    app_controller.handle_quit_game_request()
    
    # Simulate app exit
    print("\nSimulating App Exit...")
    app_controller.handle_app_exit_request() # Will print placeholder close messages

    print("\n--- SIMULATION END ---") 