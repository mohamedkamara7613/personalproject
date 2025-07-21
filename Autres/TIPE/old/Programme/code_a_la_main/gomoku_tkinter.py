import tkinter as tk
from tkinter import messagebox


class Gomoku:
    def __init__(self, size=15):
        self.size = size
        self.grid = [[0 for _ in range(self.size)] for _ in range(self.size)]
        self.current_player = 1  # 1 pour X, -1 pour O
        self.window = tk.Tk()
        self.window.title("Gomoku")
        self.buttons = [[None for _ in range(self.size)] for _ in range(self.size)]
        self.create_board()

    def create_board(self):
        """Crée l'interface graphique du plateau de jeu."""
        for row in range(self.size):
            for col in range(self.size):
                button = tk.Button(
                    self.window,
                    text="",
                    width=3,
                    height=1,
                    font=("Helvetica", 16),
                    command=lambda r=row, c=col: self.make_move(r, c)
                )
                button.grid(row=row, column=col)
                self.buttons[row][col] = button

    def make_move(self, row, col):
        """Gère le placement des pions par les joueurs."""
        if self.grid[row][col] == 0:  # Vérifie si la case est vide
            self.grid[row][col] = self.current_player
            self.buttons[row][col]["text"] = "X" if self.current_player == 1 else "O"
            self.buttons[row][col]["fg"] = "red" if self.current_player == 1 else "green"

            # Vérifie si le jeu est terminé
            if self.is_game_over(row, col):
                winner = "Joueur X" if self.current_player == 1 else "Joueur O"
                messagebox.showinfo("Victoire", f"{winner} a gagné !")
                self.window.quit()
            else:
                self.current_player = -self.current_player  # Change de joueur
        else:
            messagebox.showwarning("Case occupée", "Cette case est déjà prise !")

    def is_game_over(self, row, col):
        """Vérifie si un joueur a gagné."""
        player = self.current_player
        align = 5

        # Directions : horizontal, vertical, diagonale (\), diagonale (/)
        directions = [
            [(0, 1), (0, -1)],  # Horizontal
            [(1, 0), (-1, 0)],  # Vertical
            [(1, 1), (-1, -1)],  # Diagonale \
            [(1, -1), (-1, 1)]   # Diagonale /
        ]

        for direction in directions:
            consecutive = 1
            for dx, dy in direction:
                for step in range(1, align):
                    r, c = row + step * dx, col + step * dy
                    if 0 <= r < self.size and 0 <= c < self.size and self.grid[r][c] == player:
                        consecutive += 1
                    else:
                        break
            if consecutive >= align:
                return True

        return False

    def run(self):
        """Démarre le jeu."""
        self.window.mainloop()


if __name__ == "__main__":
    game = Gomoku()
    game.run()
