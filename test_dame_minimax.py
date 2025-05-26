import sys
from games.dame import Dame
from ai.minimax import Minimax

def test_dame_minimax():
    print("Testing Dame with Minimax AI...")

    # Create a new Dame game
    game = Dame()
    print("Initial board:")
    print(game)

    # Create a Minimax AI with depth 3
    ai = Minimax(game, max_depth=3)

    # Make a few moves to test the AI
    for i in range(3):
        print(f"\nTurn {i+1}:")

        if game.current_player == "human":
            print("Human's turn")
            # Get all possible moves for human
            human_moves = game.get_all_possible_moves(game.human_player_piece)
            if not human_moves:
                print("No moves available for human")
                break

            # Just pick the first move for testing
            move = human_moves[0]
            print(f"Human makes move: {move}")
            game.make_move(move, game.human_player_piece)
        else:
            print("AI's turn")
            # Use minimax to find the best move
            ai_move = ai.find_best_move(game.ai_player_piece)
            if not ai_move:
                print("No moves available for AI")
                break

            print(f"AI makes move: {ai_move}")
            game.make_move(ai_move, game.ai_player_piece)

        print("Board after move:")
        print(game)

        # Check if game is over
        if game.is_game_over():
            win_status = game.check_win_condition()
            print(f"Game over! Result: {win_status}")
            break

    print("Test completed successfully!")

if __name__ == "__main__":
    test_dame_minimax()
