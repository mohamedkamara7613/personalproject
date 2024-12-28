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