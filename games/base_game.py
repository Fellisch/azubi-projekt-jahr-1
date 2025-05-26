from abc import ABC, abstractmethod

class BaseGame(ABC):
    def __init__(self, board_size=6):
        self.board_size = board_size
        self.board = self.initialize_board()
        self.current_player = "human" # 'human' or 'ai'

    @abstractmethod
    def initialize_board(self):
        """Initializes the game board."""
        pass

    @abstractmethod
    def make_move(self, piece_coord, target_coord):
        """Applies a move to the board for the given player."""
        pass

    @abstractmethod
    def get_ai_move(self):
        """Returns the AI's move based on the current board state."""
        pass

    @abstractmethod
    def get_possible_moves(self, pieceCoord):
        """Returns a list of all possible moves for the given player."""
        pass

    @abstractmethod
    def check_win_condition(self):
        """Checks if the current board state results in a win for either player or a draw."""
        # Returns 'human_wins', 'ai_wins', 'draw', or None
        pass

    @abstractmethod
    def is_game_over(self):
        """Checks if the game has ended."""
        pass

    @abstractmethod
    def evaluate_board(self, player):
        """Evaluates the board state for the Minimax algorithm from the perspective of the given player."""
        pass

    def switch_player(self):
        if self.current_player == "human":
            self.current_player = "ai"
        else:
            self.current_player = "human" 