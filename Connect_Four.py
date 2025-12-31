import tkinter as tk
import random

class ConnectFour:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Connect Four")
        self.root.geometry("750x820")
        self.root.configure(bg="#1e1b4b")
        self.root.resizable(False, False)

        self.ROWS = 6
        self.COLS = 7

        self.player1 = ""
        self.player2 = ""
        self.score1 = 0
        self.score2 = 0

        self.vs_computer = False
        self.board = [[0]*self.COLS for _ in range(self.ROWS)]
        self.current_player = 1

        self.start_screen()

    # ---------------- START SCREEN ----------------
    def start_screen(self):
        self.clear()

        tk.Label(self.root, text="CONNECT FOUR",
                 font=("Arial", 32, "bold"),
                 bg="#1e1b4b", fg="white").pack(pady=30)

        tk.Button(self.root, text="👥 Player vs Player",
                  font=("Arial", 18, "bold"),
                  bg="#10b981", fg="white",
                  width=25, height=2,
                  command=self.player_vs_player).pack(pady=15)

        tk.Button(self.root, text="🤖 Player vs Computer",
                  font=("Arial", 18, "bold"),
                  bg="#3b82f6", fg="white",
                  width=25, height=2,
                  command=self.player_vs_computer).pack(pady=15)

    # ---------------- MODE SELECT ----------------
    def player_vs_player(self):
        self.vs_computer = False
        self.name_screen(two_players=True)

    def player_vs_computer(self):
        self.vs_computer = True
        self.name_screen(two_players=False)

    # ---------------- NAME INPUT ----------------
    def name_screen(self, two_players):
        self.clear()

        tk.Label(self.root, text="Enter Player Name(s)",
                 font=("Arial", 26, "bold"),
                 bg="#1e1b4b", fg="white").pack(pady=20)

        self.p1_entry = tk.Entry(self.root, font=("Arial", 18))
        self.p1_entry.pack(pady=10)
        self.p1_entry.insert(0, "Player 1")

        if two_players:
            self.p2_entry = tk.Entry(self.root, font=("Arial", 18))
            self.p2_entry.pack(pady=10)
            self.p2_entry.insert(0, "Player 2")

        tk.Button(self.root, text="Start Game",
                  font=("Arial", 16, "bold"),
                  bg="#22c55e", fg="white",
                  command=lambda: self.start_game(two_players)).pack(pady=20)

    def start_game(self, two_players):
        self.player1 = self.p1_entry.get()
        self.player2 = self.p2_entry.get() if two_players else "Computer"
        self.score1 = 0
        self.score2 = 0
        self.new_round()

    # ---------------- GAME UI ----------------
    def new_round(self):
        self.clear()
        self.board = [[0]*self.COLS for _ in range(self.ROWS)]
        self.current_player = 1

        self.score_label = tk.Label(self.root,
            text=f"{self.player1}: {self.score1}   |   {self.player2}: {self.score2}",
            font=("Arial", 18, "bold"),
            bg="#1e1b4b", fg="#facc15")
        self.score_label.pack(pady=10)

        self.turn_label = tk.Label(self.root,
            text=f"{self.player1}'s Turn",
            font=("Arial", 16, "bold"),
            bg="#1e1b4b", fg="#fca5a5")
        self.turn_label.pack()

        self.board_frame = tk.Frame(self.root, bg="#2563eb", padx=15, pady=15)
        self.board_frame.pack()

        self.cells = [[None]*self.COLS for _ in range(self.ROWS)]

        for r in range(self.ROWS):
            for c in range(self.COLS):
                canvas = tk.Canvas(self.board_frame, width=75, height=75,
                                   bg="#1e40af", highlightthickness=2,
                                   highlightbackground="#1e3a8a")
                canvas.grid(row=r, column=c, padx=3, pady=3)
                oval = canvas.create_oval(8, 8, 67, 67, fill="white")
                self.cells[r][c] = (canvas, oval)
                canvas.bind("<Button-1>", lambda e, col=c: self.drop_piece(col))

    # ---------------- GAME LOGIC ----------------
    def drop_piece(self, col):
        for r in range(self.ROWS - 1, -1, -1):
            if self.board[r][col] == 0:
                self.board[r][col] = self.current_player
                self.update_board()

                if self.check_win(r, col):
                    self.handle_win()
                    return

                if self.is_full():
                    self.handle_draw()
                    return

                self.current_player = 2 if self.current_player == 1 else 1
                self.update_turn()

                if self.vs_computer and self.current_player == 2:
                    self.root.after(400, self.computer_move)
                return

    def computer_move(self):
        valid_cols = [c for c in range(self.COLS) if self.board[0][c] == 0]
        self.drop_piece(random.choice(valid_cols))

    def update_board(self):
        for r in range(self.ROWS):
            for c in range(self.COLS):
                canvas, oval = self.cells[r][c]
                color = "white"
                if self.board[r][c] == 1:
                    color = "#ef4444"
                elif self.board[r][c] == 2:
                    color = "#fbbf24"
                canvas.itemconfig(oval, fill=color)

    def update_turn(self):
        name = self.player1 if self.current_player == 1 else self.player2
        self.turn_label.config(text=f"{name}'s Turn")

    def check_win(self, r, c):
        p = self.board[r][c]
        for dr, dc in [(1,0),(0,1),(1,1),(1,-1)]:
            count = 0
            for i in range(-3, 4):
                rr, cc = r + dr*i, c + dc*i
                if 0 <= rr < self.ROWS and 0 <= cc < self.COLS and self.board[rr][cc] == p:
                    count += 1
                    if count == 4:
                        return True
                else:
                    count = 0
        return False

    def is_full(self):
        return all(self.board[0][c] != 0 for c in range(self.COLS))

    # ---------------- END GAME ----------------
    def handle_win(self):
        if self.current_player == 1:
            self.score1 += 1
        else:
            self.score2 += 1
        self.end_popup(f"{self.player1 if self.current_player == 1 else self.player2} Wins!")

    def handle_draw(self):
        self.end_popup("It's a Draw!")

    def end_popup(self, text):
        popup = tk.Toplevel(self.root)
        popup.title("Game Over")
        popup.geometry("420x260")
        popup.configure(bg="#1e293b")
        popup.grab_set()

        tk.Label(popup, text=text,
                 font=("Arial", 20, "bold"),
                 bg="#1e293b", fg="#fde047").pack(pady=20)

        btn_frame = tk.Frame(popup, bg="#1e293b")
        btn_frame.pack(pady=15)

        tk.Button(btn_frame, text="▶ Continue",
                  font=("Arial", 14, "bold"),
                  bg="#10b981", fg="white",
                  width=12,
                  command=lambda: [popup.destroy(), self.new_round()]).grid(row=0, column=0, padx=10)

        tk.Button(btn_frame, text="🔁 Restart",
                  font=("Arial", 14, "bold"),
                  bg="#3b82f6", fg="white",
                  width=12,
                  command=lambda: [popup.destroy(), self.start_screen()]).grid(row=0, column=1, padx=10)

        tk.Button(btn_frame, text="❌ Quit",
                  font=("Arial", 14, "bold"),
                  bg="#ef4444", fg="white",
                  width=12,
                  command=self.root.destroy).grid(row=0, column=2, padx=10)

    def clear(self):
        for w in self.root.winfo_children():
            w.destroy()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    ConnectFour().run()