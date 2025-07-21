class GomokuAI:
    def __init__(self, size=15):
        self.size = size
        self.board = [['.' for _ in range(size)] for _ in range(size)]

    def evaluate(self):
        # Fonction d'évaluation simple : compte le nombre de pierres alignées pour chaque joueur.
        player = 'X'  # L'IA est 'X'.
        opponent = 'O'
        score = 0

        # Parcours horizontal, vertical, et diagonal pour les deux joueurs.
        for r in range(self.size):
            for c in range(self.size):
                if self.board[r][c] == player:
                    # Évaluation pour l'IA (X).
                    score += self.count_stones_in_direction(r, c, player, 1, 0)  # Horizontal.
                    score += self.count_stones_in_direction(r, c, player, 0, 1)  # Vertical.
                    score += self.count_stones_in_direction(r, c, player, 1, 1)  # Diagonale droite.
                    score += self.count_stones_in_direction(r, c, player, -1, 1)  # Diagonale gauche.

                elif self.board[r][c] == opponent:
                    # Évaluation pour l'adversaire (O).
                    score -= self.count_stones_in_direction(r, c, opponent, 1, 0)
                    score -= self.count_stones_in_direction(r, c, opponent, 0, 1)
                    score -= self.count_stones_in_direction(r, c, opponent, 1, 1)
                    score -= self.count_stones_in_direction(r, c, opponent, -1, 1)

        return score

    def count_stones_in_direction(self, row, col, player, dr, dc):
        count = 0
        r, c = row, col
        while 0 <= r < self.size and 0 <= c < self.size and self.board[r][c] == player:
            count += 1
            r += dr
            c += dc
        return count

    def minimax(self, depth, maximizing_player):
        if depth == 0 or self.is_game_over():
            return self.evaluate()

        if maximizing_player:
            max_eval = float('-inf')
            for r in range(self.size):
                for c in range(self.size):
                    if self.board[r][c] == '.':
                        self.board[r][c] = 'X'
                        eval = self.minimax(depth - 1, False)
                        self.board[r][c] = '.'
                        max_eval = max(max_eval, eval)
            return max_eval

        else:
            min_eval = float('inf')
            for r in range(self.size):
                for c in range(self.size):
                    if self.board[r][c] == '.':
                        self.board[r][c] = 'O'
                        eval = self.minimax(depth - 1, True)
                        self.board[r][c] = '.'
                        min_eval = min(min_eval, eval)
            return min_eval

    def make_best_move(self):
        best_move = None
        best_eval = float('-inf')
        for r in range(self.size):
            for c in range(self.size):
                if self.board[r][c] == '.':
                    self.board[r][c] = 'X'
                    eval = self.minimax(3, False)  # Profondeur de recherche de l'IA.
                    self.board[r][c] = '.'
                    if eval > best_eval:
                        best_eval = eval
                        best_move = (r, c)

        if best_move:
            return best_move

    def is_game_over(self):
        # Fonction pour vérifier si le jeu est terminé (par exemple, s'il y a un gagnant ou un match nul).
        # Vous devrez la compléter avec votre propre logique de fin de jeu.

        return False  # Cette version simplifiée ne gère pas la fin du jeu.

# Utilisation de l'IA dans le jeu
ai = GomokuAI()
best_move = ai.make_best_move()
if best_move:
    ai.board[best_move[0]][best_move[1]] = 'X'  # L'IA joue son meilleur coup.