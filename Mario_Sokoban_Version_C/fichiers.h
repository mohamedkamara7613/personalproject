/*
	fichiers.h

	----------------------

	Par Mohamedkamara, pour un exo TP

	Rôle : definit les prototypes pour la gestion des fichiers(chargement et sauvegarde)
*/
#ifndef __FICHIERS__H__
#define __FICHIERS__H__
#include "constantes.h"

	//Declaration de prototype de fonction
	int chargerNiveau(int carte[][NB_BLOC_HAUTEUR], int niveau);
	int sauvegarderNiveau(int carte[][NB_BLOC_HAUTEUR]);

#endif