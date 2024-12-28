import pygame
import sys

# --- Constantes --- 
# Ces valeurs définissent les différents états possibles pour chaque case de la grille
VIDE = 0  # Case vide
JOUEUR_1 = 1  # Case occupée par le joueur 1
JOUEUR_2 = 2  # Case occupée par le joueur 2

# Couleurs pour l'affichage graphique
COULEUR_VIDE = (200, 200, 200)  # Gris clair pour les cases vides
COULEUR_JOUEUR_1 = (255, 0, 0)  # Rouge pour le joueur 1
COULEUR_JOUEUR_2 = (255, 255, 0)  # Jaune pour le joueur 2
COULEUR_GRILLE = (0, 0, 255)  # Bleu pour la grille

# Dimensions des cases et marges
LARGEUR_COLONNE = 130  # Largeur d'une colonne
HAUTEUR_LIGNE = 130  # Hauteur d'une ligne
MARGE = 5  # Espace entre les cercles et les bords de la grille

# Taille de la grille
COLONNES = 7  # Nombre de colonnes
LIGNES = 6  # Nombre de lignes
LARGEUR = COLONNES * LARGEUR_COLONNE  # Largeur totale de la fenêtre
HAUTEUR = (LIGNES + 1) * HAUTEUR_LIGNE  # Hauteur totale de la fenêtre (+1 pour la zone d'entrée)
DIMENSIONS = (LARGEUR, HAUTEUR)  # Dimensions de la fenêtre

class ConnectFour:
    """
    Classe principale pour gérer le jeu de Puissance 4.
    Elle contient la grille, les méthodes pour ajouter des jetons, 
    changer de joueur, vérifier les conditions de victoire ou de match nul.
    """
    def __init__(self):
        # Initialise le plateau (une grille vide) et le joueur actuel
        self.rows = LIGNES
        self.columns = COLONNES
        self.board = [[VIDE for _ in range(self.columns)] for _ in range(self.rows)]
        self.current_player = JOUEUR_1

    def drop_piece(self, column):
        """
        Permet de déposer un jeton dans une colonne spécifique.
        Retourne True si le jeton est placé avec succès, sinon False (colonne pleine).
        """
        if self.board[0][column] != VIDE:
            return False  # Si la première case de la colonne est occupée, la colonne est pleine

        # Parcourir les cases de la colonne de bas en haut pour trouver une case vide
        for row in reversed(range(self.rows)):
            if self.board[row][column] == VIDE:
                self.board[row][column] = self.current_player
                return True  # Jeton placé avec succès
        return False

    def switch_player(self):
        """
        Change le joueur actuel : passe de JOUEUR_1 à JOUEUR_2 ou inversement.
        """
        self.current_player = JOUEUR_2 if self.current_player == JOUEUR_1 else JOUEUR_1

    def check_victory(self):
        """
        Vérifie si le joueur actuel a une ligne de 4 jetons (horizontale, verticale ou diagonale).
        Retourne True si une victoire est détectée, sinon False.
        """
        player = self.current_player

        # Vérification horizontale
        for row in range(self.rows):
            for col in range(self.columns - 3):  # -3 pour éviter de dépasser les limites
                if all(self.board[row][col + i] == player for i in range(4)):
                    return True

        # Vérification verticale
        for col in range(self.columns):
            for row in range(self.rows - 3):
                if all(self.board[row + i][col] == player for i in range(4)):
                    return True

        # Vérification diagonale (de haut-gauche à bas-droit)
        for row in range(self.rows - 3):
            for col in range(self.columns - 3):
                if all(self.board[row + i][col + i] == player for i in range(4)):
                    return True

        # Vérification diagonale (de bas-gauche à haut-droit)
        for row in range(3, self.rows):
            for col in range(self.columns - 3):
                if all(self.board[row - i][col + i] == player for i in range(4)):
                    return True

        return False

    def is_full(self):
        """
        Vérifie si la grille est complètement remplie.
        Retourne True si toutes les colonnes sont pleines, sinon False.
        """
        return all(self.board[0][col] != VIDE for col in range(self.columns))


def draw_board(screen, game):
    """
    Dessine la grille et les jetons sur la fenêtre.
    """
    for row in range(game.rows):
        for col in range(game.columns):
            # Dessiner le rectangle bleu représentant une cellule de la grille
            pygame.draw.rect(screen, COULEUR_GRILLE,
                             (col * LARGEUR_COLONNE, (row + 1) * HAUTEUR_LIGNE, LARGEUR_COLONNE, HAUTEUR_LIGNE))
            # Choisir la couleur du jeton (vide, joueur 1 ou joueur 2)
            couleur = COULEUR_VIDE
            if game.board[row][col] == JOUEUR_1:
                couleur = COULEUR_JOUEUR_1
            elif game.board[row][col] == JOUEUR_2:
                couleur = COULEUR_JOUEUR_2

            # Dessiner le jeton comme un cercle dans la cellule
            pygame.draw.circle(screen, couleur,
                               (col * LARGEUR_COLONNE + LARGEUR_COLONNE // 2,
                                (row + 1) * HAUTEUR_LIGNE + HAUTEUR_LIGNE // 2), LARGEUR_COLONNE // 2 - MARGE)


def main():
    """
    Fonction principale qui gère la boucle du jeu.
    """
    pygame.init()  # Initialisation de Pygame
    screen = pygame.display.set_mode(DIMENSIONS)  # Créer la fenêtre de jeu
    pygame.display.set_caption("Puissance 4")  # Titre de la fenêtre
    clock = pygame.time.Clock()  # Gère la vitesse de rafraîchissement

    game = ConnectFour()  # Initialisation de l'objet ConnectFour
    running = True  # Contrôle si le jeu est en cours
    font = pygame.font.SysFont("monospace", 50)  # Police pour afficher les messages

    while running:
        screen.fill((0, 0, 0))  # Remplir l'écran de noir avant chaque rafraîchissement

        # Dessiner la grille et les jetons
        draw_board(screen, game)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Quitter le jeu si l'utilisateur ferme la fenêtre
                running = False
                break

            if event.type == pygame.MOUSEBUTTONDOWN:  # Gestion des clics
                x = event.pos[0]  # Récupérer la position X de la souris
                column = x // LARGEUR_COLONNE  # Calculer la colonne cliquée

                if game.drop_piece(column):  # Tenter de déposer un jeton
                    if game.check_victory():  # Vérifier si le joueur a gagné
                        draw_board(screen, game)
                        winner_text = font.render(f"Joueur {game.current_player} gagne!", True, (255, 255, 255))
                        screen.blit(winner_text, (40, 10))
                        pygame.display.update()
                        pygame.time.wait(5000)
                        running = False
                    elif game.is_full():  # Vérifier si la grille est pleine
                        draw_board(screen, game)
                        draw_text = font.render("Match nul!", True, (255, 255, 255))
                        screen.blit(draw_text, (50, 10))
                        pygame.display.update()
                        pygame.time.wait(5000)
                        running = False

                    game.switch_player()  # Passer au joueur suivant

        pygame.display.update()  # Mettre à jour l'affichage
        clock.tick(60)  # Limiter la vitesse à 60 images par seconde

    pygame.quit()  # Quitter Pygame
    sys.exit()  # Terminer le programme


if __name__ == "__main__":
    main()  # Démarrer le jeu
