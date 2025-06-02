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
        else:  # TicTacToe
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
                        self._update_dame_piece_sets(move)
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
                            return None, self.make_ai_move()
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
            return None, self.make_ai_move()
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

    def _update_dame_piece_sets(self, move):
        if self.game_type != "Dame":
            return
        move_type, from_pos, to_pos = move[0], move[1], move[2]
        pieces_set = self.game.human_pieces if self.game.current_player == "human" else self.game.ai_pieces
        opponent_pieces = self.game.ai_pieces if self.game.current_player == "human" else self.game.human_pieces
        try:
            pieces_set.remove(from_pos)
            pieces_set.add(to_pos)
            if move_type == "capture":
                for captured in move[3]:
                    opponent_pieces.discard(captured)
        except KeyError:
            self._resync_dame_piece_sets()

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
            return None
        while self.game.current_player == "ai" and not self.game.is_game_over():
            ai = Minimax(self.game, max_depth=self.difficulty)
            ai_move = ai.find_best_move(self.game.ai_player_piece if self.game_type == "Dame" else self.game.ai_player_mark)
            if ai_move:
                if self.game_type == "Dame":
                    valid, further_capture = self.game.make_move(ai_move, self.game.ai_player_piece)
                    if valid:
                        self._update_dame_piece_sets(ai_move)
                        if not further_capture:
                            break
                else:  # TicTacToe
                    valid = self.game.make_move(ai_move, self.game.ai_player_mark)
                    if valid:
                        break
            else:
                break
        return self.game.check_win_condition()

    def reset_game(self):
        self.game = self._create_game(self.game_type)
        self.reset_selection()