# -*- coding: utf-8 -*-

"""
Documentation des fonctions pour le projet Puissance 4.
Ce fichier regroupe les signatures, paramètres et descriptions des fonctions
de tous les fichiers (à savoir `game_logic.py`, `game_ui.py` et `ai_engine.py`).
"""

# ----------- Fichier : game_logic.py -----------

def __init__(self, rows=6, columns=7, starting_player=1):
    """
    Initialisation de la classe ConnectFour.
    
    Paramètres :
        rows (int) : Nombre de lignes du plateau (par défaut 6).
        columns (int) : Nombre de colonnes du plateau (par défaut 7).
        starting_player (int) : Joueur qui commence (1 ou 2).
    """


def drop_piece(self, column):
    """
    Ajoute un jeton dans une colonne si valide.
    
    Paramètres :
        column (int) : Index de la colonne où déposer le jeton.
    
    Retour :
        bool : True si le coup est valide, False sinon.
    """


def switch_player(self):
    """
    Change le joueur actuel (1 <-> 2).
    
    Paramètres :
        Aucun.
    
    Retour :
        None.
    """


def check_horizontal(self, player):
    """
    Vérifie les alignements horizontaux pour le joueur donné.
    
    Paramètres :
        player (int) : Joueur (1 ou 2).
    
    Retour :
        bool : True si un alignement est trouvé, False sinon.
    """


def check_vertical(self, player):
    """
    Vérifie les alignements verticaux pour le joueur donné.
    
    Paramètres :
        player (int) : Joueur (1 ou 2).
    
    Retour :
        bool : True si un alignement est trouvé, False sinon.
    """


def check_diagonal(self, player):
    """
    Vérifie les alignements diagonaux (montants et descendants).
    
    Paramètres :
        player (int) : Joueur (1 ou 2).
    
    Retour :
        bool : True si un alignement est trouvé, False sinon.
    """


def check_victory(self):
    """
    Vérifie si le joueur actuel a gagné (horizontale, verticale, diagonale).
    
    Paramètres :
        Aucun.
    
    Retour :
        bool : True si victoire, False sinon.
    """


def is_full(self):
    """
    Vérifie si le plateau est plein.
    
    Paramètres :
        Aucun.
    
    Retour :
        bool : True si le plateau est plein, False sinon.
    """

# ----------- Fichier : game_ui.py -----------

def draw_board(game):
    """
    Affiche la grille dans la console avec des symboles colorés.
    
    Paramètres :
        game (ConnectFour) : Instance de la classe ConnectFour contenant le plateau.
    
    Retour :
        None.
    """


def get_player_input():
    """
    Demande à l'utilisateur de choisir une colonne via la console.
    
    Paramètres :
        Aucun.
    
    Retour :
        int : Index de la colonne choisie.
    """


def display_message(message, color_code="\033[32m"):
    """
    Affiche un message dans la console avec une couleur spécifique.
    
    Paramètres :
        message (str) : Message à afficher.
        color_code (str) : Code couleur ANSI pour styliser le texte.
    
    Retour :
        None.
    """

# ----------- Fichier : ai_engine.py -----------

def coup_possible(board):
    """
    Renvoie la liste des colonnes où un jeton peut être déposé.
    
    Paramètres :
        board (list[list[int]]) : Plateau de jeu (2D).
    
    Retour :
        list[int] : Liste des indices des colonnes disponibles.
    """


def simulation(board, player):
    """
    Simule une partie aléatoire à partir d'un plateau donné.
    
    Paramètres :
        board (list[list[int]]) : Plateau de jeu (2D).
        player (int) : Joueur qui commence la simulation.
    
    Retour :
        int : Vainqueur (1 ou 2), ou 0 pour un match nul.
    """


def evaluate(board, player, nb_simulations=10):
    """
    Evalue une position donnée en effectuant plusieurs simulations.
    
    Paramètres :
        board (list[list[int]]) : Plateau de jeu (2D).
        player (int) : Joueur évaluant la position (1 ou 2).
        nb_simulations (int) : Nombre de simulations à effectuer (par défaut 10).
    
    Retour :
        tuple[int, int, int] : (nuls, victoires joueur 1, victoires joueur 2).
    """


def minimax(board, depth, maximizing_player, alpha=-float('inf'), beta=float('inf')):
    """
    Implémente l'algorithme Minimax avec élagage alpha-bêta.
    
    Paramètres :
        board (list[list[int]]) : Plateau de jeu (2D).
        depth (int) : Profondeur maximale de l'arbre de recherche.
        maximizing_player (bool) : Indique si c'est au tour du joueur maximisant.
        alpha (float) : Valeur alpha pour l'élagage (par défaut -infini).
        beta (float) : Valeur beta pour l'élagage (par défaut +infini).
    
    Retour :
        float : Meilleur score possible pour la position actuelle.
    """

def get_ai_move(board, depth, maximizing_player=True):
    """
    Calcule le meilleur coup pour l'IA à l'aide de l'algorithme Minimax.
    
    Paramètres :
        board (list[list[int]]) : Plateau de jeu.
        depth (int) : Profondeur maximale de recherche.
        maximizing_player (bool) : True si l'IA maximise son score.
    
    Retour :
        int : Index de la colonne correspondant au meilleur coup.
    """