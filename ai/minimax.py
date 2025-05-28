import copy

class Minimax:
    def __init__(self, game_logic_instance, max_depth=3):
        """ Initializes the Minimax AI.
        Args:
            game_logic_instance: An instance of the game (e.g., TicTacToe, Dame).
            max_depth: The maximum search depth for the Minimax algorithm.
        """
        self.game_logic_instance = game_logic_instance
        self.max_depth = int(max_depth) if max_depth is not None else 3
        self.ai_player_piece = None # This will be set when find_best_move is called

    def _get_current_turn_piece(self, game_state_instance, is_maximizing_player_turn):
        """Determines which player's piece should be used for getting moves.
           Relies on self.ai_player_piece being set.
        """
        if is_maximizing_player_turn:
            return self.ai_player_piece
        else:
            # It's opponent's turn, determine opponent's piece
            if game_state_instance.__class__.__name__ == "TicTacToe":
                return game_state_instance.human_player_mark if self.ai_player_piece == game_state_instance.ai_player_mark else game_state_instance.ai_player_mark
            elif game_state_instance.__class__.__name__ == "Dame":
                return game_state_instance.human_player_piece if self.ai_player_piece == game_state_instance.ai_player_piece else game_state_instance.ai_player_piece
            return None # Should not happen

    def find_best_move(self, ai_player_role_piece):
        """ Finds the best move for the AI player using the Minimax algorithm.
        Args:
            ai_player_role_piece: The piece/mark that the AI is playing as (e.g., 'O' for TTT, 'B' for Dame).
                               This is the piece for whom the score should be maximized.
        Returns:
            The best move found for the AI player, or None if no moves are possible.
        """
        self.ai_player_piece = ai_player_role_piece
        # print(f"[Minimax] AI finding best move as piece: {self.ai_player_piece} with depth: {self.max_depth}")

        best_move_found = None
        best_eval_score = -float('inf')
        alpha = -float('inf')
        beta = float('inf')

        # The initial game state for considering moves is the one held by self.game_logic_instance
        # This game instance is controlled by the App controller and reflects the live game.
        # We must not modify it directly here, only its copies.
        current_live_game = self.game_logic_instance

        # Determine whose turn it is in the live game to get initial moves.
        # This should be the AI's turn if this method is called correctly.
        # The piece (ai_player_role_piece) explicitly tells us who the AI is.
        possible_first_moves = current_live_game.get_all_possible_moves(self.ai_player_piece) if hasattr(current_live_game, 'get_all_possible_moves') else current_live_game.get_possible_moves(self.ai_player_piece)

        if not possible_first_moves:
            # print("[Minimax] No possible initial moves for AI.")
            return None

        # Order moves for potentially better pruning (optional, not implemented here yet)
        # For example, heuristic to try likely good moves first.

        for move in possible_first_moves:
            # Create a deep copy of the current live game state to simulate this move
            simulated_game_after_ai_move = copy.deepcopy(current_live_game)

            # Apply AI's potential move to this copied game state
            # The make_move method in game classes should handle piece placement and current_player switching.
            if simulated_game_after_ai_move.__class__.__name__ == "TicTacToe":
                simulated_game_after_ai_move.make_move(move, self.ai_player_piece)
            elif simulated_game_after_ai_move.__class__.__name__ == "Dame":
                # Dame's moves are lists like [type, from, to, [captures]]
                simulated_game_after_ai_move.make_move(move, self.ai_player_piece)

            # After AI's move, it's opponent's turn (minimizing player).
            # Depth for recursive call is self.max_depth - 1 because one ply (AI's move) has been made.
            eval_score = self._minimax_recursive(simulated_game_after_ai_move, self.max_depth - 1, False, alpha, beta)

            # print(f"[Minimax] Move: {move}, Eval Score: {eval_score}")
            if eval_score > best_eval_score:
                best_eval_score = eval_score
                best_move_found = move

            # Update alpha for the root node (AI's main maximizing turn)
            alpha = max(alpha, eval_score)
            # No beta check here at the root for pruning among the AI's first moves directly,
            # because we want to find the absolute best score for the AI from all its options.
            # Pruning happens *within* the recursive calls.

        # print(f"[Minimax] Chosen best move: {best_move_found} with score: {best_eval_score}")
        return best_move_found

    def _minimax_recursive(self, game_state, depth, is_maximizing_player_turn, alpha, beta):
        """ Recursive helper for the Minimax algorithm.
        Args:
            game_state: The current game state (an instance of a game class, e.g., TicTacToe or Dame) to evaluate.
            depth: The remaining search depth.
            is_maximizing_player_turn: True if the current turn is for the maximizing player (our AI),
                                       False if for the minimizing player (opponent).
            alpha: The alpha value for alpha-beta pruning.
            beta: The beta value for alpha-beta pruning.
        Returns:
            The evaluation score for the given game_state from the perspective of self.ai_player_piece.
        """

        # Base case: depth limit reached or game is over
        if depth == 0 or game_state.is_game_over():
            # Evaluation is always from the perspective of the original AI player (self.ai_player_piece)
            return game_state.evaluate_board(self.ai_player_piece)

        # Determine whose piece to use for getting moves for the current turn in the recursion
        current_recursive_turn_piece = self._get_current_turn_piece(game_state, is_maximizing_player_turn)

        if current_recursive_turn_piece is None:
            # This should not happen if _get_current_turn_piece is correct
            # print("[Minimax Error] Could not determine piece for recursive turn.")
            return 0 # Or some neutral/error value

        possible_moves = game_state.get_all_possible_moves(current_recursive_turn_piece) if hasattr(game_state, 'get_all_possible_moves') else game_state.get_possible_moves(current_recursive_turn_piece)

        if not possible_moves:
            # No moves possible for the current player at this state, but game not over by depth/win condition.
            # This typically means a loss for the player who cannot move.
            # The game's is_game_over() should ideally catch this via check_win_condition() (e.g. no moves = loss)
            # If is_game_over() was false, but no moves, evaluate current board. evaluate_board() should handle it.
            # Or, if it represents a specific loss not caught by evaluate_board based on win_status:
            if is_maximizing_player_turn: # AI (maximizing) cannot move
                return -float('inf') 
            else: # Opponent (minimizing) cannot move
                return float('inf')

        if is_maximizing_player_turn:
            max_eval = -float('inf')
            for move in possible_moves:
                next_game_state = copy.deepcopy(game_state)
                if next_game_state.__class__.__name__ == "TicTacToe":
                    next_game_state.make_move(move, current_recursive_turn_piece)
                elif next_game_state.__class__.__name__ == "Dame":
                    next_game_state.make_move(move, current_recursive_turn_piece)

                evaluation = self._minimax_recursive(next_game_state, depth - 1, False, alpha, beta)
                max_eval = max(max_eval, evaluation)
                alpha = max(alpha, evaluation)
                if beta <= alpha:
                    break # Beta cut-off
            return max_eval
        else: # Minimizing player's turn
            min_eval = float('inf')
            for move in possible_moves:
                next_game_state = copy.deepcopy(game_state)
                if next_game_state.__class__.__name__ == "TicTacToe":
                    next_game_state.make_move(move, current_recursive_turn_piece)
                elif next_game_state.__class__.__name__ == "Dame":
                    next_game_state.make_move(move, current_recursive_turn_piece)

                evaluation = self._minimax_recursive(next_game_state, depth - 1, True, alpha, beta)
                min_eval = min(min_eval, evaluation)
                beta = min(beta, evaluation)
                if beta <= alpha:
                    break # Alpha cut-off
            return min_eval 
