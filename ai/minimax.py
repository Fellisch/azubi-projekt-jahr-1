import copy

class Minimax:
    WIN_BASE_SCORE = 1000000

    def __init__(self, game_logic_instance, max_depth=3):
        self.game_logic_instance = game_logic_instance
        self.max_depth = int(max_depth) if max_depth is not None else 3
        self.ai_player_piece = None

    def _get_current_turn_piece(self, game_state_instance, is_maximizing_player_turn):
        if is_maximizing_player_turn:
            return self.ai_player_piece
        else:
            if game_state_instance.__class__.__name__ == "TicTacToe":
                return game_state_instance.human_player_mark if self.ai_player_piece == game_state_instance.ai_player_mark else game_state_instance.ai_player_mark
            elif game_state_instance.__class__.__name__ == "Dame":
                return game_state_instance.human_player_piece if self.ai_player_piece == game_state_instance.ai_player_piece else game_state_instance.ai_player_piece
            return None

    def find_best_move(self, ai_player_role_piece):
        self.ai_player_piece = ai_player_role_piece
        best_move_found = None
        best_eval_score = -float('inf')
        alpha = -float('inf')
        beta = float('inf')

        current_live_game = self.game_logic_instance
        possible_first_moves = current_live_game.get_all_possible_moves(self.ai_player_piece) if hasattr(current_live_game, 'get_all_possible_moves') else current_live_game.get_possible_moves(self.ai_player_piece)

        if not possible_first_moves:
            return None

        for move in possible_first_moves:
            simulated_game_after_ai_move = copy.deepcopy(current_live_game)

            if simulated_game_after_ai_move.__class__.__name__ == "TicTacToe":
                simulated_game_after_ai_move.make_move(move, self.ai_player_piece)
            elif simulated_game_after_ai_move.__class__.__name__ == "Dame":
                simulated_game_after_ai_move.make_move(move, self.ai_player_piece)
            
            eval_score = self._minimax_recursive(simulated_game_after_ai_move, self.max_depth - 1, False, alpha, beta)

            if eval_score > best_eval_score:
                best_eval_score = eval_score
                best_move_found = move

            alpha = max(alpha, eval_score)

        return best_move_found

    def _minimax_recursive(self, game_state, depth, is_maximizing_player_turn, alpha, beta):
        if depth == 0 or game_state.is_game_over():
            current_eval = game_state.evaluate_board(self.ai_player_piece)

            if current_eval == float('inf'):
                return self.WIN_BASE_SCORE + depth
            elif current_eval == float('-inf'):
                return -self.WIN_BASE_SCORE - depth
            else:
                return current_eval

        current_recursive_turn_piece = self._get_current_turn_piece(game_state, is_maximizing_player_turn)

        if current_recursive_turn_piece is None:
            return 0

        possible_moves = game_state.get_all_possible_moves(current_recursive_turn_piece) if hasattr(game_state, 'get_all_possible_moves') else game_state.get_possible_moves(current_recursive_turn_piece)

        if not possible_moves:
            if is_maximizing_player_turn: # AI (maximizing) cannot move
                return -self.WIN_BASE_SCORE - depth # Penalize inability to move like a loss
            else: # Opponent (minimizing) cannot move
                return self.WIN_BASE_SCORE + depth # Reward opponent's inability to move like a win

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
                    break
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
                    break
            return min_eval