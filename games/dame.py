from .base_game import BaseGame

EMPTY = '_'
HUMAN_PIECE = 'W'
AI_PIECE = 'B'

class Dame(BaseGame):
    def __init__(self, board_size=6):
        self.human_player_piece = HUMAN_PIECE
        self.ai_player_piece = AI_PIECE
        self.human_pieces = set()
        self.ai_pieces = set()
        super().__init__(board_size)

    def initialize_board(self):
        board = [[EMPTY for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.human_pieces.clear()
        self.ai_pieces.clear()
        for row in range(self.board_size - 2, self.board_size):
            for col in range(self.board_size):
                if (row + col) % 2 == 0:
                    board[row][col] = self.ai_player_piece
                    self.ai_pieces.add((row, col))
        for row in range(2):
            for col in range(self.board_size):
                if (row + col) % 2 == 0:
                    board[row][col] = self.human_player_piece
                    self.human_pieces.add((row, col))
        return board

    def _is_valid_coord(self, r, c):
        return 0 <= r < self.board_size and 0 <= c < self.board_size

    def _get_opponent_piece(self, player_piece):
        return self.ai_player_piece if player_piece == self.human_player_piece else self.human_player_piece

    def get_all_possible_moves(self, player_piece):
        pieces = self.human_pieces if player_piece == self.human_player_piece else self.ai_pieces
        direction = 1 if player_piece == self.human_player_piece else -1
        opponent_piece = self._get_opponent_piece(player_piece)
        captures = self._get_possible_captures(pieces, opponent_piece, direction)
        if captures:
            return captures
        return self._get_regular_moves(pieces, direction)

    def get_possible_moves(self, piece_coord):
        row, col = piece_coord
        if not self._is_valid_coord(row, col) or self.board[row][col] == EMPTY:
            return []
        player_piece = self.board[row][col]
        direction = 1 if player_piece == self.human_player_piece else -1
        opponent_piece = self._get_opponent_piece(player_piece)
        captures = self._get_possible_captures_for_piece((row, col), opponent_piece, direction)
        if captures:
            return captures
        return self._get_regular_moves_for_piece((row, col), direction)

    def _get_possible_captures(self, pieces, opponent_piece, direction):
        possible_captures = []
        for row, col in pieces:
            piece_captures = self._get_possible_captures_for_piece((row, col), opponent_piece, direction)
            possible_captures.extend(piece_captures)
        return possible_captures

    def _get_possible_captures_for_piece(self, piece_coord, opponent_piece, direction):
        possible_captures = []
        row, col = piece_coord
        for drow in [-1, 1]:
            for dcol in [-1, 1]:
                jump_row, jump_col = row + drow, col + dcol
                land_row, land_col = row + 2 * drow, col + 2 * dcol
                if self._is_valid_coord(land_row, land_col) and \
                        self.board[land_row][land_col] == EMPTY and \
                        self._is_valid_coord(jump_row, jump_col) and \
                        self.board[jump_row][jump_col] == opponent_piece:
                    if drow == direction:
                        possible_captures.append([
                                "capture",
                                (row, col),
                                (land_row, land_col),
                                [(jump_row, jump_col)]
                            ])
        return possible_captures

    def _get_regular_moves(self, pieces, direction):
        moves = []
        for row, col in pieces:
            piece_moves = self._get_regular_moves_for_piece((row, col), direction)
            moves.extend(piece_moves)
        return moves

    def _get_regular_moves_for_piece(self, piece_coord, direction):
        moves = []
        row, col = piece_coord
        for dcol in [-1, 1]:
            to_row, to_col = row + direction, col + dcol
            if self._is_valid_coord(to_row, to_col) and self.board[to_row][to_col] == EMPTY:
                moves.append(["move", (row, col), (to_row, to_col)])
        return moves

    def _check_further_captures(self, r_start, c_start, piece_making_move):
        opponent_piece = self._get_opponent_piece(piece_making_move)
        piece_forward_direction = 1 if piece_making_move == self.human_player_piece else -1
        for dr_one_step in [-1, 1]: 
            for dc_one_step in [-1, 1]: 
                if dr_one_step != piece_forward_direction:
                    continue
                opponent_r, opponent_c = r_start + dr_one_step, c_start + dc_one_step
                land_r, land_c = r_start + 2*dr_one_step, c_start + 2*dc_one_step
                if self._is_valid_coord(land_r, land_c) and \
                   self.board[land_r][land_c] == EMPTY and \
                   self._is_valid_coord(opponent_r, opponent_c) and \
                   self.board[opponent_r][opponent_c] == opponent_piece:
                    return True
        return False

    def make_move(self, move_info, player_piece_making_move):
        move_type, from_pos, to_pos = move_info[0], move_info[1], move_info[2]
        from_r, from_c = from_pos
        to_r, to_c = to_pos

        if not self._is_valid_coord(from_r, from_c) or \
           self.board[from_r][from_c] != player_piece_making_move:
            return False, False

        self.board[to_r][to_c] = player_piece_making_move
        self.board[from_r][from_c] = EMPTY
        
        moving_player_pieces = self.human_pieces if player_piece_making_move == self.human_player_piece else self.ai_pieces
        opponent_player_pieces = self.ai_pieces if player_piece_making_move == self.human_player_piece else self.human_pieces

        if from_pos in moving_player_pieces:
            moving_player_pieces.remove(from_pos)
        moving_player_pieces.add(to_pos)
        
        further_capture_possible = False

        if move_type == "capture":
            if len(move_info) < 4 or not isinstance(move_info[3], list):
                self.board[from_r][from_c] = player_piece_making_move
                self.board[to_r][to_c] = EMPTY
                if to_pos in moving_player_pieces:
                    moving_player_pieces.remove(to_pos)
                moving_player_pieces.add(from_pos)
                return False, False

            captured_coords_list = move_info[3]
            for cap_r, cap_c in captured_coords_list:
                self.board[cap_r][cap_c] = EMPTY 
                if (cap_r, cap_c) in opponent_player_pieces:
                    opponent_player_pieces.remove((cap_r, cap_c))
            
            if self._check_further_captures(to_r, to_c, player_piece_making_move):
                further_capture_possible = True
            else:
                self.switch_player()
        
        elif move_type == "move":
            self.switch_player()
        
        else: 
            self.board[from_r][from_c] = player_piece_making_move
            self.board[to_r][to_c] = EMPTY
            if to_pos in moving_player_pieces:
                moving_player_pieces.remove(to_pos)
            moving_player_pieces.add(from_pos)
            return False, False
        return True, further_capture_possible

    def check_win_condition(self):
        for r, c in self.human_pieces:
            if r == self.board_size - 1:
                return "human_wins"
        for r, c in self.ai_pieces:
            if r == 0:
                return "ai_wins"
        if not self.human_pieces:
            return "ai_wins"
        if not self.ai_pieces:
            return "human_wins"
        
        possible_moves_for_current_player = self.get_all_possible_moves(self.current_player_piece)
        if not possible_moves_for_current_player:
            if self.current_player == "human":
                return "ai_wins"
            else:
                return "human_wins"
        return None

    @property
    def current_player_piece(self):
        return self.human_player_piece if self.current_player == "human" else self.ai_player_piece

    def get_ai_move(self):
        from ai.minimax import Minimax
        ai = Minimax(self, max_depth=3) 
        best_move = ai.find_best_move(self.ai_player_piece)
        return best_move 

    def is_game_over(self):
        return self.check_win_condition() is not None

    def evaluate_board(self, player_piece_perspective):
        win_status = self.check_win_condition()
        if win_status == "human_wins":
            return -float('inf') if player_piece_perspective == self.ai_player_piece else float('inf')
        if win_status == "ai_wins":
            return float('inf') if player_piece_perspective == self.ai_player_piece else float('-inf')

        human_pieces_count = len(self.human_pieces)
        ai_pieces_count = len(self.ai_pieces)
        piece_diff_score = human_pieces_count - ai_pieces_count

        human_score = sum(r + 1 for r, c in self.human_pieces)
        ai_score = sum(self.board_size - r for r, c in self.ai_pieces)
        advancement_score = human_score - ai_score 

        total_score = piece_diff_score * 10 + advancement_score

        if player_piece_perspective == self.human_player_piece:
            return total_score
        else:
            return -total_score

    def get_rules(self):
        return [
            "Move: 1 square diagonally forward",
            "Capture (mandatory): Diagonally over an opponent to a free square",
            "Multiple captures are allowed & mandatory",
            "No jumping over own pieces",
            "Win: Opponent cannot move or own piece reaches opponent's baseline",
        ]

    def __str__(self):
        s = "  " + " ".join(map(str, range(self.board_size))) + "\n"
        for r in range(self.board_size):
            s += str(r) + " " + "|".join(self.board[r]) + "\n"
        return s