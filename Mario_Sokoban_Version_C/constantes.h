/*
	constantes.h

	----------------------

	Par Mohamedkamara, pour un exo TP

	Rôle : definit toutes les constantes du programme
*/
#ifndef __CONSTANTE__H__
#define __CONSTANTE__H__
	
	#define TAILLE_BLOC 34 //En pixel
	#define NB_BLOC_HAUTEUR 12
	#define NB_BLOC_LARGEUR 12
	#define HAUTEUR_FENETRE (NB_BLOC_HAUTEUR * TAILLE_BLOC)
	#define LARGEUR_FENETRE (NB_BLOC_LARGEUR * TAILLE_BLOC)

	enum{HAUT, BAS, GAUCHE, DROITE};
	enum {VIDE, MUR, CAISSE, OBJECTIF, MARIO, CAISSE_OK};

#endif