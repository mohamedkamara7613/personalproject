/**
 * \file TableHashDictionnaire.h
 * \brief Dictionnaire générique (clé -> valeur) fondé sur hachage et listes chaînées.
 * \author Nicolas Delestre et IA générative
 * \version 1.0
 * \date 2025
 *
 * \section CONCEPTION
 *  - Dictionnaire associant une clé à une valeur (toutes deux génériques, manipulées en \c void*).
 *  - Les éléments sont répartis dans un tableau de 256 listes chaînées.
 *  - La fonction de hachage (interne au .c) calcule un \c unsigned char à partir
 *    de la somme des octets de la clé (\c tailleCle fournie à la création).
 *  - L'égalité des clés est définie par \c comparerCle(k1,k2)==0.
 *  - Gestion mémoire via callbacks fournis par l'utilisateur pour copier/libérer
 *    les clés et les valeurs.
 */

#ifndef __TABLEHASHDICTIONNAIRE_H__
#define __TABLEHASHDICTIONNAIRE_H__

#include <stdbool.h>
#include <stddef.h> 
#include "tableHachage.h"
#include "copieLiberationComparaison.h"
#include "ListeChaineeListe.h"  
 

/**
 * \struct THD_Dictionnaire
 * \brief Dictionnaire générique fondé sur un tableau de listes chaînées.
 * \warning les clés sont obligatoires de taille fixe (tailleCle).
 */
typedef TH_TableHachage THD_Dictionnaire;

/**
 * \brief Crée un dictionnaire vide.
 *
 * \param copierCle     Fonction de copie des clés (doit allouer un duplicata).
 * \param libererCle    Fonction de libération des clés.
 * \param comparerCle   Fonction de comparaison des clés (<0, 0, >0).
 * \param tailleCle     Taille en octets des clés (utilisée pour le hachage).
 * \param copierValeur  Fonction de copie des valeurs (doit allouer un duplicata).
 * \param libererValeur Fonction de libération des valeurs.
 * \return Un dictionnaire initialisé et vide.
 *
 * \pre Toutes les fonctions doivent être non NULL ; \c tailleCle > 0.
 */
THD_Dictionnaire THD_dictionnaire(CLC_FonctionCopier copierCle,
                                CLC_FonctionLiberer libererCle,
                                CLC_FonctionComparer comparerCle,
                                size_t tailleCle,
                                CLC_FonctionCopier copierValeur,
                                CLC_FonctionLiberer libererValeur);

/**
 * \brief Indique si le dictionnaire est vide.
 *
 * \param dico Le dictionnaire examiné.
 * \return \c true si aucun élément n'est stocké, \c false sinon.
 */
bool THD_estVide(THD_Dictionnaire dico);

/**
 * \brief Renvoie le nombre de paires stockées.
 *
 * \param dico Le dictionnaire examiné.
 * \return Nombre d'éléments stockés.
 */
unsigned int THD_taille(THD_Dictionnaire dico);

/**
 * \brief Vérifie si une clé existe dans le dictionnaire.
 *
 * \param dico Le dictionnaire consulté.
 * \param pcle Pointeur vers la clé recherchée (non modifiée).
 * \return \c true si la clé est trouvée, \c false sinon.
 */
bool THD_contient(THD_Dictionnaire dico, void* pcle);

/**
 * \brief Insère ou met à jour une paire clé/valeur.
 *
 * \param pdico   Pointeur vers le dictionnaire à modifier.
 * \param pcle    Pointeur vers la clé à insérer (copiée).
 * \param pvaleur Pointeur vers la valeur à associer (copiée).
 *
 * \post
 *  - Si la clé n'existait pas, une nouvelle paire est ajoutée (\c errno=0).
 *  - Si la clé existait, l'ancienne valeur est libérée puis remplacée
 *    (\c errno=THD_CLE_DEJA_PRESENTE_INFO).
 */
void THD_inserer(THD_Dictionnaire* pdico, void* pcle, void* pvaleur);

/**
 * \brief Supprime une paire clé/valeur.
 *
 * \param pdico Pointeur vers le dictionnaire à modifier.
 * \param pcle  Pointeur vers la clé de la paire à supprimer.
 *
 * \post
 *  - Si la clé existe, elle est supprimée et \c errno=0.
 *  - Si la clé est absente, \c errno=THD_CLE_ABSENTE_ERREUR.
 */
void THD_supprimer(THD_Dictionnaire* pdico, void* pcle);

/**
 * \brief Retourne une copie de la valeur associée à une clé.
 *
 * \param dico Le dictionnaire consulté.
 * \param pcle Pointeur vers la clé recherchée.
 * \return
 *  - Une copie de la valeur si la clé est présente (\c errno=0).
 *  - \c NULL si la clé est absente (\c errno=THD_CLE_ABSENTE_ERREUR).
 *
 * \warning L'appelant est responsable de libérer la valeur copiée
 *          avec la fonction \c libererValeur.
 */
void* THD_valeur(THD_Dictionnaire dico, void* pcle);

/**
 * \brief Retourne une liste contenant toutes les clés du dictionnaire.
 *
 * \param dico Le dictionnaire consulté.
 * \return Une liste (LCL_Liste) contenant une copie de chaque clé présente.
 *
 * \note
 *  - Les éléments de la liste sont des COPIES obtenues via \c copierCle.
 *  - L'appelant est responsable de libérer cette liste (via \c LCL_vider).
 *  - L'ordre des clés n'est pas garanti (dépend de la table de hachage).
 *
 * \complexite O(N) où N est le nombre total d'éléments du dictionnaire.
 */
LCL_Liste THD_cles(THD_Dictionnaire dico);


/**
 * \brief Vide complètement le dictionnaire.
 *
 * \param pdico Pointeur vers le dictionnaire à vider.
 *
 * \post Toutes les paires sont supprimées et libérées, \c nbElements=0.
 */
void THD_vider(THD_Dictionnaire* pdico);

#endif 
