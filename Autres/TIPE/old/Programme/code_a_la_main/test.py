def calculer_threats(self, board):
    threats = []

    # Recherche des menaces potentielles dans les lignes, colonnes et diagonales
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:  # Case vide
                # Vérifier les menaces potentielles pour la case vide
                threat_in_row = self.check_threat_in_row(board, i, j)
                threat_in_column = self.check_threat_in_column(board, i, j)
                threat_in_diagonal = self.check_threat_in_diagonal(board, i, j)

                # Si une menace est trouvée, l'ajouter à la liste des menaces
                if threat_in_row or threat_in_column or threat_in_diagonal:
                    threats.append((i, j, threat_in_row, threat_in_column, threat_in_diagonal))

    return threats

    def TSS_algorithm(self, board):
        score = 0
        
        # Types de menaces
        quatre = [(1, 1, 1, 1, 0), (0, 1, 1, 1, 1)]  # 4 en ligne de 5 carrés
        quatre_droites = [(1, 0, 1, 1, 1, 0), (0, 1, 1, 1, 0, 1)]  # 4 en ligne de 6 carrés avec centre occupé
        trois = [(1, 0, 1, 1, 1, 0, 0), (0, 0, 1, 1, 1, 0, 1)]  # 3 en ligne de 7 carrés avec centre occupé
        trois_alternatif = [(1, 0, 0, 1, 1, 0), (0, 1, 1, 0, 0, 1)]  # 3 alternative en ligne de 6 carrés
        trois_casse = [(1, 0, 1, 0, 1, 0), (0, 1, 0, 1, 0, 1)]  # 3 cassé en ligne de 6 carrés

        # Recherche de menaces potentielles dans la direction horizontale
        for r in range(self.size):
            for c in range(self.size - self.align):
                window = tuple(board[r][c:c+self.align])
                if window in quatre:
                    score += 100  # Un 4 est une menace critique
                elif window in quatre_droites:
                    score += 80  # Un 4 droit est également très menaçant
                elif window in trois:
                    score += 50  # Un 3 est une menace importante
                elif window in trois_alternatif:
                    score += 30  # Un 3 alternatif est moins menaçant
                elif window in trois_casse:
                    score += 20  # Un 3 cassé est moins prioritaire
                
        # Recherche de menaces potentielles dans la direction verticale
        for c in range(self.size):
            for r in range(self.size - self.align):
                window = tuple(board[r:r+self.align, c])
                if window in quatre:
                    score += 100
                elif window in quatre_droites:
                    score += 80
                elif window in trois:
                    score += 50
                elif window in trois_alternatif:
                    score += 30
                elif window in trois_casse:
                    score += 20
        
        # Recherche de menaces potentielles dans la direction diagonale positive
        for r in range(self.size - self.align):
            for c in range(self.size - self.align):
                window = tuple(board[r+i][c+i] for i in range(self.align))
                if window in quatre:
                    score += 100
                elif window in quatre_droites:
                    score += 80
                elif window in trois:
                    score += 50
                elif window in trois_alternatif:
                    score += 30
                elif window in trois_casse:
                    score += 20
        
        # Recherche de menaces potentielles dans la direction diagonale négative
        for r in range(self.size - self.align):
            for c in range(self.align - 1, self.size):
                window = tuple(board[r+i][c-i] for i in range(self.align))
                if window in quatre:
                    score += 100
                elif window in quatre_droites:
                    score += 80
                elif window in trois:
                    score += 50
                elif window in trois_alternatif:
                    score += 30
                elif window in trois_casse:
                    score += 20
        
        return score


    def score_position_TSS_algorithm(self, board):
        score = 0
        
        # Recherche de menaces potentielles dans la direction horizontale
        for r in range(self.size):
            for c in range(self.size - self.align-1):
                threat_count = 0
                own_count = 0
                opponent_count = 0
                for i in range(self.align):
                    if board[r][c + i] == self.playerX:
                        own_count += 1
                        threat_count = 0
                    elif board[r][c + i] == self.playerO:
                        opponent_count += 1
                        threat_count = 0
                    else:
                        threat_count += 1
                        if threat_count == 5:
                            score += 100
                            break
                if own_count == 4:
                    score += 50
                elif own_count == 3 and threat_count == 1:
                    score += 10
                elif own_count == 2 and threat_count == 2:
                    score += 5
                elif opponent_count == 4:
                    score -= 80
                elif opponent_count == 3 and threat_count == 1:
                    score -= 20
                elif opponent_count == 2 and threat_count == 2:
                    score -= 10
        
        # Recherche de menaces potentielles dans la direction verticale
        for c in range(self.size):
            for r in range(self.size - self.align-1):
                threat_count = 0
                own_count = 0
                opponent_count = 0
                for i in range(self.align):
                    if board[r + i][c] == self.playerX:
                        own_count += 1
                        threat_count = 0
                    elif board[r + i][c] == self.playerO:
                        opponent_count += 1
                        threat_count = 0
                    else:
                        threat_count += 1
                        if threat_count == 5:
                            score += 100
                            break
                if own_count == 4:
                    score += 50
                elif own_count == 3 and threat_count == 1:
                    score += 10
                elif own_count == 2 and threat_count == 2:
                    score += 5
                elif opponent_count == 4:
                    score -= 80
                elif opponent_count == 3 and threat_count == 1:
                    score -= 20
                elif opponent_count == 2 and threat_count == 2:
                    score -= 10
        
        # Recherche de menaces potentielles dans la direction diagonale positive
        for r in range(self.size - self.align-1):
            for c in range(self.size - self.align-1):
                threat_count = 0
                own_count = 0
                opponent_count = 0
                for i in range(self.align):
                    if board[r + i][c + i] == self.playerX:
                        own_count += 1
                        threat_count = 0
                    elif board[r + i][c + i] == self.playerO:
                        opponent_count += 1
                        threat_count = 0
                    else:
                        threat_count += 1
                        if threat_count == 5:
                            score += 100
                            break
                if own_count == 4:
                    score += 50
                elif own_count == 3 and threat_count == 1:
                    score += 10
                elif own_count == 2 and threat_count == 2:
                    score += 5
                elif opponent_count == 4:
                    score -= 80
                elif opponent_count == 3 and threat_count == 1:
                    score -= 20
                elif opponent_count == 2 and threat_count == 2:
                    score -= 10
        
        # Recherche de menaces potentielles dans la direction diagonale négative
        for r in range(self.size - self.align-1):
            for c in range(4, self.size):
                threat_count = 0
                own_count = 0
                opponent_count = 0
                for i in range(self.align):
                    if board[r + i][c - i] == self.playerX:
                        own_count += 1
                        threat_count = 0
                    elif board[r + i][c - i] == self.playerO:
                        opponent_count += 1
                        threat_count = 0
                    else:
                        threat_count += 1
                        if threat_count == 5:
                            score += 100
                            break
                if own_count == 4:
                    score += 50
                elif own_count == 3 and threat_count == 1:
                    score += 10
                elif own_count == 2 and threat_count == 2:
                    score += 5
                elif opponent_count == 4:
                    score -= 80
                elif opponent_count == 3 and threat_count == 1:
                    score -= 20
                elif opponent_count == 2 and threat_count == 2:
                    score -= 10
        
        return score
    
        

window = [0 for i in range(5)]

window[0] = 1
window[2] = 1
window[3] = -1

print(window)
print(window.count(1), window.count(-1))
            
class Gomoku_AI():
    def  __init__(self, Gomoku_game_instance):
        self.Gomoku_game_instance = Gomoku_game_instance
        self.board = self.Gomoku_game_instance.board
        self.playerX = 1
        self.playerO = -1
        self.empty = 0
        self.size = self.Gomoku_game_instance.size
        self.align:int = self.Gomoku_game_instance.align
        self.transposition_table = {}  # Table de transposition

    def alphaBeta(self, depth=2, alpha=None, beta=None, maximizing_player=False):
        # ...

        # Clé de hash pour la position actuelle
        hash_key = hash(str(self.board))

        # Vérifier si la position est déjà évaluée dans la table de transposition
        if hash_key in self.transposition_table:
            entry = self.transposition_table[hash_key]
            if entry['depth'] >= depth:
                return entry['value']

        # Évaluation normale de la position
        if maximizing_player:
            # ...
        else:
            # ...

        # Stockage de la position évaluée dans la table de transposition
        self.transposition_table[hash_key] = {'value': eval, 'depth': depth}

        return eval
