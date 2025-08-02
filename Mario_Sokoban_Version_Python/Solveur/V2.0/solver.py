# coding: utf-8
"""
    starting at Wen 27 juil 2025
    Par Mohamed Kamara
--------------------- Mario Sokoban Solver --------------------------
"""

# Globals
_solver_thread = None
stop_solver = False
current_level = None

from data import nb_bloc_width, nb_bloc_height, items

from gestion_file import load_level


from typing import Tuple, FrozenSet, List
from dataclasses import dataclass
import heapq
import pygame
import time
import threading


# ---------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------

@dataclass(frozen=True)
class Etat:
    joueur: Tuple[int, int]
    caisses: FrozenSet[Tuple[int, int]]
    objectifs: FrozenSet[Tuple[int, int]]

    @staticmethod
    def from_grille() -> "Etat":
        from game import grille
        caisses = set()
        objectifs = set()
        joueur = None

        for x in range(nb_bloc_width):  # lignes
            for y in range(nb_bloc_height):  # colonnes
                val = grille[x][y]

                if val == items["CAISSE"] or val == items["CAISSE_OK"]:
                    caisses.add((x, y))
                if val == items["OBJECTIF"] or val == items["CAISSE_OK"]:
                    objectifs.add((x, y))
                if val == items["JOUEUR"]:
                    joueur = (x, y)

        if joueur is None:
            raise ValueError("Position du joueur non trouvée dans la grille.")

        return Etat(joueur=joueur, caisses=frozenset(caisses), objectifs=frozenset(objectifs))
# ---------------------------------------------------------------------------------------------------------------------------
    def est_etat_final(self) -> bool:
        return self.caisses == self.objectifs
    
# ---------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------

class Noeud:
    def __init__(self, etat, parent=None, action=None, g=0, h=0):
        self.etat = etat            # Un objet de type Etat
        self.parent = parent        # Noeud précédent
        self.action = action        # Action pour passer de parent à self (optionnel ici)
        self.g = g                  # Coût depuis le départ
        self.h = h                  # Estimation coût restant
        self.f = g + h              # Score total

    def __lt__(self, other):
        """Permet de comparer deux nœuds selon f, utile pour la file de priorité."""
        return self.f < other.f

    def chemin(self):
        """Reconstruit le chemin depuis le départ jusqu’à ce noeud."""
        noeud, chemin = self, []
        while noeud.parent is not None:
            chemin.append(noeud)
            noeud = noeud.parent
        chemin.append(noeud)  # ajouter l’état initial
        chemin.reverse()
        return chemin

# ---------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------

def successeurs(etat: Etat) -> List[Etat]:
    """
        Pour chaque direction :

            Calculer la nouvelle position du joueur (x1, y1)

            Si la case (x1, y1) est :

                - Un mur → on ignore

                - Une caisse :
                    Calculer (x2, y2) la case derrière
                    Vérifier que (x2, y2) est libre
                    Si oui → pousser la caisse (la déplacer)

                - Libre → bouger le joueur

            Créer un nouvel Etat avec :
                Nouvelle position du joueur
                Nouvelles positions des caisses (copiées et modifiées si une a bougé)
                Même grille
                Liste d’actions mise à jour
    """
    from game import grille
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # gauche, droite, haut, bas
    resultats = []
    actions_correspondantes = []

    for dx, dy in directions:
        nx = etat.joueur[0] + dx
        ny = etat.joueur[1] + dy
        destination = (nx, ny)

        # Vérifie que la case de destination est dans la grille
        if not (0 <= nx < nb_bloc_width and 0 <= ny < nb_bloc_height):
            continue

        # Si c'est un mur, on ne peut pas y aller
        if grille[nx][ny] == items["MUR"]:
            continue
        
        action = "aucune"  # Action par défaut si aucune caisse n'est poussée
        if dx == -1:
            action = "gauche"
        elif dx == 1:
            action = "droite"
        elif dy == -1:
            action = "haut"
        elif dy == 1:
            action = "bas"

        # Si on pousse une caisse
        if destination in etat.caisses:
            # Position après la caisse
            cx, cy = nx + dx, ny + dy
            pos_apres_caisse = (cx, cy)

            # Vérifie si la case après la caisse est libre
            if not (0 <= cx < nb_bloc_width and 0 <= cy < nb_bloc_height):
                continue
            if grille[cx][cy] == items["MUR"]:
                continue
            if pos_apres_caisse in etat.caisses:
                continue  # une autre caisse bloque

            # Construire le nouvel état
            nouvelles_caisses = set(etat.caisses)
            nouvelles_caisses.remove(destination)
            nouvelles_caisses.add(pos_apres_caisse)

            nouvel_etat = Etat(joueur=destination,
                            caisses=frozenset(nouvelles_caisses),
                            objectifs=etat.objectifs)
            resultats.append(nouvel_etat)
            actions_correspondantes.append(action)  # Ajouter l'action de pousser la caisse
        else:
            # Avancer sans pousser de caisse
            nouvel_etat = Etat(joueur=destination,
                            caisses=etat.caisses,
                            objectifs=etat.objectifs)
            resultats.append(nouvel_etat)
            actions_correspondantes.append(action)  # Ajouter l'action de déplacement
            
    return list(zip(resultats, actions_correspondantes))  # Retourne la liste des nouveaux états et les actions correspondantes

# ---------------------------------------------------------------------------------------------------------------------------

def heuristique(etat: Etat) -> int:
    total = 0
    objectifs_restants = set(etat.objectifs)

    for caisse in etat.caisses:
        min_dist = min(abs(caisse[0] - obj[0]) + abs(caisse[1] - obj[1]) for obj in objectifs_restants)
        total += min_dist

    return total

# ---------------------------------------------------------------------------------------------------------------------------

def a_star(etat_initial: Etat):
    # Noeud initial
    noeud_initial = Noeud(etat=etat_initial, g=0, h=heuristique(etat_initial))

    # File de priorité (open list)
    open_list = []
    heapq.heappush(open_list, noeud_initial)

    # Ensemble des états déjà explorés
    closed_set = set()

    while open_list:
        # Prendre le noeud avec le plus petit f
        noeud_courant = heapq.heappop(open_list)
        log_recherche(f"Exploration du noeud : {noeud_courant.etat.joueur} avec {len(noeud_courant.etat.caisses)} caisses.")

        # Si c’est l’état final, on retourne le chemin jusqu’à cet état
        if noeud_courant.etat.est_etat_final():
            return noeud_courant.chemin()

        # Marquer l’état comme visité
        closed_set.add(noeud_courant.etat)
        
        # Explorer les successeurs
        for (nouvel_etat, action_correspondante) in successeurs(noeud_courant.etat):
            if nouvel_etat in closed_set:
                continue

            g = noeud_courant.g + 1  # coût fixe de 1 par action
            h = heuristique(nouvel_etat)
            nouveau_noeud = Noeud(
                etat=nouvel_etat,
                parent=noeud_courant,
                action=action_correspondante,
                g=g,
                h=h
            )

            heapq.heappush(open_list, nouveau_noeud)

    return None  # Pas de solution trouvée
# ---------------------------------------------------------------------------------------------------------------------------
def envoyer_actions(level, delay: float = 0.2):
    """Envoie les événements Pygame correspondant aux actions (haut, bas, gauche, droite)."""
    global stop_solver, current_level
    
    mapping = {
        "haut": pygame.K_UP,
        "bas": pygame.K_DOWN,
        "gauche": pygame.K_LEFT,
        "droite": pygame.K_RIGHT
    }
    actions = main(level)  # Remplacez 0 par le niveau souhaité
    for i, action in enumerate(actions):
        if stop_solver or current_level != level:
            log_recherche("[Solver] Arrêt demandé.")
            return
        
        if action not in mapping:
            continue  # Ignore les actions inconnues

        log_recherche(f"➡️ Action {i+1}/{len(actions)} : {action}")
        event = pygame.event.Event(pygame.KEYDOWN, key=mapping[action])
        pygame.event.post(event)
        time.sleep(delay)  # temporisation entre les coups
# ---------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------

def main(level):
    log_recherche(f"----------- Chargement du niveau {level+1} -----------")

    load_level(level)  # charge le niveau spécifié et remplit la grille
    etat_initial = Etat.from_grille()
    log_recherche(": État initial généré.")

    log_recherche(": Lancement de A*...")
    solution = a_star(etat_initial)
    actions = []
     # Filtrer les actions inutiles
    if solution:
        log_recherche(": ✅ Solution trouvée !")
        
        for noeud in solution:
            actions.append(noeud.action)
            
        actions = [action for action in actions if action != None]
        log_recherche(f": {len(actions)} actions à entreprendre.")
        log_recherche(f"  {actions}")
    else:
        log_recherche("❌ Aucune solution trouvée.")

    return actions
# ---------------------------------------------------------------------------------------------------------------------------
def run_solver(niveau, delay):
    global _solver_thread, stop_solver, current_level
    
    # Stop previous solver
    if _solver_thread and _solver_thread.is_alive():
        stop_solver = True
        _solver_thread.join()
        
    stop_solver = False
    current_level = niveau
    
    _solver_thread = threading.Thread(target=envoyer_actions, args=(niveau, delay))
    _solver_thread.daemon = True
    _solver_thread.start()
    
def log_recherche(msg):
    from game import ajouter_log
    ajouter_log(f"[Recherche] {msg}")


"""
Exemple de grille après chargement du niveau 0 :
000111111100
000111111100
000420003100
000111111100
000111111100
000111111100
000000000000
000000000000
000000000000 


"""