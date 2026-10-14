/**
 * \file graphe.h
 * \brief Fichier d'en-tête pour des graphes orientés ou non, étiquetés ou non, valués ou non
 * \author N. Delestre
 * \version 1.0
 * \date 2025
 */

#ifndef __GRAPHE__
#define __GRAPHE__
#include <stdlib.h>
#include <stdbool.h>
#include <errno.h>
#include "copieLiberationComparaison.h"
#include "ListeChaineeListe.h"
#include "TableHachageDictionnaire.h"

typedef struct {
  unsigned int src; // id du sommet source
  unsigned int dest; // id du sommet destination
} G_Arc;

typedef struct {
  bool oriente; // true si le graphe est orienté, false sinon
  LCL_Liste sommets; // liste des ids des sommets présents dans le graphe
  LCL_Liste arcs; // liste des arcs présents dans le graphe (type G_Arc)
  THD_Dictionnaire etiquettes; // table de hachage des étiquettes des sommets (clé : id du sommet, valeur : étiquette). Vide si le graphe n'est pas étiqueté
  void* (*copierEtiquette) (void*); // fonction de copie d'étiquette. Null si le graphe n'est pas étiqueté
  void (*libererEtiquette) (void*); // fonction de libération d'étiquette. Null si le graphe n'est pas étiqueté
  int (*comparerEtiquettes) (void*, void*); // fonction de comparaison d'étiquettes. Null si le graphe n'est pas étiqueté
  THD_Dictionnaire valeurs; // table de hachage des valeurs des arcs (clé : G_Arc, valeur : valeur de l'arc)
  void* (*copierValeur) (void*); // fonction de copie de valeur. Null si le graphe n'est pas valué
  void (*libererValeur) (void*); // fonction de libération de valeur. Null si le graphe n'est pas valué
  int (*comparerValeurs) (void*, void*); // fonction de comparaison de valeurs. Null si le graphe n'est pas valué
} G_Graphe;

#define G_GRAPHE_NON_ETIQUETE_ERREUR 1
#define G_GRAPHE_ETIQUETE_ERREUR 2
#define G_GRAPHE_NON_VALUE_ERREUR 3
#define G_GRAPHE_VALUE_ERREUR 4
#define G_SOMMET_ERREUR 5
#define G_ARC_ERREUR 6
#define G_GRAPHE_INCOHERENT_ERREUR 7
#define G_MEMOIRE_ERREUR 8

/**
 * \brief Crée un graphe
 * \param oriente Booléen indiquant si le graphe est orienté (true) ou non (false)
 * \param G_copierEtiquette Pointeur vers une fonction de copie d'étiquette (pour les sommets)
 * \param G_libererEtiquette Pointeur vers une fonction de libération d'étiquette (pour les sommets)
 * \param G_comparerEtiquettes Pointeur vers une fonction de comparaison d'étiquettes (pour les sommets)
 * \param G_copierValeur Pointeur vers une fonction de copie de valeur (pour les arcs)
 * \param G_libererValeur Pointeur vers une fonction de libération de valeur (pour les arcs)
 * \param G_comparerValeurs Pointeur vers une fonction de comparaison de valeurs (pour les arcs)
 * \brief pour les graphes non étiquetés, G_copierEtiquette, G_libererEtiquette et G_comparerEtiquettes doivent être NULL. Pour les graphes non valués, G_copierValeur, G_libererValeur et G_comparerValeurs doivent être NULL.
 * \return Le graphe créé. Si les trois fonctions de gestion des étiquettes et des valeurs ne sont pas bien renseignés ensemble, errno contient le code d'erreur : G_GRAPHE_INCOHERENT_ERREUR
 * 
 */
G_Graphe G_graphe(bool oriente,
		  void* (*copierEtiquette) (void*),
		  void (*libererEtiquette) (void*),
		  int (*comparerEtiquettes) (void*, void*),
		  void* (*copierValeur) (void*),
		  void (*libererValeur) (void*),
		  int (*comparerValeurs) (void*, void*));

/**
 * \brief Ajoute un sommet au graphe
 * \param pg Pointeur vers le graphe
 * \param id Identifiant du sommet à ajouter, il ne doit pas être déjà présent dans le graphe
 * \param petiquette  Pointeur vers l'étiquette du sommet à ajouter (NULL si le graphe n'est pas étiqueté)
 * \return L'id du sommet ajouté, ou -1 en cas d'erreur et errno contient le code d'erreur : G_SOMMET_ERREUR
 */
int G_ajouterSommet(G_Graphe *pg, unsigned int id, void *petiquette);

/**
 * \brief Ajoute un arc entre deux sommets du graphe
 * \param pg Pointeur vers le graphe
 * \param idSrc Indice du sommet source
 * \param idDest Indice du sommet destination
 * \param pvaleur Pointeur vers la valeur de l'arc à ajouter (NULL si le graphe n'est pas valué)
 * \return 0 si l'arc a été ajouté avec succès, -1 en cas d'erreur. Dans ce cas la variable errno contient le code d'erreur : G_SOMMET_ERREUR ou G_GRAPHE_NON_VALUE_ERREUR
 */
int G_ajouterArc(G_Graphe *pg, unsigned int idSrc, unsigned int idDest, void *pvaleur);

/**
 * \brief Vérifie si un sommet est présent dans le graphe
 * \param g Le graphe
 * \param id L'id du sommet à vérifier
 * \return true si le sommet est présent, false sinon
 */
bool G_sommetPresent(G_Graphe g, unsigned int id);

/**
 * \brief Vérifie si un arc est présent entre deux sommets du graphe
 * \param g Le graphe
 * \param idSrc L'id du sommet source
 * \param idDest L'id du sommet destination
 * \return true si l'arc est présent, false sinon
 */
bool G_arcPresent(G_Graphe g, unsigned int idSrc, unsigned int idDest);

/**
 * \brief Supprime un sommet du graphe
 * \param pg Pointeur vers le graphe
 * \param id Indice du sommet à supprimer
 * \return 0 si le sommet a été supprimé avec succès, -1 en cas d'erreur. Dans ce cas la variable errno contient le code d'erreur : G_SOMMET_ERREUR
 * \note La suppression d'un sommet entraîne la suppression de tous les arcs associés à ce sommet
 */
int G_supprimerSommet(G_Graphe *pg, unsigned int id);

/**
 * \brief Supprime un arc entre deux sommets du graphe
 * \param pg Pointeur vers le graphe
 * \param idSrc Indice du sommet source
 * \param idDest Indice du sommet destination
 * \return 0 si l'arc a été supprimé avec succès, -1 en cas d'erreur. Dans ce cas la variable errno contient le code d'erreur : G_SOMMET_ERREUR
 */
int G_supprimerArc(G_Graphe *pg, unsigned int idSrc, unsigned int idDest);

/**
 * \brief Retourne un tableau des ids des sommets présents dans le graphe
 * \param g Le graphe
 * \return Une liste chaînée contenant les ids des sommets présents dans le graphe 
 */
LCL_Liste G_sommets(G_Graphe g);

/**
 * \brief Retourne un tableau des ids des sommets adjacents à un sommet donné
 * \param g Le graphe
 * \param idSrc Indice du sommet dont on veut connaître les sommets adjacents
 * \return Une liste chaînée contenant les ids des sommets adjacents au sommet donné. En cas d'erreur (sommet inexistant), la fonction retourne une liste vide et la variable errno contient le code d'erreur : G_SOMMET_ERREUR
 */
LCL_Liste G_obtenirSommetsAdjacents(G_Graphe g, unsigned int idSrc);

/**
 * \brief Retourne l'étiquette d'un sommet
 * \param g Le graphe
 * \param id Indice du sommet dont on veut connaître l'étiquette
 * \return Un pointeur vers l'étiquette du sommet (une copie qui devra être libérée par l'utilisateur). En cas d'erreur (sommet inexistant ou graphe non étiqueté), la fonction retourne NULL et la variable errno contient le code d'erreur : G_SOMMET_ERREUR ou G_GRAPHE_NON_ETIQUETE_ERREUR
 */
void* G_obtenirEtiquette(G_Graphe g, unsigned int id);

/**
 * \brief Modifie l'étiquette d'un sommet
 * \param pg Pointeur vers le graphe
 * \param id Indice du sommet dont on veut modifier l'étiquette
 * \param petiquette Pointeur vers la nouvelle étiquette du sommet
 * \return 0 si l'étiquette a été modifiée avec succès, -1 en cas d'erreur. Dans ce cas la variable errno contient le code d'erreur : G_SOMMET_ERREUR ou G_GRAPHE_NON_ETIQUETE_ERREUR
 */
 
int G_fixerEtiquette(G_Graphe *pg, unsigned int id, void *petiquette);

/**
 * \brief Retourne la valeur d'un arc entre deux sommets
 * \param g Le graphe
 * \param idSrc Indice du sommet source
 * \param idDest Indice du sommet destination
 * \return Un pointeur vers la valeur de l'arc (une copie qui devra être libérée par l'utilisateur). En cas d'erreur (sommet inexistant, arc inexistant ou graphe non valué), la fonction retourne NULL et la variable errno contient le code d'erreur : G_SOMMET_ERREUR, G_GRAPHE_NON_VALUE_ERREUR
 */
void* G_obtenirValeur(G_Graphe g, unsigned int idSrc, unsigned int idDest);

/**
 * \brief Modifie la valeur d'un arc entre deux sommets
 * \param pg Pointeur vers le graphe
 * \param idSrc Indice du sommet source
 * \param idDest Indice du sommet destination
 * \param pvaleur Pointeur vers la nouvelle valeur de l'arc
 * \return 0 si la valeur a été modifiée avec succès, -1 en cas d'erreur. Dans ce cas la variable errno contient le code d'erreur : G_SOMMET_ERREUR, G_GRAPHE_NON_VALUE_ERREUR ou G_ARC_ERREUR
 */
int G_fixerValeur(G_Graphe *pg, unsigned int idSrc, unsigned int idDest, void *pvaleur);

/**
 * \brief Vide le graphe en supprimant tous les sommets et arcs
 * \param pg Pointeur vers le graphe
 */
void G_vider(G_Graphe *pg);

#endif 
