# Diese Datei ist ein einfaches Beispiel für den Minimax in TicTacToe.
# Dies ist NICHT final und wird noch stark abgeändert


import math

WINNING_COMBINATIONS = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Reihen
    (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Spalten
    (0, 4, 8), (2, 4, 6)              # Diagonalen
]


def check_winner(board):
    """Gibt 'X' oder 'O' zurück, wenn einer gewonnen hat; sonst None."""
    for (i, j, k) in WINNING_COMBINATIONS:
        if board[i] == board[j] == board[k] and board[i] != " ":
            return board[i]
    return None


def is_draw(board):
    """True, wenn keine leeren Felder mehr übrig sind und niemand gewonnen hat."""
    return all(cell != " " for cell in board) and check_winner(board) is None


def minimax(board, player):
    """
    Minimax-Algorithmus:
    - player ist 'X' oder 'O', der gerade zieht.
    - Rückgabe: (best_score, best_move_index)
    """
    winner = check_winner(board)
    if winner == 'X':
        return (1, None)
    if winner == 'O':
        return (-1, None)
    if is_draw(board):
        return (0, None)

    if player == 'X':  # Maximierer
        best_score = -math.inf
    else:  # Minimierer
        best_score = math.inf
    best_move = None

    for i, cell in enumerate(board):
        if cell == " ":
            board[i] = player  # Zug simulieren
            score, _ = minimax(board, 'O' if player == 'X' else 'X')
            board[i] = " "  # Zug rückgängig machen

            if player == 'X':
                if score > best_score:
                    best_score = score
                    best_move = i
            else:
                if score < best_score:
                    best_score = score
                    best_move = i

    return (best_score, best_move)


def print_board(board):
    """Gibt das Tic-Tac-Toe-Brett aus."""
    for row in range(3):
        print(" | ".join(board[row*3:(row+1)*3]))
        if row < 2:
            print("---------")
    print()


def play_game():
    """Spielschleife: Mensch (O) gegen Computer (X)."""
    board = [" "] * 9
    current_player = 'X'

    while True:
        print_board(board)
        if current_player == 'X':
            _, move = minimax(board, 'X')
            print(f"Computer (X) zieht auf Feld {move}.")
        else:
            move = int(input("Dein Zug (0-8)? "))
            if board[move] != " ":
                print("Feld bereits belegt, versuche es erneut.")
                continue

        board[move] = current_player
        if check_winner(board) or is_draw(board):
            print_board(board)
            winner = check_winner(board)
            if winner:
                print(f"Spiel vorbei! Gewinner: {winner}")
            else:
                print("Unentschieden!")
            break

        current_player = 'O' if current_player == 'X' else 'X'


if __name__ == "__main__":
    play_game()
