from ai.minimax import Minimax
from games.base_game import BaseGame


class TicTacToe(BaseGame):
    def __init__(self, board_size=6):
        super().__init__(board_size)
        self.human_player_mark = 'X'
        self.ai_player_mark = 'O'

    def initialize_board(self):
        """Initializes the 6x6 game board with empty cells."""
        return [['' for _ in range(self.board_size)] for _ in range(self.board_size)]

    def make_move(self, move, player_mark):
        """Applies a move to the board for the given player.
        Move is a tuple (row, col).
        player_mark is 'X' or 'O'.
        Returns True if the move was successful, False otherwise.
        """
        row, col = move
        if 0 <= row < self.board_size and 0 <= col < self.board_size and self.board[row][col] == '':
            self.board[row][col] = player_mark
            self.switch_player()
            return True
        return False

    def get_possible_moves(self, player_mark=None):  # player_mark is not used here but kept for consistency
        """Returns a list of all possible moves (empty cells)."""
        moves = []
        for r in range(self.board_size):
            for c in range(self.board_size):
                if self.board[r][c] == '':
                    moves.append((r, c))
        return moves

    def _check_line(self, mark, count, cells):
        """Helper to check if a line (row, col, or diagonal) has 'count' marks."""
        for i in range(len(cells) - count + 1):
            if all(cells[j] == mark for j in range(i, i + count)):
                return True
        return False

    def check_win_condition(self):
        """Checks for 4 in a row, column, or diagonal. Also checks for a draw.
        Returns 'human_wins', 'ai_wins', 'draw', or None.
        """
        for i in range(self.board_size):
            row_cells = self.board[i]
            if self._check_line(self.human_player_mark, 4, row_cells):
                return "human_wins"
            if self._check_line(self.ai_player_mark, 4, row_cells):
                return "ai_wins"

            col_cells = [self.board[r][i] for r in range(self.board_size)]
            if self._check_line(self.human_player_mark, 4, col_cells):
                return "human_wins"
            if self._check_line(self.ai_player_mark, 4, col_cells):
                return "ai_wins"

        for r_start in range(self.board_size):
            for c_start in range(self.board_size):
                if r_start <= self.board_size - 4 and c_start <= self.board_size - 4:
                    diag_tl_br = [self.board[r_start + i][c_start + i] for i in range(4)]
                    if all(cell == self.human_player_mark for cell in diag_tl_br): return "human_wins"
                    if all(cell == self.ai_player_mark for cell in diag_tl_br): return "ai_wins"

                if r_start <= self.board_size - 4 and c_start >= 3:
                    diag_tr_bl = [self.board[r_start + i][c_start - i] for i in range(4)]
                    if all(cell == self.human_player_mark for cell in diag_tr_bl): return "human_wins"
                    if all(cell == self.ai_player_mark for cell in diag_tr_bl): return "ai_wins"

        if not self.get_possible_moves():
            return "draw"

        return None

    def is_game_over(self):
        """Checks if the game has ended (win or draw)."""
        return self.check_win_condition() is not None

    def evaluate_board(self, player_mark_perspective):
        winner_status = self.check_win_condition()
        if winner_status == "ai_wins":
            return 10000 if player_mark_perspective == self.ai_player_mark else -10000
        elif winner_status == "human_wins":
            return -10000 if player_mark_perspective == self.ai_player_mark else 10000
        elif winner_status == "draw":
            return 0

        def count_open_lines(mark):
            score = 0
            # Horizontal und vertikal
            for r in range(self.board_size):
                for c in range(self.board_size - 3):
                    # Horizontal
                    line = [self.board[r][c + i] for i in range(4)]
                    if line.count(mark) > 0 and line.count(
                            self.human_player_mark if mark == self.ai_player_mark else self.ai_player_mark) == 0:
                        score += pow(10, line.count(mark))
                    # Vertikal
                    line = [self.board[c + i][r] for i in range(4)]
                    if line.count(mark) > 0 and line.count(
                            self.human_player_mark if mark == self.ai_player_mark else self.ai_player_mark) == 0:
                        score += pow(10, line.count(mark))
            # Diagonal
            for r in range(self.board_size - 3):
                for c in range(self.board_size - 3):
                    line = [self.board[r + i][c + i] for i in range(4)]
                    if line.count(mark) > 0 and line.count(
                            self.human_player_mark if mark == self.ai_player_mark else self.ai_player_mark) == 0:
                        score += pow(10, line.count(mark))
            for r in range(self.board_size - 3):
                for c in range(3, self.board_size):
                    line = [self.board[r + i][c - i] for i in range(4)]
                    if line.count(mark) > 0 and line.count(
                            self.human_player_mark if mark == self.ai_player_mark else self.ai_player_mark) == 0:
                        score += pow(10, line.count(mark))
            return score

        ai_score = count_open_lines(self.ai_player_mark)
        human_score = count_open_lines(self.human_player_mark)
        return ai_score - human_score if player_mark_perspective == self.ai_player_mark else human_score - ai_score

    def get_rules(self):
        return (f"Tic-Tac-Toe (Vier gewinnt) on a {self.board_size}x{self.board_size} board.\n"
                f"Players take turns placing their mark ('{self.human_player_mark}' or '{self.ai_player_mark}').\n"
                f"The first player to get 4 of their marks in a row, column, or diagonal wins.\n"
                f"If the board is filled and no player has won, the game is a draw.\n"
                f"Human plays as '{self.human_player_mark}', AI plays as '{self.ai_player_mark}'. Human starts.")

    # In games/tic_tac_toe.py
    def clone(self):
        new_game = TicTacToe(self.board_size)
        new_game.board = [row[:] for row in self.board]
        new_game.current_player = self.current_player
        return new_game

    def get_ai_move(self):
        """Returns the AI's move using Minimax algorithm."""
        ai = Minimax(self, max_depth=3)  # Default depth, adjusted by GameController
        return ai.find_best_move(self.ai_player_mark)

    def __str__(self):
        board_str = ""
        for r in range(self.board_size):
            board_str += "|".join([mark if mark else ' ' for mark in self.board[r]]) + "\n"
            if r < self.board_size - 1:
                board_str += "-" * (self.board_size * 2 - 1) + "\n"
        return board_str

    def test_input(self):
        coords = input("Enter coordinates (x,y): ")
        x, y = coords.split(',')
        combined_coords = (int(x), int(y))
        self.make_move(combined_coords, self.human_player_mark)


if __name__ == '__main__':
    game = TicTacToe()
    difficulty = input("Max Depth: ")
    minimax_ai = Minimax(game, max_depth=int(difficulty))
    print(game.get_rules())
    print("Initial board:")
    print(game)

    while game.check_win_condition() is None:
        game.test_input()
        print(game)
        best_move = minimax_ai.find_best_move(game.ai_player_mark)
        if best_move is not None:
            game.make_move(best_move, game.ai_player_mark)
        print(game)