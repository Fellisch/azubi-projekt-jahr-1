# Dame Game Logic Documentation (`games/dame.py`)

This document describes the game logic for Dame (Checkers) as implemented in `games/dame.py`.

## Class: `Dame`

Inherits from `BaseGame`.

### Constants Defined at Module Level:

*   `EMPTY` (str): Represents an empty square on the board (e.g., '_').
*   `HUMAN_PIECE` (str): Represents the human player's piece (e.g., 'W' for White).
*   `AI_PIECE` (str): Represents the AI player's piece (e.g., 'B' for Black).

### Attributes:

*   `human_player_piece` (str): Stores the character for the human's pieces.
*   `ai_player_piece` (str): Stores the character for the AI's pieces.
*   `human_pieces` (set):
    *   A set of tuples, where each tuple `(r, c)` represents the 0-indexed row and column of a human player's piece.
    *   Used for efficient lookups and win condition checks.
*   `ai_pieces` (set):
    *   A set of tuples, similar to `human_pieces`, but for the AI player's pieces.
*   Inherited from `BaseGame`:
    *   `board_size` (int): The dimension of the square board (e.g., 6 for a 6x6 board).
    *   `board` (list of lists): The 2D list representing the game board.
    *   `current_player` (str): String indicating whose turn it is ("human" or "ai").

### Methods:

#### `__init__(self, board_size=6)`
*   **Purpose:** Initializes the Dame game.
*   **Parameters:**
    *   `board_size` (optional, default: 6): The size of one side of the game board.
*   **Functionality:** Sets up player pieces, initializes empty sets for `human_pieces` and `ai_pieces`, and calls the `super().__init__(board_size)` which in turn calls `initialize_board()`.

#### `initialize_board(self)`
*   **Purpose:** Sets up the initial state of the game board with pieces in their starting positions.
*   **Returns:** A 2D list representing the initialized board.
*   **Functionality:**
    1.  Creates an empty board of `board_size` x `board_size`.
    2.  Clears `human_pieces` and `ai_pieces` sets.
    3.  Places AI pieces (e.g., Black) on the dark squares of the last two rows.
    4.  Places Human pieces (e.g., White) on the dark squares of the first two rows.
    5.  Populates the `human_pieces` and `ai_pieces` sets with the coordinates of the placed pieces.

#### `_is_valid_coord(self, r, c)`
*   **Purpose:** (Internal helper) Checks if given row `r` and column `c` are within the board boundaries.
*   **Returns:** `True` if valid, `False` otherwise.

#### `_get_opponent_piece(self, player_piece)`
*   **Purpose:** (Internal helper) Returns the opponent's piece character given a player's piece character.
*   **Returns:** The opponent's piece character.

#### `get_all_possible_moves(self, player_piece)`
*   **Purpose:** Returns a list of all valid moves for the specified `player_piece`.
*   **Parameters:**
    *   `player_piece`: The piece character of the player whose moves are to be found.
*   **Returns:** A list of moves. Each move is a list, e.g., `["move", (from_r, from_c), (to_r, to_c)]` or `["capture", (from_r, from_c), (to_r, to_c), [(captured_r, captured_c)]]`.
*   **Functionality (Schlagzwang - Forced Capture):**
    1.  Determines the active player's pieces and their forward direction.
    2.  First, calls `_get_possible_captures()` to find all available capture moves.
    3.  If any capture moves exist, only those are returned (captures are mandatory).
    4.  If no captures are available, calls `_get_regular_moves()` to find all non-capture moves.

#### `get_possible_moves(self, piece_coord)`
*   **Purpose:** Returns a list of all valid moves for a *specific piece* at `piece_coord`.
*   **Parameters:**
    *   `piece_coord` (tuple): `(row, col)` of the piece.
*   **Returns:** A list of moves for that specific piece, following the same format as `get_all_possible_moves`.
*   **Functionality:**
    1.  Verifies that the `piece_coord` is valid and contains a piece of the current player.
    2.  Checks for captures available to this piece using `_get_possible_captures_for_piece()`. If captures exist, only they are returned.
    3.  Otherwise, checks for regular moves using `_get_regular_moves_for_piece()`.

#### `_get_possible_captures(self, pieces, opponent_piece, direction)`
*   **Purpose:** (Internal helper) Finds all possible capture moves for a given set of `pieces`.
*   **Parameters:**
    *   `pieces` (set): Set of coordinates `(r,c)` of the pieces to check.
    *   `opponent_piece`: Character of the opponent's piece.
    *   `direction`: Integer indicating the forward direction (+1 for human, -1 for AI for standard pieces).
*   **Returns:** A list of all capture moves available to the pieces.

#### `_get_possible_captures_for_piece(self, piece_coord, opponent_piece, direction)`
*   **Purpose:** (Internal helper) Finds all capture moves for a single piece at `piece_coord`.
*   **Parameters:** See `_get_possible_captures`.
*   **Returns:** A list of capture moves for the specified piece.
*   **Functionality:**
    *   Checks diagonally forward squares for an opponent piece that can be jumped over into an empty landing square.
    *   Only considers captures in the piece's `direction` (standard pieces do not capture backward).

#### `_get_regular_moves(self, pieces, direction)`
*   **Purpose:** (Internal helper) Finds all regular (non-capture) moves for a given set of `pieces`.
*   **Returns:** A list of all regular moves available.

#### `_get_regular_moves_for_piece(self, piece_coord, direction)`
*   **Purpose:** (Internal helper) Finds all regular moves for a single piece at `piece_coord`.
*   **Returns:** A list of regular moves for the specified piece.
*   **Functionality:** Checks diagonally forward squares that are empty.

#### `_check_further_captures(self, r_start, c_start, piece_making_move)`
*   **Purpose:** (Internal helper) After a capture, checks if the piece that just captured (now at `r_start, c_start`) can make another *forward* capture immediately.
*   **Parameters:**
    *   `r_start`, `c_start`: Coordinates of the piece that just made a capture.
    *   `piece_making_move`: The character of the piece that just moved.
*   **Returns:** `True` if a further forward capture is possible, `False` otherwise.

#### `make_move(self, move_info, player_piece_making_move)`
*   **Purpose:** Applies a given move to the board and updates the game state.
*   **Parameters:**
    *   `move_info` (list): The move details (type, from, to, captured pieces if any).
    *   `player_piece_making_move`: The character of the piece being moved.
*   **Returns:** A tuple `(bool: move_was_valid, bool: further_capture_possible)`.
*   **Functionality:**
    1.  Validates the move source.
    2.  Updates the `self.board` (moves piece, clears old square).
    3.  **Crucially, updates `self.human_pieces` and `self.ai_pieces` sets:**
        *   Removes the piece from its `from_pos` in the relevant set.
        *   Adds the piece to its `to_pos` in the relevant set.
    4.  If the move is a capture:
        *   Removes captured pieces from the board and from the opponent's piece set.
        *   Calls `_check_further_captures()` to see if a chain capture is possible.
        *   If no further capture, or if it was a simple move, calls `self.switch_player()`.
    5.  Returns `True` and `further_capture_possible` status if valid, `False, False` otherwise.

#### `check_win_condition(self)`
*   **Purpose:** Checks if the current board state results in a win for either player.
*   **Returns:** 'human_wins', 'ai_wins', or `None` if the game is ongoing. Draw is not explicitly handled as a win condition in this basic Dame variant.
*   **Functionality (checks in order):**
    1.  **Human reaches AI's back rank:** Iterates through `self.human_pieces`. If any human piece `(r,c)` has `r == self.board_size - 1`.
    2.  **AI reaches Human's back rank:** Iterates through `self.ai_pieces`. If any AI piece `(r,c)` has `r == 0`.
    3.  **No Human pieces left:** Checks if `self.human_pieces` is empty.
    4.  **No AI pieces left:** Checks if `self.ai_pieces` is empty.
    5.  **Current player has no legal moves:** Calls `get_all_possible_moves()` for the `self.current_player_piece`. If the list is empty, the other player wins.

#### `current_player_piece` (property)
*   **Purpose:** Gets the piece character of the current player.
*   **Returns:** `self.human_player_piece` or `self.ai_player_piece`.

#### `get_ai_move(self)`
*   **Purpose:** Intended to get the AI's next move. In the current setup, `GameController` typically instantiates `Minimax` directly.
*   **Returns:** The best move found by a Minimax search (default depth 3 if not configured by controller).
*   **Note:** This method in its current form in `dame.py` *does not* make the move; it only finds it. The `GameController` is responsible for taking the returned move and calling `Dame.make_move()`.

#### `is_game_over(self)`
*   **Purpose:** Checks if the game has ended.
*   **Returns:** `True` if `check_win_condition()` is not `None`, `False` otherwise.

#### `evaluate_board(self, player_piece_perspective)`
*   **Purpose:** Evaluates the current board state for the Minimax algorithm, from the perspective of `player_piece_perspective`.
*   **Parameters:**
    *   `player_piece_perspective`: The piece character of the player for whom the evaluation is being done (usually the AI).
*   **Returns:** A numerical score. Positive for favorable to `player_piece_perspective`, negative for unfavorable.
*   **Functionality:**
    1.  Calls `check_win_condition()`.
        *   If AI wins (from AI's perspective): returns `float('inf')`.
        *   If Human wins (AI loses, from AI's perspective): returns `float('-inf')`.
    2.  If no win/loss, calculates a heuristic score based on:
        *   **Piece difference:** `(len(human_pieces) - len(ai_pieces))`. Weighted more heavily (e.g., by 10).
        *   **Advancement score:** Sum of row advancements for each piece. Human pieces gain score for increasing row index; AI pieces gain score for decreasing row index (moving towards their respective back ranks).
    3.  The `total_score` is returned (negated if `player_piece_perspective` is not the human player, to align scores).

#### `get_rules(self)`
*   **Purpose:** Returns a list of strings describing the game rules.

#### `__str__(self)`
*   **Purpose:** Returns a simple string representation of the current board state for printing to console.

## Interaction with `BaseGame`

`Dame` inherits abstract methods from `BaseGame` and provides concrete implementations for them, tailored to Dame rules. 