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
            return True
        return False

    def get_possible_moves(self, player_mark=None): # player_mark is not used here but kept for consistency
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
        # Check rows and columns for 4 in a line
        for i in range(self.board_size):
            # Check row i
            row_cells = self.board[i]
            if self._check_line(self.human_player_mark, 4, row_cells):
                return "human_wins"
            if self._check_line(self.ai_player_mark, 4, row_cells):
                return "ai_wins"
            
            # Check column i
            col_cells = [self.board[r][i] for r in range(self.board_size)]
            if self._check_line(self.human_player_mark, 4, col_cells):
                return "human_wins"
            if self._check_line(self.ai_player_mark, 4, col_cells):
                return "ai_wins"

        # Check diagonals for 4 in a line
        # Iterate over all possible starting cells for diagonals
        for r_start in range(self.board_size):
            for c_start in range(self.board_size):
                # Check \ diagonal (top-left to bottom-right)
                if r_start <= self.board_size - 4 and c_start <= self.board_size - 4:
                    diag_tl_br = [self.board[r_start+i][c_start+i] for i in range(4)]
                    if all(cell == self.human_player_mark for cell in diag_tl_br): return "human_wins"
                    if all(cell == self.ai_player_mark for cell in diag_tl_br): return "ai_wins"
                
                # Check / diagonal (top-right to bottom-left)
                # To check from (r_start, c_start) going down-left
                # This means r increases, c decreases.
                # So, self.board[r_start+i][c_start-i]
                # Bounds: r_start+i < board_size, c_start-i >= 0
                # For a line of 4: r_start+3 < board_size, c_start-3 >= 0
                # So, r_start <= board_size - 4 AND c_start >= 3
                if r_start <= self.board_size - 4 and c_start >= 3:
                    diag_tr_bl = [self.board[r_start+i][c_start-i] for i in range(4)]
                    if all(cell == self.human_player_mark for cell in diag_tr_bl): return "human_wins"
                    if all(cell == self.ai_player_mark for cell in diag_tr_bl): return "ai_wins"

        # Check for draw (board full and no winner)
        if not self.get_possible_moves():
            return "draw"

        return None # Game is ongoing

    def is_game_over(self):
        """Checks if the game has ended (win or draw)."""
        return self.check_win_condition() is not None

    def evaluate_board(self, player_mark_perspective):
        """Evaluates the board state for the Minimax algorithm.
        Simple evaluation: +1 for AI win, -1 for Human win, 0 otherwise.
        player_mark_perspective is the mark of the player for whom we evaluate (e.g., AI's mark).
        """
        winner_status = self.check_win_condition()
        if winner_status == "ai_wins":
            return 1 if player_mark_perspective == self.ai_player_mark else -1
        elif winner_status == "human_wins":
            return -1 if player_mark_perspective == self.ai_player_mark else 1
        # elif winner_status == "draw":
        return 0 # Draw or ongoing

    def get_rules(self):
        return (f"Tic-Tac-Toe (Vier gewinnt) on a {self.board_size}x{self.board_size} board.\n"
                f"Players take turns placing their mark ('{self.human_player_mark}' or '{self.ai_player_mark}').\n"
                f"The first player to get 4 of their marks in a row, column, or diagonal wins.\n"
                f"If the board is filled and no player has won, the game is a draw.\n"
                f"Human plays as '{self.human_player_mark}', AI plays as '{self.ai_player_mark}'. Human starts.")

    def __str__(self):
        board_str = ""
        for r in range(self.board_size):
            board_str += "|".join([mark if mark else ' ' for mark in self.board[r]]) + "\n"
            if r < self.board_size - 1:
                board_str += "-" * (self.board_size * 2 - 1) + "\n"
        return board_str

    # Dumme Methode zum Testen der Eingabe bevor das Frontend fertig ist.
    def test_input(self):
        coords = input("Enter coordinates (x,y): ")
        x, y = coords.split(',')
        combined_coords = (int(x), int(y))
        game.make_move(combined_coords, self.human_player_mark)

# Example Usage (for testing)
if __name__ == '__main__':
    game = TicTacToe()
    minimax_ai = Minimax(game, max_depth=3)  # AI with depth 3
    print(game.get_rules())
    print("Initial board:")
    print(game)

    # Main game loop
    while game.check_win_condition() is None:
        game.test_input()
        print(game)
        best_move = minimax_ai.find_best_move(game.ai_player_mark)
        if best_move is not None:
            game.make_move(best_move, game.ai_player_mark)
        print(game)



    # # Example moves
    # game.make_move((0, 0), game.human_player_mark) # Human
    # print(game)
    # game.make_move((1, 1), game.ai_player_mark)     # AI
    # print(game)
    # game.make_move((0, 1), game.human_player_mark) # Human
    # print(game)
    # game.make_move((1, 2), game.ai_player_mark)     # AI
    # print(game)
    # game.make_move((0, 2), game.human_player_mark) # Human
    # print(game)
    # game.make_move((1, 0), game.ai_player_mark)     # AI
    # print(game)
    # game.make_move((0, 3), game.human_player_mark) # Human - Win attempt
    # print(game)
    #
    # print(f"Possible moves: {game.get_possible_moves()}")
    # print(f"Game over: {game.is_game_over()}")
    # print(f"Win condition: {game.check_win_condition()}")
    # print(f"Board evaluation for AI ({game.ai_player_mark}): {game.evaluate_board(game.ai_player_mark)}")
    # print(f"Board evaluation for Human ({game.human_player_mark}): {game.evaluate_board(game.human_player_mark)}")
    #
    # # Test win
    # game_win = TicTacToe()
    # game_win.make_move((0,0), game_win.human_player_mark)
    # game_win.make_move((1,0), game_win.ai_player_mark)
    # game_win.make_move((0,1), game_win.human_player_mark)
    # game_win.make_move((1,1), game_win.ai_player_mark)
    # game_win.make_move((0,2), game_win.human_player_mark)
    # game_win.make_move((1,2), game_win.ai_player_mark)
    # game_win.make_move((0,3), game_win.human_player_mark) # Human wins
    # print("\nTest Win Scenario:")
    # print(game_win)
    # print(f"Game over: {game_win.is_game_over()}")
    # print(f"Win condition: {game_win.check_win_condition()}")
    #
    # # Test draw
    # game_draw = TicTacToe()
    # marks = [game_draw.human_player_mark, game_draw.ai_player_mark]
    # idx = 0
    # for r in range(game_draw.board_size):
    #     for c in range(game_draw.board_size):
    #         # Create a pattern that doesn't lead to an early win for 4-in-a-row
    #         if not ((r < 4 and all(game_draw.board[r][k] == marks[idx%2] for k in range(c))) or \
    #                 (c < 4 and all(game_draw.board[k][c] == marks[idx%2] for k in range(r)))):
    #             # A simple alternating pattern that avoids immediate wins for this test
    #             # This is not a perfect draw-forcing sequence, just for filling the board.
    #             if (r%2 == 0 and c%2 == 0) or (r%2 !=0 and c%2 !=0) :
    #                 game_draw.make_move((r,c), marks[0]) # Human
    #             else:
    #                 game_draw.make_move((r,c), marks[1]) # AI
    #         idx +=1
    #         # This filling logic is too simple and might still result in a win.
    #         # A true draw setup needs careful placement or filling all spots then checking.
    #
    # # Let's just fill the board alternatingly for a draw test, might result in a win though.
    # game_draw_simple = TicTacToe()
    # current_mark_idx = 0
    # for r_draw in range(game_draw_simple.board_size):
    #     for c_draw in range(game_draw_simple.board_size):
    #         if game_draw_simple.check_win_condition() is None:
    #              game_draw_simple.make_move((r_draw, c_draw), [game_draw_simple.human_player_mark, game_draw_simple.ai_player_mark][current_mark_idx])
    #              current_mark_idx = 1 - current_mark_idx # Switch mark
    #         else:
    #             break
    #     if game_draw_simple.check_win_condition() is not None:
    #         break
    #
    # print("\nTest Draw/Full Scenario:")
    # print(game_draw_simple)
    # print(f"Game over: {game_draw_simple.is_game_over()}")
    # print(f"Win condition: {game_draw_simple.check_win_condition()}")