from games.dame import Dame
from games.tic_tac_toe import TicTacToe
from ai.minimax import Minimax

class GameController:
    def __init__(self, game_type="Dame", difficulty=3):
        self.game = self._create_game(game_type)
        self.difficulty = difficulty
        self.selected_piece = None
        self.possible_moves = []
        self.game_type = game_type
        self.mandatory_human_captures = []

    def _create_game(self, game_type):
        if game_type == "Dame":
            return Dame()
        elif game_type == "TicTacToe":
            return TicTacToe()
        else:
            raise ValueError("Unknown game type")

    def get_board(self):
        return self.game.board

    def set_difficulty(self, max_depth):
        self.difficulty = max_depth
        self.reset_game()

    def _get_mandatory_human_captures(self):
        if self.game_type == "Dame" and self.game.current_player == "human":
            all_moves = self.game.get_all_possible_moves(self.game.human_player_piece)
            captures = [move for move in all_moves if move[0] == "capture"]
            return captures
        return []

    def handle_cell_click(self, position):
        if self.game.is_game_over():
            self.mandatory_human_captures = []
            return None, None
        
        if self.game_type == "Dame" and self.game.current_player == "human":
            if not self.selected_piece and not self.mandatory_human_captures:
                 self.mandatory_human_captures = self._get_mandatory_human_captures()

        if self.game.current_player == "ai":
            ai_win_status, _ = self.make_ai_move()
            self.mandatory_human_captures = [] 
            return ai_win_status, None

        if not self._is_valid_position(position):
            self.reset_selection(clear_turn_mandatory_captures=True)
            return None, None

        if self.game_type == "Dame":
            return self._handle_dame_click(position)
        else:
            return self._handle_tictactoe_click(position)

    def _handle_dame_click(self, position):
        # Part 1: A piece is currently selected
        if self.selected_piece is not None:
            current_selected_coord = self.selected_piece

            chosen_move = None
            for move_option in self.possible_moves:
                if move_option[2] == position:
                    chosen_move = move_option
                    break

            if chosen_move:
                # 1. CLICKED A VALID MOVE DESTINATION
                valid, further_capture = self.game.make_move(chosen_move, self.game.human_player_piece)
                if valid:
                    win_status = self.game.check_win_condition()
                    if win_status:
                        self.reset_selection(clear_turn_mandatory_captures=True)
                        return None, win_status
                    
                    if further_capture:
                        self.selected_piece = chosen_move[2] 
                        self.possible_moves = self.game.get_possible_moves(self.selected_piece)
                        self.possible_moves = [m for m in self.possible_moves if m[0] == "capture"]
                        self.mandatory_human_captures = self.possible_moves 
                        if not self.possible_moves:
                            self.reset_selection(clear_turn_mandatory_captures=True)
                            return None, "ai_turn_pending"
                        return self.possible_moves, None
                    else:
                        self.reset_selection(clear_turn_mandatory_captures=True)
                        return None, "ai_turn_pending"
                else:
                    return None, None 
            
            elif self.game.board[position[0]][position[1]] == self.game.human_player_piece and \
                 position != current_selected_coord:
                # 2. CLICKED ANOTHER OWN PIECE
                self.reset_selection(clear_turn_mandatory_captures=True)
                self.mandatory_human_captures = self._get_mandatory_human_captures()
                # Fall through to Part 2 to select the new piece at 'position'.
            
            elif position == current_selected_coord:
                # 3. CLICKED THE CURRENTLY SELECTED PIECE AGAIN (DESELECT)
                self.reset_selection(clear_turn_mandatory_captures=True)
                self.mandatory_human_captures = self._get_mandatory_human_captures()
                return None, None
            
            else:
                # 4. CLICKED ANYWHERE ELSE (empty square, opponent piece)
                self.reset_selection(clear_turn_mandatory_captures=True)
                self.mandatory_human_captures = self._get_mandatory_human_captures()
                return None, None

        # Part 2: No piece is selected (self.selected_piece is None)
        if self.game.board[position[0]][position[1]] == self.game.human_player_piece:
            if self.mandatory_human_captures:
                can_make_mandatory_capture = any(m[1] == position for m in self.mandatory_human_captures)
                if not can_make_mandatory_capture:
                    return None, None 
            
            self.selected_piece = position
            if self.mandatory_human_captures:
                self.possible_moves = [
                    m for m in self.mandatory_human_captures if m[1] == self.selected_piece
                ]
            else:
                self.possible_moves = self.game.get_possible_moves(self.selected_piece)

            if not self.possible_moves: 
                self.reset_selection(clear_turn_mandatory_captures=False)
                return None, None
            return self.possible_moves, None
        else:
            return None, None

    def _handle_tictactoe_click(self, position):
        valid = self.game.make_move(position, self.game.human_player_mark)
        if valid:
            win_status = self.game.check_win_condition()
            if win_status:
                self.mandatory_human_captures = []
                return None, win_status
            self.mandatory_human_captures = []
            return None, "ai_turn_pending"
        return None, None

    def _is_valid_position(self, position):
        try:
            row, col = position
            return 0 <= row < self.game.board_size and 0 <= col < self.game.board_size
        except (TypeError, IndexError):
            return False

    def reset_selection(self, clear_turn_mandatory_captures=False):
        self.selected_piece = None
        self.possible_moves = []
        if clear_turn_mandatory_captures:
            self.mandatory_human_captures = []

    def _resync_dame_piece_sets(self):
        if self.game_type != "Dame":
            return
        self.game.human_pieces.clear()
        self.game.ai_pieces.clear()
        for row in range(self.game.board_size):
            for col in range(self.game.board_size):
                if self.game.board[row][col] == self.game.human_player_piece:
                    self.game.human_pieces.add((row, col))
                elif self.game.board[row][col] == self.game.ai_player_piece:
                    self.game.ai_pieces.add((row, col))

    def make_ai_move(self):
        if self.game.is_game_over():
            self.mandatory_human_captures = []
            return self.game.check_win_condition(), False
        
        if self.game.current_player != "ai":
            return self.game.check_win_condition(), False

        ai = Minimax(self.game, max_depth=self.difficulty)
        ai_player_id = self.game.ai_player_piece if self.game_type == "Dame" else self.game.ai_player_mark
        ai_move = ai.find_best_move(ai_player_id)

        if not ai_move:
            if self.game_type == "Dame":
                 pass 
            else:
                self.game.switch_player()
            return self.game.check_win_condition(), False

        further_capture_pending_for_ai = False
        if self.game_type == "Dame":
            valid, further_capture_after_ai_move = self.game.make_move(ai_move, self.game.ai_player_piece)
            if valid:
                win_status = self.game.check_win_condition()
                if win_status:
                    return win_status, False
                if further_capture_after_ai_move:
                    further_capture_pending_for_ai = True 
            else:
                return self.game.check_win_condition(), False
        else:
            valid = self.game.make_move(ai_move, self.game.ai_player_mark)
            if not valid:
                return self.game.check_win_condition(), False
        
        current_win_status = self.game.check_win_condition()
        if current_win_status:
            return current_win_status, False

        ai_has_more_moves_now = (self.game_type == "Dame" and further_capture_pending_for_ai)
        
        return current_win_status, ai_has_more_moves_now

    def reset_game(self):
        self.game = self._create_game(self.game_type)
        self.reset_selection(clear_turn_mandatory_captures=True)