#ifndef ASTAR_H
#define ASTAR_H

#include "graphe.h"

/**
 * \enum Direction
 * \brief Directions cardinales pour le déplacement du robot
 */
typedef enum {
    NORTH = 0, /*!< Nord */
    EAST = 1,  /*!< Est */
    SOUTH = 2, /*!< Sud */
    WEST = 3   /*!< Ouest */
} Direction;

/**
 * \enum ActionType
 * \brief Types d'actions possibles pour le robot
 */
typedef enum {
    ACTION_AV = 0, /*!< Avancer */
    ACTION_TD = 1, /*!< Tourner à droite */
    ACTION_TG = 2  /*!< Tourner à gauche */
} ActionType;

/**
 * \struct Step
 * \brief Représente une étape (action) dans le chemin calculé
 */
typedef struct {
    ActionType type;  /*!< Type d'action (AV, TD, TG) */
    int target_node;  /*!< Noeud destination après l'action (pour AV). Pour une rotation, c'est le même noeud. */
} Step;

// Costs
#define COST_MOVE 1
#define COST_TURN 2

/**
 * \brief Exécute l'algorithme A* pour trouver le chemin le plus court
 * \param g Le graphe représentant la carte
 * \param width Largeur de la carte (pour calculer les coordonnées)
 * \param start_node ID du noeud de départ
 * \param start_dir Direction initiale du robot
 * \param target_node ID du noeud d'arrivée
 * \param[out] total_cost Pointeur vers le coût total du chemin
 * \param[out] rotation_count Pointeur vers le nombre de rotations effectuées
 * \param[out] steps_len Pointeur vers le nombre d'étapes (taille du tableau retourné)
 * \return Un tableau de Step (étapes) représentant le chemin, se terminant par une étape de type -1. Doit être libéré par l'appelant.
 */
Step* astar_search(G_Graphe g, int width, int start_node, Direction start_dir, int target_node, int* total_cost, int* rotation_count, int* steps_len);

/**
 * \brief Stratégie gloutonne utilisant A* pour visiter une liste de checkpoints
 * \param g Le graphe représentant la carte
 * \param width Largeur de la carte
 * \param start_node ID du noeud de départ
 * \param start_dir Direction initiale du robot
 * \param checkpoints Tableau des IDs des noeuds à visiter
 * \param num_checkpoints Nombre de checkpoints
 * \param[out] total_len Pointeur vers la longueur totale du tableau d'étapes retourné
 * \param[out] total_cost Pointeur vers le coût total du parcours
 * \param[out] total_rotations Pointeur vers le nombre total de rotations
 * \return La séquence complète des actions (Step*) pour visiter tous les checkpoints.
 */
Step* greedy_astar_patrol(G_Graphe g, int width, int start_node, Direction start_dir, int* checkpoints, int num_checkpoints, int* total_len, int* total_cost, int* total_rotations);

#endif
