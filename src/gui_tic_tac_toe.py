import tkinter as tk
from tkinter import messagebox
import random

class TicTacToeGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Tic Tac Toe")
        self.window.geometry("400x500")
        self.window.configure(bg="#1e1e2f")
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.current_player = "X"
        self.game_mode = "Human vs AI"  # Default mode
        self.difficulty = "Hard"       # Default difficulty
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.status_label = None
        self.create_widgets()
        self.window.mainloop()

    def create_widgets(self):
        # Create a title label with shadow effect
        title = tk.Label(
            self.window,
            text="Tic Tac Toe",
            font=("Helvetica", 24, "bold"),
            bg="#1e1e2f",
            fg="#f1c40f",
            pady=20
        )
        title.pack()

        # Game mode and difficulty selection
        settings_frame = tk.Frame(self.window, bg="#1e1e2f")
        settings_frame.pack(pady=10)

        tk.Label(settings_frame, text="Game Mode:", bg="#1e1e2f", fg="#ffffff", font=("Helvetica", 12)).grid(row=0, column=0, padx=5)
        self.mode_var = tk.StringVar(value=self.game_mode)
        mode_menu = tk.OptionMenu(settings_frame, self.mode_var, "Human vs Human", "Human vs AI")
        mode_menu.config(bg="#34495e", fg="#ffffff", font=("Helvetica", 12), highlightthickness=0)
        mode_menu.grid(row=0, column=1, padx=10)

        tk.Label(settings_frame, text="Difficulty:", bg="#1e1e2f", fg="#ffffff", font=("Helvetica", 12)).grid(row=0, column=2, padx=5)
        self.difficulty_var = tk.StringVar(value=self.difficulty)
        difficulty_menu = tk.OptionMenu(settings_frame, self.difficulty_var, "Easy", "Medium", "Hard")
        difficulty_menu.config(bg="#34495e", fg="#ffffff", font=("Helvetica", 12), highlightthickness=0)
        difficulty_menu.grid(row=0, column=3, padx=10)

        # Create a frame for the game board
        board_frame = tk.Frame(self.window, bg="#1e1e2f")
        board_frame.pack(pady=10)

        # Create buttons for the game grid with rounded corners
        for row in range(3):
            for col in range(3):
                button = tk.Button(
                    board_frame,
                    text=" ",
                    font=("Helvetica", 20, "bold"),
                    width=5,
                    height=2,
                    bg="#2c3e50",
                    fg="#ecf0f1",
                    activebackground="#34495e",
                    activeforeground="#f1c40f",
                    relief="flat",
                    command=lambda r=row, c=col: self.make_move(r, c)
                )
                button.grid(row=row, column=col, padx=10, pady=10)
                self.buttons[row][col] = button

        # Add hover effects for buttons
        for row in range(3):
            for col in range(3):
                button = self.buttons[row][col]
                button.bind("<Enter>", lambda e, b=button: b.config(bg="#34495e"))
                button.bind("<Leave>", lambda e, b=button: b.config(bg="#2c3e50"))

        # Create a status label with a modern font and shadow effect
        self.status_label = tk.Label(
            self.window,
            text="Player X's Turn",
            font=("Helvetica", 16, "bold"),
            bg="#1e1e2f",
            fg="#ffffff",
            pady=10
        )
        self.status_label.pack()

        # Create a reset button with rounded corners
        reset_button = tk.Button(
            self.window,
            text="Reset Game",
            font=("Helvetica", 14),
            bg="#e74c3c",
            fg="#ffffff",
            activebackground="#c0392b",
            activeforeground="#ffffff",
            relief="flat",
            command=self.reset_game
        )
        reset_button.pack(pady=20)

    def make_move(self, row, col):
        if self.board[row][col] == " " and self.status_label["text"] != "Game Over":
            self.board[row][col] = self.current_player
            self.buttons[row][col].config(text=self.current_player, fg="#e74c3c" if self.current_player == "X" else "#3498db")

            if self.check_winner():
                self.status_label.config(
                    text=f"Player {self.current_player} wins!",
                    fg="#f1c40f"
                )
                self.disable_buttons()
            elif self.is_draw():
                self.status_label.config(
                    text="It's a draw!",
                    fg="#f39c12"
                )
                self.disable_buttons()
            else:
                self.current_player = "O" if self.current_player == "X" else "X"
                self.status_label.config(text=f"Player {self.current_player}'s Turn")
                if self.current_player == "O" and self.mode_var.get() == "Human vs AI":
                    self.ai_move()

    def ai_move(self):
        difficulty = self.difficulty_var.get()

        if difficulty == "Easy":
            self.ai_easy()
        elif difficulty == "Medium":
            self.ai_medium()
        else:
            self.ai_hard()

    def ai_easy(self):
        empty_cells = [(r, c) for r in range(3) for c in range(3) if self.board[r][c] == " "]
        if empty_cells:
            move = random.choice(empty_cells)
            self.make_move(move[0], move[1])

    def ai_medium(self):
        if random.random() < 0.5:
            self.ai_easy()
        else:
            self.ai_hard()

    def ai_hard(self):
        best_score = float("-inf")
        best_move = None

        for row in range(3):
            for col in range(3):
                if self.board[row][col] == " ":
                    self.board[row][col] = "O"
                    score = self.minimax(False)
                    self.board[row][col] = " "
                    if score > best_score:
                        best_score = score
                        best_move = (row, col)

        if best_move:
            self.make_move(best_move[0], best_move[1])

    def minimax(self, is_maximizing):
        if self.check_winner():
            return 1 if self.current_player == "O" else -1
        if self.is_draw():
            return 0

        if is_maximizing:
            best_score = float("-inf")
            for row in range(3):
                for col in range(3):
                    if self.board[row][col] == " ":
                        self.board[row][col] = "O"
                        score = self.minimax(False)
                        self.board[row][col] = " "
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = float("inf")
            for row in range(3):
                for col in range(3):
                    if self.board[row][col] == " ":
                        self.board[row][col] = "X"
                        score = self.minimax(True)
                        self.board[row][col] = " "
                        best_score = min(score, best_score)
            return best_score

    def check_winner(self):
        for i in range(3):
            if all(self.board[i][j] == self.current_player for j in range(3)) or \
               all(self.board[j][i] == self.current_player for j in range(3)):
                return True
        if all(self.board[i][i] == self.current_player for i in range(3)) or \
           all(self.board[i][2 - i] == self.current_player for i in range(3)):
            return True
        return False

    def is_draw(self):
        return all(cell != " " for row in self.board for cell in row)

    def disable_buttons(self):
        for row in self.buttons:
            for button in row:
                button.config(state="disabled")

    def reset_game(self):
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.current_player = "X"
        for row in range(3):
            for col in range(3):
                self.buttons[row][col].config(text=" ", state="normal", fg="#ecf0f1")
        self.status_label.config(text="Player X's Turn", fg="#ffffff")


if __name__ == "__main__":
    TicTacToeGUI()
