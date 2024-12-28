/*
	jeu.h

	----------------------

	Par Mohamedkamara, pour un exo TP

	Rôle : definit les prototypes pour la section jeu
*/
#ifndef __JEU__H__
#define __JEU__H__
#include "constantes.h"

	//Declaration de prototype de fonction
		void jouer(SDL_Surface* ecran);
		void deplacerJoueur(int carte[][NB_BLOC_HAUTEUR], SDL_Rect *pos, int direction);
		void deplacerCaisse(int *premierCase, int *secondeCase);

#endif