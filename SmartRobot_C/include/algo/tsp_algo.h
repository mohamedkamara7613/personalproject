#ifndef TSP_H
#define TSP_H

#include "graphe.h"
#include "astar_algo.h"

/**
 * \brief Résout le problème du voyageur de commerce (TSP) en utilisant A*
 * \details Cette fonction tente de trouver un chemin optimal visitant tous les checkpoints
 * en utilisant une heuristique gloutonne ou une autre approche, tout en prenant en compte
 * les coûts de déplacement et de rotation du robot.
 * 
 * \param g Le graphe représentant la carte
 * \param width Largeur de la carte (taille)
 * \param start_node ID du noeud de départ
 * \param start_dir Direction initiale du robot
 * \param checkpoints Tableau des IDs des noeuds à visiter
 * \param num_checkpoints Nombre de checkpoints à visiter
 * \param[out] total_actions Pointeur vers le nombre total d'actions dans le chemin retourné
 * \param[out] total_cost Pointeur vers le coût total (déplacements + rotations)
 * \param[out] total_rots Pointeur vers le nombre total de rotations
 * \return Un tableau de Step représentant la séquence complète d'actions pour le parcours TSP.
 */
Step* solve_tsp_astar(G_Graphe g, int width, int start_node, Direction start_dir, int* checkpoints, int num_checkpoints, int* total_actions, int* total_cost, int* total_rots);

#endif
