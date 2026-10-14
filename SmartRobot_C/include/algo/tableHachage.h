/**
 * \file tableHachage.h
 * \brief table de hachage utilisant les listes chaînées.
 * \author Nicolas Delestre
 * \version 1.0
 * \date 2025
 *
 */

#ifndef __TABLEHACHAGE_H__
#define __TABLEHACHAGE_H__

#include <stdbool.h>
#include <stddef.h> 
#include "listeChainee.h"
#include "copieLiberationComparaison.h" 


#define TH_TAILLE_TABLE 256

#define TH_MEMOIRE_ERREUR          1
#define TH_CLE_ABSENTE_ERREUR       2  
#define TH_CLE_DEJA_PRESENTE_INFO   3  

/**
 * \struct TH_TableHachage
 * \brief Dictionnaire générique fondé sur un tableau de listes chaînées.
 * \warning les clés sont obligatoires de taille fixe (tailleCle).
 */
typedef struct {
  LC_ListeChainee      table[TH_TAILLE_TABLE]; 
  size_t               tailleCle;              
  CLC_FonctionCopier   copierCle;              
  CLC_FonctionLiberer  libererCle;             
  CLC_FonctionComparer comparerCle;            
  CLC_FonctionCopier   copierValeur;           
  CLC_FonctionLiberer  libererValeur;          
  unsigned int         nbElements;             
} TH_TableHachage;

/**
 * \brief Crée une table de hachage vide.
 *
 * \param copierCle     Fonction de copie des clés (doit allouer un duplicata).
 * \param libererCle    Fonction de libération des clés.
 * \param comparerCle   Fonction de comparaison des clés (<0, 0, >0).
 * \param tailleCle     Taille en octets des clés (utilisée pour le hachage).
 * \param copierValeur  Fonction de copie des valeurs (doit allouer un duplicata).
 * \param libererValeur Fonction de libération des valeurs.
 * \return Une table de hachage initialisée et vide.
 *
 * \pre Toutes les fonctions doivent être non NULL ; \c tailleCle > 0.
 */
TH_TableHachage TH_tableHachage(CLC_FonctionCopier copierCle,
                                CLC_FonctionLiberer libererCle,
                                CLC_FonctionComparer comparerCle,
                                size_t tailleCle,
                                CLC_FonctionCopier copierValeur,
                                CLC_FonctionLiberer libererValeur);

/**
 * \brief Indique si la table de hachage est vide.
 *
 * \param tableHachage La table de hachage examiné.
 * \return \c true si aucun élément n’est stocké, \c false sinon.
 */
bool TH_estVide(TH_TableHachage tableHachage);

/**
 * \brief Renvoie le nombre de paires stockées.
 *
 * \param tableHachage La table de hachage examiné.
 * \return Nombre d’éléments stockés.
 */
unsigned int TH_taille(TH_TableHachage tableHachage);

/**
 * \brief Vérifie si une clé existe dans la table de hachage.
 *
 * \param tableHachage La table de hachage consultée.
 * \param pcle Pointeur vers la clé recherchée (non modifiée).
 * \return \c true si la clé est trouvée, \c false sinon.
 */
bool TH_contient(TH_TableHachage tableHachage, void* pcle);

/**
 * \brief Insère ou met à jour une paire clé/valeur.
 *
 * \param ptableHachage   Pointeur vers la table de hachage à modifier.
 * \param pcle    Pointeur vers la clé à insérer (copiée).
 * \param pvaleur Pointeur vers la valeur à associer (copiée).
 *
 * \post
 *  - Si la clé n’existait pas, une nouvelle paire est ajoutée (\c errno=0).
 *  - Si la clé existait, l’ancienne valeur est libérée puis remplacée
 *    (\c errno=TH_CLE_DEJA_PRESENTE_INFO).
 */
void TH_inserer(TH_TableHachage* ptableHachage, void* pcle, void* pvaleur);

/**
 * \brief Supprime une paire clé/valeur.
 *
 * \param ptableHachage Pointeur vers la table de hachage à modifier.
 * \param pcle  Pointeur vers la clé de la paire à supprimer.
 *
 * \post
 *  - Si la clé existe, elle est supprimée et \c errno=0.
 *  - Si la clé est absente, \c errno=TH_CLE_ABSENTE_ERREUR.
 */
void TH_supprimer(TH_TableHachage* ptableHachage, void* pcle);

/**
 * \brief Retourne une copie de la valeur associée à une clé.
 *
 * \param tableHachage La table de hachage consultée.
 * \param pcle Pointeur vers la clé recherchée.
 * \return
 *  - Une copie de la valeur si la clé est présente (\c errno=0).
 *  - \c NULL si la clé est absente (\c errno=TH_CLE_ABSENTE_ERREUR).
 *
 * \warning L’appelant est responsable de libérer la valeur copiée
 *          avec la fonction \c libererValeur.
 */
void* TH_valeur(TH_TableHachage tableHachage, void* pcle);

/**
 * \brief Retourne une liste contenant toutes les clés de la table de hachage.
 *
 * \param tableHachage La table de hachage consultée.
 * \return Un tableau dynamique de pointeurs sur les clés
 *
 * \note
 *  - Les éléments du tableau sont des COPIES obtenues via \c copierCle.
 *  - L’appelant est responsable de libérer ce tableau dynamique et les clés.
 *  - L’ordre des clés n’est pas garanti (dépend de la table de hachage).
 */
void** TH_cles(TH_TableHachage tableHachage);


/**
 * \brief Vide complètement la table de hachage.
 *
 * \param ptableHachage Pointeur vers la table de hachage à vider.
 *
 * \post Toutes les paires sont supprimées et libérées, \c nbElements=0.
 */
void TH_vider(TH_TableHachage* ptableHachage);

#endif 
