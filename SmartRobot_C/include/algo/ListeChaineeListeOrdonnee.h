/**
 * \file ListeChaineeListeOrdonnee.h
 * \brief Liste générique ordonnée basée sur liste chaînée (insertion triée).
 * \author Nicolas Delestre et IA générative
 * \version 1.0
 * \date 2025
 **/

#ifndef __LISTECHAINEELISTEORDONNEE_H__
#define __LISTECHAINEELISTEORDONNEE_H__

#include <stdbool.h>
#include "listeChainee.h"
#include "copieLiberationComparaison.h"

/* Codes d'erreur proposés pour rester homogène avec les autres modules */
#define LCLO_LISTE_VIDE_ERREUR 3
#define LCLO_POSITION_TROP_GRANDE_ERREUR 4

/**
 * \struct LCLO_ListeOrdonnee
 * \brief Liste ordonnée générique avec suivi O(1) de la longueur.
 *
 * \invariant
 *   Pour toute paire de oeuds successifs a->b, on a comparerElements(a,b) <= 0.
 */
typedef struct {
  LC_ListeChainee liste;                 /**< Tête de liste */
  CLC_FonctionCopier copierElement;      /**< Fonction de copie des éléments */
  CLC_FonctionLiberer supprimerElement;  /**< Fonction de libération des éléments */
  CLC_FonctionComparer comparer;         /**< Comparateur: <0, =0, >0 */
  unsigned int longueur;                 /**< Taille courante de la liste */
} LCLO_ListeOrdonnee;


/**
 * \brief Construit une liste ordonnée vide avec ses fonctions de gestion.
 *
 * \param copierElement     Fonction qui **duplique** un élément (copie profonde).
 * \param supprimerElement  Fonction qui **libère** un élément.
 * \param comparerElements  Fonction de comparaison : <0 si a<b, 0 si a==b, >0 si a>b.
 * \return LCLO_ListeOrdonnee  Une liste vide prête à l'emploi.
 *
 * \post LCLO_estVide(retour) == true, LCLO_longueur(retour) == 0
 * \complexite O(1)
 */
LCLO_ListeOrdonnee LCLO_listeOrdonnee(CLC_FonctionCopier copierElement,
                                      CLC_FonctionLiberer supprimerElement,
                                      CLC_FonctionComparer comparerElement);

/**
 * \brief Indique si la liste est vide.
 * \param liste  Liste considérée.
 * \return bool  true ssi longueur == 0.
 * \complexite O(1)
 */
bool LCLO_estVide(LCLO_ListeOrdonnee liste);

/**
 * \brief Insère une **copie** de l'élément en respectant l'ordre croissant.
 *
 * L'élément est inséré **après** tous les éléments `<=` lui, et **avant**
 * le premier élément strictement `>` (doublons autorisés).
 *
 * \param pliste   Pointeur sur la liste.
 * \param pelement  Pointeur sur l'élément à copier (jamais stocké tel quel).
 *
 * \post LCLO_longueur(*pliste) est incrémentée de 1 si succès ; l'invariant d'ordre
 *       est maintenu.
 * \complexite O(n) (liste chaînée simple).
 */
void LCLO_inserer(LCLO_ListeOrdonnee* pliste, void* pelement);

/**
 * \brief Supprime l'élément à la position donnée (1..longueur).
 *
 * \param pliste    Pointeur sur la liste.
 * \param position  Entier 0..longueur-1.
 *
 * \pre pliste != NULL ; 0 <= position < LCLO_longueur(*pliste)
 * \post LCLO_longueur(*pliste) est décrémentée de 1 si succès.
 * \complexite O(n)
 */
void LCLO_supprimer(LCLO_ListeOrdonnee* pliste, unsigned int position);


/**
 * \brief Renvoie une **COPIE** de l'élément situé à la position demandée.
 *
 * \param liste     Liste source (non modifiée).
 * \param position  Entier 0..longueur-1.
 * \return void*    Copie de l'élément (à **libérer par l'appelant** avec la
 *                  fonction adaptée), ou `NULL` si erreur.
 *
 * \remarques
 *   - Sémantique de **copie** : l'objet retourné est indépendant de celui stocké
 *     dans la liste. L'appelant en devient propriétaire.
 * \complexite O(n)
 */
void* LCLO_element(LCLO_ListeOrdonnee liste, unsigned int position);

/**
 * \brief Longueur de la liste.
 * \param liste  Liste considérée.
 * \return int   Nombre d'éléments (>= 0).
 * \complexite O(1)
 */
int LCLO_longueur(LCLO_ListeOrdonnee liste);

/**
 * \brief Vide entièrement la liste (appel de `supprimerElement` sur chaque élément).
 *
 * \param pliste  Pointeur sur la liste.
 * \post LCLO_estVide(*pliste) == true, LCLO_longueur(*pliste) == 0.
 * \complexite O(n)
 */
void LCLO_vider(LCLO_ListeOrdonnee* pliste);

#endif
