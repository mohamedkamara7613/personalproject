/**
 * \file allocationLiberationComparaison.h
 * \brief Définitions des types de fonctions qui permettent de:
 *  - copier un élément
 *  - supprimer un élément
 *  - comparer deux éléments
 * \author N. Delestre
 * \version 2.0
 * \date 23/11/2015
 *
 */


#ifndef __COPIE_LIBERATION_COMPARAISON__
#define __COPIE_LIBERATION_COMPARAISON__

typedef void* (*CLC_FonctionCopier) (void*);
typedef void (*CLC_FonctionLiberer) (void*);
typedef int (*CLC_FonctionComparer) (void*,void*);
#endif
