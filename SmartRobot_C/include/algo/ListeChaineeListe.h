/**
 * \file ListeChaineeListe.h
 * \brief Interface d'une liste générique basée sur liste chaînée,
 *        avec insertion/suppression par position, accès par position,
 *        et suivi en O(1) de la longueur.
 * \author Nicolas Delestre et IA générative
 * \version 1.0
 * \date 2025
 *
 * Cette couche "Liste" encapsule la structure de liste chaînée de bas niveau
 * (voir listeChainee.h) pour offrir des opérations par position (1..n),
 * une gestion de la copie/libération des éléments, et le suivi de la longueur.
 *
 * Convention d'indexation :
 *   - Les positions sont **0..longueur-1** (0 = tête de liste).
 *   - Toute position hors de cet intervalle produit une erreur.
 *
 * Gestion mémoire des éléments :
 *   - A l'insertion, l'élément fourni est **copié** via `copierElement`.
 *   - A la suppression/vidage, les éléments sont libérés via `supprimerElement`.
 *   - La liste contient donc ses **propres copies** ; l'appelant reste libre
 *     de gérer la durée de vie de ses objets d'entrée.
 */

#ifndef __LISTECHAINEELISTE_H__
#define __LISTECHAINEELISTE_H__

#include <stdbool.h>
#include "listeChainee.h"
#include "copieLiberationComparaison.h"

/** \brief La liste est vide (par ex. lecture/suppression impossible). */
#define LISTE_VIDE_ERREUR 3

/** \brief La position indiquée n'appartient pas à 0..longueur-1. */
#define POSITION_HORS_BORNES_ERREUR 4

/*----------------------------------------------------------------------------
 * Types
 *----------------------------------------------------------------------------*/

/**
 * \struct LCL_Liste
 * \brief Liste générique avec suivi de la longueur.
 *
 * Les champs sont publics pour l'implémentation, mais l'utilisateur
 * doit passer par les fonctions de l'API.
 */
typedef struct {
  LC_ListeChainee    liste;             /**< Ancre de la liste chaînée bas niveau. */
  CLC_FonctionCopier copierElement;     /**< Copie profonde d'un élément (à l'insertion). */
  CLC_FonctionLiberer supprimerElement; /**< Libération d'un élément (à la suppression/vidage). */
  int                longueur;          /**< Longueur courante (toujours >= 0). */
} LCL_Liste;

/*----------------------------------------------------------------------------
 * Construction / propriétés
 *----------------------------------------------------------------------------*/

/**
 * \fn LCL_liste
 * \brief Construit une liste vide avec fonctions de copie et libération.
 *
 * \param copierElement   Fonction qui duplique un élément (copie profonde).
 * \param supprimerElement Fonction qui libère un élément.
 * \return LCL_Liste      Une liste vide prête à l'emploi.
 *
 * \post LCL_estVide(retour) == true, LCL_longueur(retour) == 0
 */
LCL_Liste LCL_liste(CLC_FonctionCopier copierElement,
                    CLC_FonctionLiberer supprimerElement);

/**
 * \fn LCL_estVide
 * \brief Indique si la liste est vide.
 *
 * \param liste  Liste considérée.
 * \return bool  true ssi longueur == 0.
 * \complexite O(1)
 */
bool LCL_estVide(LCL_Liste liste);

/**
 * \fn LCL_longueur
 * \brief Longueur de la liste.
 *
 * \param liste  Liste considérée.
 * \return int   Nombre d'éléments (>= 0).
 * \complexite O(1)
 */
int LCL_longueur(LCL_Liste liste);

/**
 * \fn LCL_inserer
 * \brief Insère une **copie** de l'élément à la position demandée.
 *
 * \param pliste    Pointeur sur la liste.
 * \param element   Pointeur sur l'élément à copier (jamais stocké tel quel).
 * \param position  Entier 0..longueur.
 *
 * \pre pliste != NULL ; 0 <= position <= LCL_longueur(*pliste)
 * \post LCL_longueur(*pliste) est incrémentée de 1 si succès.
 *
 * \erreurs
 *   - POSITION_HORS_BORNES_ERREUR si position n'appartient pas [0..longueur]
 *   - autres erreurs possibles selon l'allocateur interne
 *
 * \complexite O(n) (liste chaînée simple).
 */
void LCL_inserer(LCL_Liste* pliste, void* element, unsigned int position);

/**
 * \fn LCL_supprimer
 * \brief Supprime l'élément à la position donnée (0..longueur-1).
 *
 * \param pliste    Pointeur sur la liste.
 * \param position  Entier 0..longueur.
 *
 * \pre pliste != NULL ; 0 <= position < LCL_longueur(*pliste)
 * \post LCL_longueur(*pliste) est décrémentée de 1 si succès.
 *
 * \erreurs
 *   - LISTE_VIDE_ERREUR si la liste est vide
 *   - POSITION_HORS_BORNES_ERREUR si position n'appartient pas [1..longueur]
 *
 * \complexite O(n)
 */
void LCL_supprimer(LCL_Liste* pliste, unsigned int position);

/**
 * \fn LCL_element
 * \brief **Copie** l'élément situé à la position demandée et la retourne.
 *
 * \param liste     Liste source (non modifiée).
 * \param position  Entier 0..longueur 
 * \return void*    Copie de l'élément (à libérer par l'appelant avec la
 *                  fonction adéquate), ou NULL si erreur.
 *
 * \erreurs (via errno)
 *   - LISTE_VIDE_ERREUR si la liste est vide
 *   - POSITION_HORS_BORNES_ERREUR si position n'appartient pas [1..longueur]
 *
 * \remarques
 *   - Cette fonction respecte la sémantique de copie : l'objet retourné
 *     est indépendant de celui stocké dans la liste.
 *   - L'appelant devient propriétaire du pointeur retourné et doit
 *     le libérer avec la fonction adaptée (ex: celle symétrique à
 *     `copierElement`).
 *
 * \complexite O(n)
 */
void* LCL_element(LCL_Liste liste, unsigned int position);

/**
 * \fn LCL_copier
 * \brief Copie entière de la liste (éléments inclus).
 *
 * \param liste  Liste source.
 * \return LCL_Liste Nouvelle liste identique (avec copies des éléments).
 *
 * \complexite O(n)
 */
LCL_Liste LCL_copier(LCL_Liste liste);

/**
 * \fn LCL_vider
 * \brief Vide entièrement la liste (appel de supprimerElement sur chaque élément).
 *
 * \param pliste  Pointeur sur la liste.
 *
 * \post LCL_estVide(*pliste) == true, LCL_longueur(*pliste) == 0
 * \complexite O(n)
 */
void LCL_vider(LCL_Liste* pliste);

#endif /* __LISTECHAINEELISTE_H__ */
