from .base_game import BaseGame

# Constants for pieces
EMPTY = '_'
HUMAN_PIECE = 'W'  # White, starts
AI_PIECE = 'B'  # Black


class Dame(BaseGame):
    def __init__(self, board_size=6):
        self.human_player_piece = HUMAN_PIECE
        self.ai_player_piece = AI_PIECE
        # Track piece positions to avoid full board scans
        self.human_pieces = set()
        self.ai_pieces = set()
        super().__init__(board_size)

    def initialize_board(self):
        """Initializes the 6x6 game board for Dame.
        White (Human) pieces on the first two rows on dark squares.
        Black (AI) pieces on the last two rows on dark squares.
        Standard checkers boards have the first square (0,0 or A1) as dark.
        If (row + col) is even, it's a dark square (assuming 0-indexed).
        """
        board = [[EMPTY for _ in range(self.board_size)] for _ in range(self.board_size)]

        # Clear piece tracking sets
        self.human_pieces.clear()
        self.ai_pieces.clear()

        # Place AI pieces (Black) - last two rows (e.g. rows 4 and 5 for 6x6)
        for row in range(self.board_size - 2, self.board_size):
            for col in range(self.board_size):
                if (row + col) % 2 == 0:  # Dark squares
                    board[row][col] = self.ai_player_piece
                    self.ai_pieces.add((row, col))

        # Place Human pieces (White) - first two rows (e.g. rows 0 and 1 for 6x6)
        for row in range(2):
            for col in range(self.board_size):
                if (row + col) % 2 == 0:  # Dark squares
                    board[row][col] = self.human_player_piece
                    self.human_pieces.add((row, col))
        return board

    def _is_valid_coord(self, r, c):
        return 0 <= r < self.board_size and 0 <= c < self.board_size

    def _get_opponent_piece(self, player_piece):
        return self.ai_player_piece if player_piece == self.human_player_piece else self.human_player_piece

    def get_all_possible_moves(self, player_piece):
        """Returns a list of all possible moves for the given player.
        Format of a move: ["move", (from_r, from_c), (to_r, to_c)] for regular moves
        or ["capture", (from_r, from_c), (to_r, to_c), [(captured_r, captured_c)]] for captures.
        This method will first check for captures (Schlagzwang).
        If captures are available, only captures are legal moves.
        """
        # Get player's pieces and direction
        pieces = self.human_pieces if player_piece == self.human_player_piece else self.ai_pieces
        direction = 1 if player_piece == self.human_player_piece else -1
        opponent_piece = self._get_opponent_piece(player_piece)

        # First check for captures (Schlagzwang)
        captures = self._get_possible_captures(pieces, opponent_piece, direction)
        if captures:
            return captures

        # If no captures, check for regular moves
        return self._get_regular_moves(pieces, direction)

    def get_possible_moves(self, piece_coord):
        """Returns a list of all possible moves for the specific piece at the given coordinates.
        Format of a move: ["move", (from_r, from_c), (to_r, to_c)] for regular moves
        or ["capture", (from_r, from_c), (to_r, to_c), [(captured_r, captured_c)]] for captures.
        """
        row, col = piece_coord

        # Verify if there's a player piece at the given coordinates
        if not self._is_valid_coord(row, col) or self.board[row][col] == EMPTY:
            return []

        player_piece = self.board[row][col]
        direction = 1 if player_piece == self.human_player_piece else -1
        opponent_piece = self._get_opponent_piece(player_piece)

        # Check for captures first (Schlagzwang)
        captures = self._get_possible_captures_for_piece((row, col), opponent_piece, direction)
        if captures:
            return captures

        # If no captures, check for regular moves
        return self._get_regular_moves_for_piece((row, col), direction)

    def _get_possible_captures(self, pieces, opponent_piece, direction):
        """Helper method to find all possible captures for all pieces."""
        possible_captures = []

        for row, col in pieces:
            piece_captures = self._get_possible_captures_for_piece((row, col), opponent_piece, direction)
            possible_captures.extend(piece_captures)

        return possible_captures

    def _get_possible_captures_for_piece(self, piece_coord, opponent_piece, direction):
        """Helper method to find all possible captures for a specific piece."""
        possible_captures = []
        row, col = piece_coord

        # Check for captures in all diagonal directions
        for drow in [-1, 1]:  # Change in row for diagonal capture
            for dcol in [-1, 1]:  # Change in col for diagonal capture
                jump_row, jump_col = row + drow, col + dcol  # Opponent piece
                land_row, land_col = row + 2 * drow, col + 2 * dcol  # Landing square

                if self._is_valid_coord(land_row, land_col) and \
                        self.board[land_row][land_col] == EMPTY and \
                        self._is_valid_coord(jump_row, jump_col) and \
                        self.board[jump_row][jump_col] == opponent_piece:
                    # Check if this capture is in the forward direction
                    if drow == direction:
                        possible_captures.append(["capture", (row, col), (land_row, land_col), [(jump_row, jump_col)]])

        return possible_captures

    def _get_regular_moves(self, pieces, direction):
        """Helper method to find all regular moves for all pieces."""
        moves = []

        for row, col in pieces:
            piece_moves = self._get_regular_moves_for_piece((row, col), direction)
            moves.extend(piece_moves)

        return moves

    def _get_regular_moves_for_piece(self, piece_coord, direction):
        """Helper method to find all regular moves for a specific piece."""
        moves = []
        row, col = piece_coord

        # Check diagonal forward moves
        for dcol in [-1, 1]:  # Diagonal columns
            to_row, to_col = row + direction, col + dcol
            if self._is_valid_coord(to_row, to_col) and self.board[to_row][to_col] == EMPTY:
                moves.append(["move", (row, col), (to_row, to_col)])

        return moves

    def _check_further_captures(self, r_start, c_start, piece_making_move):
        """
        Checks if the piece at (r_start, c_start) belonging to piece_making_move
        has any further *forward* capture moves available.
        Returns True if further captures are possible, False otherwise.
        """
        opponent_piece = self._get_opponent_piece(piece_making_move)
        # Determine forward direction for the current piece for a non-king piece
        # Human (W) moves towards increasing row index (+1).
        # AI (B) moves towards decreasing row index (-1).
        piece_forward_direction = 1 if piece_making_move == self.human_player_piece else -1

        # dr_one_step is the change in row to reach the opponent's square
        # dc_one_step is the change in col to reach the opponent's square
        for dr_one_step in [-1, 1]: 
            for dc_one_step in [-1, 1]: 
                # This is the crucial check for "forward" capture for a simple piece
                if dr_one_step != piece_forward_direction:
                    continue

                opponent_r, opponent_c = r_start + dr_one_step, c_start + dc_one_step
                land_r, land_c = r_start + 2*dr_one_step, c_start + 2*dc_one_step

                if self._is_valid_coord(land_r, land_c) and \
                   self.board[land_r][land_c] == EMPTY and \
                   self._is_valid_coord(opponent_r, opponent_c) and \
                   self.board[opponent_r][opponent_c] == opponent_piece:
                    return True # Found at least one valid forward capture
        
        return False # No further forward captures found

    def make_move(self, move_info, player_piece_making_move):
        """Applies a move to the board.
        move_info is [type, from_pos, to_pos, list_of_captured_coords_if_capture]
        type is "move" or "capture".
        Returns a tuple: (bool: move_was_valid, bool: further_capture_possible_for_same_player)
        """
        move_type, from_pos, to_pos = move_info[0], move_info[1], move_info[2]
        from_r, from_c = from_pos
        to_r, to_c = to_pos

        if not self._is_valid_coord(from_r, from_c) or \
           self.board[from_r][from_c] != player_piece_making_move:
            # print(f"Error: Piece at {from_pos} is not {player_piece_making_move} or invalid coord.")
            return False, False # Trying to move opponent's piece, empty square, or invalid from_pos

        # Assuming get_possible_moves ensures to_pos is valid and empty.
        # If direct calls to make_move are possible, more validation for to_pos might be needed.

        self.board[to_r][to_c] = player_piece_making_move
        self.board[from_r][from_c] = EMPTY
        
        further_capture_possible = False

        if move_type == "capture":
            # Ensure move_info has the captured piece coordinates for a capture type
            if len(move_info) < 4 or not isinstance(move_info[3], list):
                # This indicates an issue with how move_info was constructed.
                # Revert board changes for atomicity or log critical error.
                self.board[from_r][from_c] = player_piece_making_move # Revert piece move
                self.board[to_r][to_c] = EMPTY # Revert landing square
                # print("Error: Capture move_info malformed.")
                return False, False # Move considered invalid due to bad data

            captured_coords_list = move_info[3]
            for cap_r, cap_c in captured_coords_list:
                # Assuming get_possible_moves ensures captured_coords are valid and contain opponent pieces.
                # If not, add validation for cap_r, cap_c and self.board[cap_r][cap_c].
                self.board[cap_r][cap_c] = EMPTY # Remove captured piece
            
            if self._check_further_captures(to_r, to_c, player_piece_making_move):
                further_capture_possible = True
                # Player DOES NOT switch if a chain capture is possible/mandatory
            else:
                self.switch_player() # Current player's turn ends
        
        elif move_type == "move":
            self.switch_player() # Current player's turn ends
            # No further captures possible after a simple move due to Schlagzwang
        
        else: # Unknown move_type
            # Revert board changes for atomicity
            self.board[from_r][from_c] = player_piece_making_move
            self.board[to_r][to_c] = EMPTY
            # print(f"Error: Unknown move_type '{move_type}'.")
            return False, False # Move is invalid

        return True, further_capture_possible

    def check_win_condition(self):
        """Checks win conditions:
        - Player places a stone on the opponent's back rank.
        - Opponent has no more pieces.
        - Opponent has no more legal moves.
        Returns 'human_wins', 'ai_wins', or None (game ongoing).
        Draw is not possible in this variant.
        """
        # Check for pieces on opponent's back rank
        for r, c in self.human_pieces:
            # Human (White) wins if reaches AI's back rank (row self.board_size - 1)
            if r == self.board_size - 1:
                return "human_wins"

        for r, c in self.ai_pieces:
            # AI (Black) wins if reaches Human's back rank (row 0)
            if r == 0:
                return "ai_wins"

        # Check for no pieces
        if not self.human_pieces:
            return "ai_wins"
        if not self.ai_pieces:
            return "human_wins"

        # Check for no legal moves for the current player
        possible_moves_for_current_player = self.get_all_possible_moves(self.current_player_piece)

        if not possible_moves_for_current_player:
            if self.current_player == "human":  # Human cannot move
                return "ai_wins"
            else:  # AI cannot move
                return "human_wins"

        return None  # Game ongoing

    @property
    def current_player_piece(self):
        return self.human_player_piece if self.current_player == "human" else self.ai_player_piece

    def get_ai_move(self):
        """Returns the AI's move based on the current board state.
        Uses the Minimax algorithm to find the best move.
        """
        from ai.minimax import Minimax
        ai = Minimax(self, max_depth=3)
        return ai.find_best_move(self.ai_player_piece)

    def is_game_over(self):
        return self.check_win_condition() is not None

    def evaluate_board(self, player_piece_perspective):
        """Evaluates the board state for Minimax.
        Factors: piece count, advancement, potential captures (not yet).
        +score good for player_piece_perspective, -score bad.
        """
        win_status = self.check_win_condition()
        # If game is decided, that's the ultimate evaluation
        if win_status == "human_wins":
            return -float('inf') if player_piece_perspective == self.ai_player_piece else float('inf')
        if win_status == "ai_wins":
            return float('inf') if player_piece_perspective == self.ai_player_piece else -float('inf')

        # Calculate piece count advantage
        human_pieces_count = len(self.human_pieces)
        ai_pieces_count = len(self.ai_pieces)
        piece_diff_score = human_pieces_count - ai_pieces_count

        # Calculate advancement score
        human_score = sum(r + 1 for r, c in self.human_pieces)  # Row 0 = 1 point, Row 5 = 6 points
        ai_score = sum(self.board_size - r for r, c in self.ai_pieces)  # Row 5 = 1 point, Row 0 = 6 points
        advancement_score = human_score - ai_score  # Human positive, AI negative from human perspective

        # Combine scores
        total_score = piece_diff_score * 10 + advancement_score  # Weight piece difference more

        if player_piece_perspective == self.human_player_piece:
            return total_score
        else:  # AI's perspective
            return -total_score

    def get_rules(self):
        return [
            "Ziehen: diagonal 1 Feld vorwärts",
            "Schlagen (Pflicht): Diagonal über Gegner auf freies Feld",
            "Mehrfachschläge sind erlaubt & verpflichtend",
            "Kein Springen über eigene Steine",
            "Sieg: Gegner kann nicht ziehen oder Grundlinie mit eigenem Stein erreicht",
        ]

    def __str__(self):
        s = "  " + " ".join(map(str, range(self.board_size))) + "\n"
        for r in range(self.board_size):
            s += str(r) + " " + "|".join(self.board[r]) + "\n"
        return s


# Example Usage:
if __name__ == '__main__':
    game = Dame()
    print(game.get_rules())
    print("Initial board:")
    print(game)

    print(f"Current player: {game.current_player} ({game.current_player_piece})")

    # Test initial possible moves for Human (W)
    human_moves = game.get_all_possible_moves(game.human_player_piece)
    print(f"Possible moves for Human ({game.human_player_piece}): {len(human_moves)}")
    # for move in human_moves:
    #     print(move)

    # Example: Manually make a move to test logic (Human: (1,0) -> (2,1))
    # Assuming (1,0) is a white piece and (2,1) is empty and a valid move.
    # First, check if (1,0) holds a human piece (W). Dark squares are (r+c)%2==0
    # (1,0) -> 1+0=1 (light), so (1,1) -> 1+1=2 (dark) or (0,0) etc.
    # Human pieces at row 0: (0,0), (0,2), (0,4)
    # Human pieces at row 1: (1,1), (1,3), (1,5)
    # A valid first move for W could be from (1,1) to (2,0) or (2,2).
    if human_moves:
        print(f"Example Human move: {human_moves[0]}")
        # game.make_move(human_moves[0], game.human_player_piece)
        # print("Board after Human move:")
        # print(game)
        # print(f"Current player: {game.current_player} ({game.current_player_piece})")

        # ai_moves = game.get_possible_moves(game.ai_player_piece)
        # print(f"Possible moves for AI ({game.ai_player_piece}): {len(ai_moves)}")
        # if ai_moves:
        #     print(f"Example AI move: {ai_moves[0]}")
        # game.make_move(ai_moves[0], game.ai_player_piece)
        # print("Board after AI move:")
        # print(game)
        # print(f"Current player: {game.current_player} ({game.current_player_piece})")
    else:
        print("No initial moves for Human? Check board setup or get_possible_moves logic.")

    # Test Capture Scenario
    # Setup: Human W at (2,2), AI B at (3,3), Human to move. Landing (4,4)
    game_cap = Dame()
    game_cap.board = [[EMPTY for _ in range(6)] for _ in range(6)]
    game_cap.board[2][2] = HUMAN_PIECE  # W
    game_cap.board[3][3] = AI_PIECE  # B
    game_cap.current_player = "human"
    print("\nBoard for capture test:")
    print(game_cap)
    capture_moves = game_cap.get_all_possible_moves(HUMAN_PIECE)
    print(f"Capture moves for Human (W) from (2,2): {capture_moves}")
    if capture_moves:
        # Expected: [['capture', (2,2), (4,4), [(3,3)]]]
        game_cap.make_move(capture_moves[0], HUMAN_PIECE)
        print("Board after capture:")
        print(game_cap)
        print(f"Piece at (3,3) (captured): '{game_cap.board[3][3]}'")
        print(f"Piece at (4,4) (moved): '{game_cap.board[4][4]}'")
        print(f"Current player after capture: {game_cap.current_player}")  # Should be AI
    else:
        print("No capture moves found, check logic.")

    # Test win by reaching back rank
    game_win_rank = Dame()
    game_win_rank.board = [[EMPTY for _ in range(6)] for _ in range(6)]
    game_win_rank.board[4][0] = HUMAN_PIECE  # Human piece close to AI back rank (row 5)
    game_win_rank.current_player = "human"
    print("\nBoard for win by rank test (Human to move from (4,0) to (5,1)):")
    print(game_win_rank)
    win_move = ["move", (4, 0), (5, 1)]  # Manually create this move
    # Need to ensure get_possible_moves would generate this
    possible_moves_for_win = game_win_rank.get_all_possible_moves(HUMAN_PIECE)
    print(f"Possible moves: {possible_moves_for_win}")
    # We assume (5,1) is a valid move from (4,0)
    game_win_rank.make_move(win_move, HUMAN_PIECE)
    print("Board after move to back rank:")
    print(game_win_rank)
    print(f"Win condition: {game_win_rank.check_win_condition()}")  # Should be human_wins

    # Test win by no pieces
    game_no_pieces = Dame()
    game_no_pieces.board = [[EMPTY for _ in range(6)] for _ in range(6)]
    game_no_pieces.board[0][0] = HUMAN_PIECE  # Only one human piece
    # AI has no pieces. check_win_condition is called after a move. Let's simulate AI's turn.
    game_no_pieces.current_player = "ai"  # It's AI's turn but AI has no pieces.
    # The check_win_condition should detect this
    # Or, get_possible_moves for AI will be empty. Let's adjust current_player for the check
    print("\nBoard for win by no opponent pieces (Human has one piece, AI has none):")
    print(game_no_pieces)
    print(f"Win condition (AI's turn, no AI pieces): {game_no_pieces.check_win_condition()}")

    # Test win by no moves
    game_no_moves = Dame()
    game_no_moves.board = [[EMPTY for _ in range(6)] for _ in range(6)]
    game_no_moves.board[0][0] = AI_PIECE  # AI piece at corner
    game_no_moves.board[1][1] = HUMAN_PIECE  # Blocker
    game_no_moves.current_player = "ai"  # AI's turn, but cannot move
    print("\nBoard for win by no moves (AI blocked):")
    print(game_no_moves)
    print(f"Possible AI moves: {game_no_moves.get_all_possible_moves(AI_PIECE)}")
    print(f"Win condition (AI cannot move): {game_no_moves.check_win_condition()}")
