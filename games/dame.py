from .base_game import BaseGame

# Constants for pieces
EMPTY = ' '
HUMAN_PIECE = 'W' # White, starts
AI_PIECE = 'B'    # Black
# According to lastenheft, no kings in this simplified version.

class Dame(BaseGame):
    def __init__(self, board_size=6):
        super().__init__(board_size)
        # Human starts as per LF4040, typically White in Checkers.
        # White pieces move "up" (decreasing row index), Black pieces move "down" (increasing row index)
        self.human_player_piece = HUMAN_PIECE
        self.ai_player_piece = AI_PIECE

    def initialize_board(self):
        """Initializes the 6x6 game board for Dame.
        White (Human) pieces on the first two rows on dark squares.
        Black (AI) pieces on the last two rows on dark squares.
        Standard checkers boards have the first square (0,0 or A1) as dark.
        If (row + col) is even, it's a dark square (assuming 0-indexed).
        """
        board = [[EMPTY for _ in range(self.board_size)] for _ in range(self.board_size)]
        
        # Place AI pieces (Black) - last two rows (e.g. rows 4 and 5 for 6x6)
        for r in range(self.board_size - 2, self.board_size):
            for c in range(self.board_size):
                if (r + c) % 2 == 0: # Dark squares
                    board[r][c] = self.ai_player_piece
        
        # Place Human pieces (White) - first two rows (e.g. rows 0 and 1 for 6x6)
        for r in range(2):
            for c in range(self.board_size):
                if (r + c) % 2 == 0: # Dark squares
                    board[r][c] = self.human_player_piece
        return board

    def _is_valid_coord(self, r, c):
        return 0 <= r < self.board_size and 0 <= c < self.board_size

    def _get_player_pieces(self, player_piece):
        pieces = []
        for r in range(self.board_size):
            for c in range(self.board_size):
                if self.board[r][c] == player_piece:
                    pieces.append((r,c))
        return pieces

    def _get_opponent_piece(self, player_piece):
        return self.ai_player_piece if player_piece == self.human_player_piece else self.human_player_piece

    def get_possible_moves(self, player_piece):
        """Returns a list of all possible moves for the given player.
        Format of a move: [(from_r, from_c), (to_r, to_c), is_capture, (captured_r, captured_c) or None]
        If multiple captures: [(from_r, from_c), (mid1_r, mid1_c), (mid2_r, mid2_c), ..., (to_r, to_c), is_capture, list_of_captured_coords]
        For simplicity now: a list of single moves/captures.
        Multi-jumps need to be handled by allowing further jumps from the landing square.
        This method will first check for captures (Schlagzwang).
        If captures are available, only captures are legal moves.
        """
        moves = []
        possible_captures = []
        player_pieces_coords = self._get_player_pieces(player_piece)
        opponent_piece = self._get_opponent_piece(player_piece)

        # Determine direction based on player piece
        # Human (W) moves from higher row index to lower row index (up the board visually if row 0 is top)
        # AI (B) moves from lower row index to higher row index (down the board visually)
        # However, the problem states "Steine ziehen jeweils ein Feld vorwärts in diagonaler Richtung."
        # And "Bauern auf der jeweiligen Grundlinie". Let's assume Human is at bottom (rows 4,5) moving to row 0.
        # And AI is at top (rows 0,1) moving to row 5. This matches Bauernschach description for "gegnerische Grundlinie".
        # Re-evaluating initial_board setup if this is the case. 
        # The current setup: AI (Black) at rows 4,5. Human (White) at rows 0,1.
        # So, Human (White, rows 0,1) moves towards row 5 (increasing row index).
        # AI (Black, rows 4,5) moves towards row 0 (decreasing row index).

        direction = 1 if player_piece == self.human_player_piece else -1

        for r, c in player_pieces_coords:
            # Check for captures first
            for dr in [-1, 1]: # Change in row for diagonal capture
                for dc in [-1, 1]: # Change in col for diagonal capture
                    jump_r, jump_c = r + dr, c + dc                 # Opponent piece
                    land_r, land_c = r + 2*dr, c + 2*dc             # Landing square

                    if self._is_valid_coord(land_r, land_c) and \
                       self.board[land_r][land_c] == EMPTY and \
                       self._is_valid_coord(jump_r, jump_c) and \
                       self.board[jump_r][jump_c] == opponent_piece:
                        # Check if this capture is in the forward direction for a simple piece
                        if dr == direction:
                             possible_captures.append( [(r,c), (land_r, land_c), (jump_r, jump_c)] )
        
        if possible_captures: # Schlagzwang - only captures are allowed
            # TODO: Handle multi-jumps. For now, just return single jumps.
            # A real multi-jump would mean the `to_pos` of a capture becomes the `from_pos` for a subsequent one.
            # The `make_move` would need to handle removing multiple pieces.
            # For now, a move is represented as [from, to, captured_piece_coord]
            return [["capture", move[0], move[1], [move[2]]] for move in possible_captures]

        # If no captures, check for simple moves
        for r, c in player_pieces_coords:
            for dc in [-1, 1]: # Diagonal columns
                to_r, to_c = r + direction, c + dc
                if self._is_valid_coord(to_r, to_c) and self.board[to_r][to_c] == EMPTY:
                    moves.append( ["move", (r,c), (to_r, to_c)] )
        return moves

    def make_move(self, move_info, player_piece_making_move):
        """Applies a move to the board.
        move_info is [type, from_pos, to_pos, list_of_captured_coords_if_capture]
        type is "move" or "capture".
        Returns True if successful.
        """
        move_type, from_pos, to_pos = move_info[0], move_info[1], move_info[2]
        from_r, from_c = from_pos
        to_r, to_c = to_pos

        if self.board[from_r][from_c] != player_piece_making_move:
            # print(f"Error: Piece at {from_pos} is not {player_piece_making_move}")
            return False # Trying to move opponent's piece or empty square

        self.board[to_r][to_c] = player_piece_making_move
        self.board[from_r][from_c] = EMPTY

        if move_type == "capture":
            captured_coords_list = move_info[3]
            for cap_r, cap_c in captured_coords_list:
                self.board[cap_r][cap_c] = EMPTY
            
            # After a capture, check if further captures are possible from to_pos by the same piece
            # This is essential for multi-jumps. The game turn only ends when no more captures for that piece.
            # For now, this is simplified: one jump per `make_move` call from `get_possible_moves`.
            # A more complex game loop would handle multi-jumps.

        self.switch_player() # Player turn switches after a move sequence.
        return True

    def check_win_condition(self):
        """Checks win conditions:
        - Player places a stone on the opponent's back rank.
        - Opponent has no more pieces.
        - Opponent has no more legal moves.
        Returns 'human_wins', 'ai_wins', or None (game ongoing).
        Draw is not possible in this variant.
        """
        human_pieces = 0
        ai_pieces = 0

        for r in range(self.board_size):
            for c in range(self.board_size):
                if self.board[r][c] == self.human_player_piece:
                    human_pieces += 1
                    # Human (White) wins if reaches AI's back rank (row self.board_size - 1)
                    if r == self.board_size - 1:
                        return "human_wins"
                elif self.board[r][c] == self.ai_player_piece:
                    ai_pieces += 1
                    # AI (Black) wins if reaches Human's back rank (row 0)
                    if r == 0:
                        return "ai_wins"
        
        if human_pieces == 0:
            return "ai_wins"
        if ai_pieces == 0:
            return "human_wins"

        # Check for no legal moves for the current player whose turn it would be NEXT
        # The player who just moved is self.current_player. We need to check for the *other* player.
        next_player_to_move_piece = self.ai_player_piece if self.current_player == "human" else self.human_player_piece
        
        # Important: get_possible_moves should be called for the player whose turn it is *about* to be.
        # However, switch_player() is called at the end of make_move.
        # So, self.current_player is ALREADY the next player.
        possible_moves_for_current_player = self.get_possible_moves(self.current_player_piece)

        if not possible_moves_for_current_player:
            if self.current_player == "human": # Human cannot move
                return "ai_wins"
            else: # AI cannot move
                return "human_wins"

        return None # Game ongoing

    @property
    def current_player_piece(self):
        return self.human_player_piece if self.current_player == "human" else self.ai_player_piece

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

        human_score = 0
        ai_score = 0
        
        human_pieces_count = 0
        ai_pieces_count = 0

        for r in range(self.board_size):
            for c in range(self.board_size):
                piece = self.board[r][c]
                if piece == self.human_player_piece:
                    human_pieces_count +=1
                    # Add score for advancement (closer to AI's back rank)
                    human_score += (r + 1) # Row 0 = 1 point, Row 5 = 6 points
                elif piece == self.ai_player_piece:
                    ai_pieces_count +=1
                    # Add score for advancement (closer to Human's back rank - row 0)
                    ai_score += (self.board_size - r) # Row 5 = 1 point, Row 0 = 6 points

        piece_diff_score = human_pieces_count - ai_pieces_count
        advancement_score = human_score - ai_score # Human positive, AI negative from human perspective

        # Combine scores
        total_score = piece_diff_score * 10 + advancement_score # Weight piece difference more

        if player_piece_perspective == self.human_player_piece:
            return total_score
        else: # AI's perspective
            return -total_score

    def get_rules(self):
        return (
            f"Dame (Simplified Checkers) on a {self.board_size}x{self.board_size} board.\n"
            f"Played only on dark squares. Human is '{self.human_player_piece}' (White), AI is '{self.ai_player_piece}' (Black).\n"
            f"Human starts from rows 0,1 (top) and moves towards row 5 (downwards on board model).\n"
            f"AI starts from rows {self.board_size-2},{self.board_size-1} (bottom) and moves towards row 0 (upwards on board model).\n"
            f"Pieces move one step diagonally forward. Capturing is mandatory (Schlagzwang).\n"
            f"To capture, jump over an opponent's piece to an empty square immediately behind it.\n"
            f"Multiple jumps in a single turn are possible if available after a capture (not fully implemented in basic AI move selection yet, but structure allows).\n"
            f"Win: Reach the opponent's back rank, or if the opponent has no pieces or no legal moves.\n"
            f"No draws."
        )

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
    human_moves = game.get_possible_moves(game.human_player_piece)
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
    game_cap.board[2][2] = HUMAN_PIECE # W
    game_cap.board[3][3] = AI_PIECE    # B
    game_cap.current_player = "human"
    print("\nBoard for capture test:")
    print(game_cap)
    capture_moves = game_cap.get_possible_moves(HUMAN_PIECE)
    print(f"Capture moves for Human (W) from (2,2): {capture_moves}")
    if capture_moves:
        # Expected: [['capture', (2,2), (4,4), [(3,3)]]]
        game_cap.make_move(capture_moves[0], HUMAN_PIECE)
        print("Board after capture:")
        print(game_cap)
        print(f"Piece at (3,3) (captured): '{game_cap.board[3][3]}'")
        print(f"Piece at (4,4) (moved): '{game_cap.board[4][4]}'")
        print(f"Current player after capture: {game_cap.current_player}") # Should be AI
    else:
        print("No capture moves found, check logic.")

    # Test win by reaching back rank
    game_win_rank = Dame()
    game_win_rank.board = [[EMPTY for _ in range(6)] for _ in range(6)]
    game_win_rank.board[4][0] = HUMAN_PIECE # Human piece close to AI back rank (row 5)
    game_win_rank.current_player = "human"
    print("\nBoard for win by rank test (Human to move from (4,0) to (5,1)):")
    print(game_win_rank)
    win_move = ["move", (4,0), (5,1)] # Manually create this move
    # Need to ensure get_possible_moves would generate this
    possible_moves_for_win = game_win_rank.get_possible_moves(HUMAN_PIECE)
    print(f"Possible moves: {possible_moves_for_win}")
    # We assume (5,1) is a valid move from (4,0)
    game_win_rank.make_move(win_move, HUMAN_PIECE)
    print("Board after move to back rank:")
    print(game_win_rank)
    print(f"Win condition: {game_win_rank.check_win_condition()}") # Should be human_wins

    # Test win by no pieces
    game_no_pieces = Dame()
    game_no_pieces.board = [[EMPTY for _ in range(6)] for _ in range(6)]
    game_no_pieces.board[0][0] = HUMAN_PIECE # Only one human piece
    # AI has no pieces. check_win_condition is called after a move. Let's simulate AI's turn.
    game_no_pieces.current_player = "ai" # It's AI's turn but AI has no pieces.
    # The check_win_condition should detect this
    # Or, get_possible_moves for AI will be empty. Let's adjust current_player for the check
    print("\nBoard for win by no opponent pieces (Human has one piece, AI has none):")
    print(game_no_pieces)
    print(f"Win condition (AI's turn, no AI pieces): {game_no_pieces.check_win_condition()}")

    # Test win by no moves
    game_no_moves = Dame()
    game_no_moves.board = [[EMPTY for _ in range(6)] for _ in range(6)]
    game_no_moves.board[0][0] = AI_PIECE # AI piece at corner
    game_no_moves.board[1][1] = HUMAN_PIECE # Blocker
    game_no_moves.current_player = "ai" # AI's turn, but cannot move
    print("\nBoard for win by no moves (AI blocked):")
    print(game_no_moves)
    print(f"Possible AI moves: {game_no_moves.get_possible_moves(AI_PIECE)}")
    print(f"Win condition (AI cannot move): {game_no_moves.check_win_condition()}") 