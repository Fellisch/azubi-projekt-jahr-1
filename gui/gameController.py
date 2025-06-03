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

    def handle_cell_click(self, position):
        if self.game.is_game_over():
            return None, None
        if self.game.current_player == "ai":
            return self.make_ai_move(), None

        if not self._is_valid_position(position):
            self.reset_selection()
            return None, None

        if self.game_type == "Dame":
            return self._handle_dame_click(position)
        else:
            return self._handle_tictactoe_click(position)

    def _handle_dame_click(self, position):
        if self.selected_piece is None:
            if self.game.board[position[0]][position[1]] == self.game.human_player_piece:
                self.selected_piece = position
                self.possible_moves = self.game.get_possible_moves(position)
                return self.possible_moves, None
            else:
                self.reset_selection()
                return None, None
        else:
            for move in self.possible_moves:
                if move[2] == position:
                    valid, further_capture = self.game.make_move(move, self.game.human_player_piece)
                    if valid:
                        win_status = self.game.check_win_condition()
                        if win_status:
                            self.reset_selection()
                            return None, win_status
                        elif further_capture:
                            self.selected_piece = move[2]
                            self.possible_moves = self.game.get_possible_moves(self.selected_piece)
                            return self.possible_moves, None
                        else:
                            self.reset_selection()
                            # AI move will be triggered by MainWindow after a delay
                            return None, "ai_turn_pending"
                    else:
                        self.reset_selection()
                        return None, None
            self.reset_selection()
            return None, None

    def _handle_tictactoe_click(self, position):
        valid = self.game.make_move(position, self.game.human_player_mark)
        if valid:
            win_status = self.game.check_win_condition()
            if win_status:
                return None, win_status
            # AI move will be triggered by MainWindow after a delay
            return None, "ai_turn_pending"
        return None, None

    def _is_valid_position(self, position):
        try:
            row, col = position
            return 0 <= row < self.game.board_size and 0 <= col < self.game.board_size
        except (TypeError, IndexError):
            return False

    def reset_selection(self):
        self.selected_piece = None
        self.possible_moves = []

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
        if self.game.is_game_over() or self.game.current_player != "ai":
            return self.game.check_win_condition(), False # Return win status and no more moves

        ai = Minimax(self.game, max_depth=self.difficulty)
        ai_player_id = self.game.ai_player_piece if self.game_type == "Dame" else self.game.ai_player_mark
        ai_move = ai.find_best_move(ai_player_id)

        if not ai_move:
            # No move found, switch player to prevent infinite loop if AI has no moves but game not over
            if self.game_type == "Dame": # Dame has explicit player switching in make_move
                 pass # If no dame move, current player may be stuck - win condition should handle this.
            else: # TicTacToe may need explicit player switch if AI has no valid moves (should not happen in normal TTT)
                self.game.switch_player()
            return self.game.check_win_condition(), False

        further_capture_pending = False
        if self.game_type == "Dame":
            valid, further_capture_after_move = self.game.make_move(ai_move, self.game.ai_player_piece)
            if valid:
                win_status = self.game.check_win_condition()
                if win_status: # Game ended by this move
                    return win_status, False
                if further_capture_after_move:
                    further_capture_pending = True # AI has another capture
                # If no further capture, player was switched by game.make_move
            else:
                # Invalid AI move somehow, should be rare. End AI turn.
                return self.game.check_win_condition(), False
        else: # TicTacToe
            valid = self.game.make_move(ai_move, self.game.ai_player_mark)
            if not valid:
                 # Invalid AI move, should be rare. End AI turn.
                return self.game.check_win_condition(), False
            # For TicTacToe, player is switched by game.make_move if move is valid and no win.
        
        current_win_status = self.game.check_win_condition()
        if current_win_status:
            return current_win_status, False # Game over, no more AI moves

        # If it's Dame and a further capture is pending, AI still has moves.
        # Otherwise, player has been switched by game.make_move, so AI has no more moves this turn.
        ai_has_more_moves_now = (self.game_type == "Dame" and further_capture_pending)
        
        return current_win_status, ai_has_more_moves_now

    def reset_game(self):
        self.game = self._create_game(self.game_type)
        self.reset_selection()