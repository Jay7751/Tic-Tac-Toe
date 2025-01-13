def initialize_board():
    return [[" " for _ in range(3)] for _ in range(3)]

def display_board(board):
    print("\n".join(["|".join(row) for row in board]))
    print("-" * 5)

def is_winner(board, player):
    for row in board:
        if all(cell == player for cell in row):
            return True
    for col in range(3):
        if all(row[col] == player for row in board):
            return True
    if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):
        return True
    return False

def is_draw(board):
    return all(cell != " " for row in board for cell in row)

def play_game():
    board = initialize_board()
    current_player = "X"
    while True:
        display_board(board)
        try:
            row, col = map(int, input(f"Player {current_player}, enter row and column (0-2): ").split())
            if board[row][col] != " ":
                print("Cell is occupied! Try again.")
                continue
            board[row][col] = current_player
            if is_winner(board, current_player):
                display_board(board)
                print(f"Player {current_player} wins!")
                break
            if is_draw(board):
                display_board(board)
                print("It's a draw!")
                break
            current_player = "O" if current_player == "X" else "X"
        except (ValueError, IndexError):
            print("Invalid input. Enter row and column between 0-2.")

if __name__ == "__main__":
    play_game()
