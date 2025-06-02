# Minimax Algorithm Documentation (`ai/minimax.py`)

This document describes the Minimax algorithm implemented in `ai/minimax.py`, which is used to determine the AI's optimal move in the games.

## Class: `Minimax`

The core of the AI logic resides in the `Minimax` class.

### Attributes:

*   `WIN_BASE_SCORE` (int):
    *   A large constant (e.g., 1,000,000) used as a base for evaluating winning or losing game states.
    *   This score is adjusted by the remaining search depth to prioritize faster wins and slower losses.

*   `game_logic_instance` (object):
    *   An instance of the current game being played (e.g., `Dame` or `TicTacToe`).
    *   The Minimax algorithm interacts with this instance to get possible moves, make simulated moves, and evaluate board states.

*   `max_depth` (int):
    *   The maximum depth (number of plies or half-moves) the algorithm will search.
    *   This value is typically derived from the game's difficulty setting (e.g., Easy, Medium, Hard).

*   `ai_player_piece` (any):
    *   Stores the piece or mark that the AI is currently playing as (e.g., 'B' for Black in Dame, 'O' in TicTacToe).
    *   This is set when `find_best_move` is called and is used to evaluate board states from the AI's perspective.

### Methods:

#### `__init__(self, game_logic_instance, max_depth=3)`
*   **Purpose:** Initializes the Minimax AI.
*   **Parameters:**
    *   `game_logic_instance`: An instance of the current game.
    *   `max_depth` (optional, default: 3): The maximum search depth.
*   **Functionality:** Stores the game instance and max depth. Initializes `ai_player_piece` to `None`.

#### `_get_current_turn_piece(self, game_state_instance, is_maximizing_player_turn)`
*   **Purpose:** (Internal helper) Determines which player's piece/mark should be used for getting moves during the recursive search.
*   **Parameters:**
    *   `game_state_instance`: The current (possibly simulated) game state.
    *   `is_maximizing_player_turn` (bool): `True` if it's the AI's (maximizing) turn, `False` otherwise.
*   **Returns:** The piece/mark of the player whose turn it is in the simulation.

#### `find_best_move(self, ai_player_role_piece)`
*   **Purpose:** Finds the best move for the AI player using the Minimax algorithm with alpha-beta pruning.
*   **Parameters:**
    *   `ai_player_role_piece`: The piece/mark that the AI is playing as. This is crucial for ensuring evaluations are from the AI's perspective.
*   **Returns:** The best move found for the AI, or `None` if no moves are possible.
*   **Functionality:**
    1.  Sets `self.ai_player_piece`.
    2.  Initializes `alpha` (best score for maximizer) to negative infinity and `beta` (best score for minimizer) to positive infinity.
    3.  Gets all possible first moves for the AI from the current live game state.
    4.  For each possible first move:
        a.  Creates a deep copy of the live game state.
        b.  Applies the move to this copied game state.
        c.  Calls `_minimax_recursive` on the copied state to get its evaluation score. The initial call to `_minimax_recursive` is for the opponent's turn (minimizing player), so `is_maximizing_player_turn` is `False`, and depth is `self.max_depth - 1`.
        d.  If the returned score is better than the current `best_eval_score`, updates `best_eval_score` and `best_move_found`.
        e.  Updates `alpha`.
    5.  Returns `best_move_found`.

#### `_minimax_recursive(self, game_state, depth, is_maximizing_player_turn, alpha, beta)`
*   **Purpose:** (Internal helper) The recursive core of the Minimax algorithm with alpha-beta pruning.
*   **Parameters:**
    *   `game_state`: The current game state (a copy) to evaluate.
    *   `depth`: The remaining search depth.
    *   `is_maximizing_player_turn` (bool): `True` if it's the AI's (maximizing) turn, `False` if it's the opponent's (minimizing) turn.
    *   `alpha`: The current best score found so far for the maximizing player on this path.
    *   `beta`: The current best score found so far for the minimizing player on this path.
*   **Returns:** The evaluation score for the given `game_state`.
*   **Functionality (Base Cases):**
    1.  If `depth == 0` (maximum depth reached) or `game_state.is_game_over()` is true:
        a.  The game is at a terminal node for this search path.
        b.  Call `game_state.evaluate_board(self.ai_player_piece)` to get the raw score of the board from the AI's perspective.
        c.  **Depth-Adjusted Scoring:**
            *   If AI wins (`current_eval == float('inf')`): Return `self.WIN_BASE_SCORE + depth`. (Higher `depth` means win was found sooner).
            *   If AI loses (`current_eval == float('-inf')`): Return `-self.WIN_BASE_SCORE - depth`. (Higher `depth` means loss occurs sooner).
            *   Otherwise (draw or heuristic score): Return `current_eval`.
*   **Functionality (Recursive Step):**
    1.  Determine the `current_recursive_turn_piece` using `_get_current_turn_piece`.
    2.  Get all `possible_moves` for `current_recursive_turn_piece` from the `game_state`.
    3.  If no `possible_moves`:
        *   If it was the AI's (maximizing) turn to move but couldn't: Return a highly negative score (`-self.WIN_BASE_SCORE - depth`), indicating a loss.
        *   If it was the opponent's (minimizing) turn but couldn't: Return a highly positive score (`self.WIN_BASE_SCORE + depth`), indicating a win for the AI.
    4.  **If `is_maximizing_player_turn` (AI's turn):**
        a.  Initialize `max_eval` to negative infinity.
        b.  For each `move` in `possible_moves`:
            i.  Create a deep copy (`next_game_state`) of the current `game_state`.
            ii. Apply the `move` to `next_game_state`.
            iii. Recursively call `_minimax_recursive` for `next_game_state`, with `depth - 1`, `is_maximizing_player_turn = False` (now opponent's turn).
            iv. Update `max_eval = max(max_eval, evaluation)`.
            v.  Update `alpha = max(alpha, evaluation)`.
            vi. **Alpha-Beta Pruning:** If `beta <= alpha`, break the loop (no need to explore further down this path for the maximizer).
        c.  Return `max_eval`.
    5.  **Else (Minimizing player's turn - Opponent):**
        a.  Initialize `min_eval` to positive infinity.
        b.  For each `move` in `possible_moves`:
            i.  Create a deep copy (`next_game_state`) of the current `game_state`.
            ii. Apply the `move` to `next_game_state`.
            iii. Recursively call `_minimax_recursive` for `next_game_state`, with `depth - 1`, `is_maximizing_player_turn = True` (now AI's turn).
            iv. Update `min_eval = min(min_eval, evaluation)`.
            v.  Update `beta = min(beta, evaluation)`.
            vi. **Alpha-Beta Pruning:** If `beta <= alpha`, break the loop (no need to explore further down this path for the minimizer).
        c.  Return `min_eval`.

## Key Concepts Implemented:

*   **Minimax:** A decision-making algorithm used to find the optimal move by recursively exploring game states, assuming the opponent also plays optimally.
*   **Alpha-Beta Pruning:** An optimization technique for Minimax that reduces the number of nodes evaluated in the search tree by eliminating branches that cannot influence the final decision.
*   **Depth-Limited Search:** The search is limited by `max_depth` to keep computation manageable.
*   **Heuristic Evaluation Function:** Relies on the `evaluate_board` method of the game logic instance (`Dame` or `TicTacToe`) to score non-terminal board states when the depth limit is reached.
*   **Depth-Adjusted Terminal Scores:** Winning or losing states are scored such that quicker wins (and slower losses) are preferred. This is achieved by adding the remaining `depth` to a `WIN_BASE_SCORE`.

## How it Interacts with Game Logic:

The `Minimax` class is designed to be generic enough to work with different game logics, provided they implement the following methods that `Minimax` relies on:

*   `game_logic_instance.get_all_possible_moves(player_piece)` or `game_logic_instance.get_possible_moves(player_piece)`: Returns a list of valid moves for the given player.
*   `game_logic_instance.make_move(move, player_piece)`: Applies a move to the game state and updates the current player.
*   `game_logic_instance.is_game_over()`: Returns `True` if the game has ended, `False` otherwise.
*   `game_logic_instance.check_win_condition()`: Returns a status indicating if a player has won, lost, or if it's a draw (e.g., 'ai_wins', 'human_wins', 'draw', or `None`).
*   `game_logic_instance.evaluate_board(ai_player_piece)`: Returns a numerical score for the current board state from the perspective of the `ai_player_piece`. Should return `float('inf')` if AI wins, `float('-inf')` if AI loses, and a heuristic score otherwise.
*   Attributes like `game_logic_instance.human_player_mark`, `game_logic_instance.ai_player_mark` (for TicTacToe) or `game_logic_instance.human_player_piece`, `game_logic_instance.ai_player_piece` (for Dame) are used to identify players. 