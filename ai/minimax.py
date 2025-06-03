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

        if current_live_game.__class__.__name__ == "TicTacToe":
            possible_first_moves = current_live_game.get_possible_moves(self.ai_player_piece)
            possible_first_moves = self._sort_moves(possible_first_moves, current_live_game, self.ai_player_piece)
            clone_func = lambda g: g.clone()
        else:
            possible_first_moves = current_live_game.get_all_possible_moves(self.ai_player_piece) if hasattr(
                current_live_game, 'get_all_possible_moves') else current_live_game.get_possible_moves(
                self.ai_player_piece)
            clone_func = lambda g: copy.deepcopy(g)

        if not possible_first_moves:
            return None

        # Prüfe auf sofortigen Gewinnzug
        for move in possible_first_moves:
            simulated_game = clone_func(current_live_game)
            simulated_game.make_move(move, self.ai_player_piece)
            if simulated_game.check_win_condition() == "ai_wins":
                return move  # Sofortiger Gewinnzug

        for move in possible_first_moves:
            simulated_game_after_ai_move = clone_func(current_live_game)
            simulated_game_after_ai_move.make_move(move, self.ai_player_piece)
            eval_score = self._minimax_recursive(simulated_game_after_ai_move, self.max_depth - 1, False, alpha, beta)
            if eval_score > best_eval_score:
                best_eval_score = eval_score
                best_move_found = move
            alpha = max(alpha, eval_score)

        return best_move_found

    def _minimax_recursive(self, game_state, depth, is_maximizing_player_turn, alpha, beta):
        if depth == 0 or game_state.is_game_over():
            return game_state.evaluate_board(self.ai_player_piece)

        current_recursive_turn_piece = self._get_current_turn_piece(game_state, is_maximizing_player_turn)
        if current_recursive_turn_piece is None:
            return 0

        if game_state.__class__.__name__ == "TicTacToe":
            possible_moves = game_state.get_possible_moves(current_recursive_turn_piece)
            possible_moves = self._sort_moves(possible_moves, game_state, current_recursive_turn_piece)
            clone_func = lambda g: g.clone()
        else:
            possible_moves = game_state.get_all_possible_moves(current_recursive_turn_piece) if hasattr(game_state, 'get_all_possible_moves') else game_state.get_possible_moves(current_recursive_turn_piece)
            clone_func = lambda g: copy.deepcopy(g)

        if not possible_moves:
            if is_maximizing_player_turn:
                return -self.WIN_BASE_SCORE - depth
            else:
                return self.WIN_BASE_SCORE + depth

        if is_maximizing_player_turn:
            max_eval = -float('inf')
            for move in possible_moves:
                next_game_state = clone_func(game_state)
                next_game_state.make_move(move, current_recursive_turn_piece)
                evaluation = self._minimax_recursive(next_game_state, depth - 1, False, alpha, beta)
                max_eval = max(max_eval, evaluation)
                alpha = max(alpha, evaluation)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in possible_moves:
                next_game_state = clone_func(game_state)
                next_game_state.make_move(move, current_recursive_turn_piece)
                evaluation = self._minimax_recursive(next_game_state, depth - 1, True, alpha, beta)
                min_eval = min(min_eval, evaluation)
                beta = min(beta, evaluation)
                if beta <= alpha:
                    break
            return min_eval

    def _sort_moves(self, moves, game_state, player_mark):
        # Nur für TicTacToe sinnvoll
        def move_score(move):
            r, c = move
            neighbors = 0
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0:
                        continue
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < game_state.board_size and 0 <= nc < game_state.board_size:
                        if game_state.board[nr][nc] != '':
                            neighbors += 1
            return -neighbors
        return sorted(moves, key=move_score)