#ifndef CITY_LOADER_H
#define CITY_LOADER_H

#include "graphe.h"
#include "astar_algo.h" // For Direction enum

/**
 * \struct CityConfig
 * \brief Configuration d'une ville (labyrinthe) chargée depuis un fichier
 */
typedef struct {
    G_Graphe graph;       /*!< Le graphe représentant la connectivité de la ville */
    int width;            /*!< Largeur de la ville (nombre de colonnes) */
    int height;           /*!< Hauteur de la ville (nombre de lignes) */
    int start_node;       /*!< ID du noeud de départ */
    Direction start_dir;  /*!< Direction initiale du robot au départ */
    int checkpoints[100]; /*!< Liste des points de passage */
    int num_checkpoints;  /*!< Nombre de points de passage */
} CityConfig;

/**
 * \brief Charge une ville (labyrinthe) depuis un fichier texte
 * \details Le format attendu est :
 * - Taille (Ex: 10 10)
 * - Depart Direction (Ex: 0 N)
 * - Arrivee Direction (Ex: 99 S)
 * - Liste des arêtes (Ex: 0-1)
 * 
 * \param filename Chemin vers le fichier de configuration de la ville
 * \return Une structure CityConfig contenant le graphe et les informations de configuration.
 *         En cas d'erreur de chargement, le graphe peut être vide ou incomplet.
 */
CityConfig load_city(const char* filename);

#endif
