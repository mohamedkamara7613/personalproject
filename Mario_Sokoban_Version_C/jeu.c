/*
	jeu.c

	----------------------

	Par Mohamedkamara, pour un exo TP

	Rôle : gere une partie de jeu complete
*/
#include <SDL/SDL.h>
#include <SDL/SDL_image.h>
#include <stdlib.h>
#include <stdio.h>

#include "jeu.h"
#include "fichiers.h"

/*-----------------------------------------------------------------------------------------------------------------------------------*/
void jouer(SDL_Surface* ecran)
{
//Declaration des variables
	SDL_Surface *mario[4] = {NULL}; //4 surfaces pour 4 directions de mario
	SDL_Surface *mur = NULL, *caisse = NULL, *caisse_ok = NULL, *objectif = NULL, *instructions = NULL, *marioActuel = NULL, *bravo = NULL;//marioActuel pointe vers une case du tableu de mario
	SDL_Rect position, positionJoueur, pos_instructions, pos_bravo;
	SDL_Event event;
	
	FILE *fichier = NULL;
	fichier = fopen("stdout.txt", "a+");
	if(fichier == NULL)
	{
		fprintf(stderr, "Impossible d'ouvrir le fichier 'stdout.txt'\n");
		exit(EXIT_FAILURE);
	}
	fprintf(fichier, "Time: %s --------- Date: %s ---------- File: %s --------- Line: %d\n", __TIME__, __DATE__, __FILE__, __LINE__);
	int continuer = 1, objectifsRestants = 0, i = 0, j= 0, continu = 1;
	int carte[NB_BLOC_LARGEUR][NB_BLOC_HAUTEUR] = {0}, niveau = 0; 
	pos_instructions.x = 0; pos_instructions.y = 0;

//Chargement des sprites(image, personnage...)
	mur = IMG_Load("src_img/mur.jpg");
	caisse = IMG_Load("src_img/caisse.jpg");
	caisse_ok = IMG_Load("src_img/caisse_ok.jpg");
	objectif = IMG_Load("src_img/objectif.png");
	instructions = IMG_Load("src_img/instructions_jeu.jpg");
	bravo = IMG_Load("src_img/bravo.jpg");
	mario[BAS] = IMG_Load("src_img/mario_bas.gif");
	mario[HAUT] = IMG_Load("src_img/mario_haut.gif");
	mario[GAUCHE] = IMG_Load("src_img/mario_gauche.gif");
	mario[DROITE] = IMG_Load("src_img/mario_droite.gif");

//Orientation initiale de mario
	marioActuel = mario[BAS];

//Chargement du niveau
	if (!chargerNiveau(carte, niveau))
	{
		fprintf(fichier, "Time: %s --------- Date: %s ---------- File: %s --------- Line: %d\n", __TIME__, __DATE__, __FILE__, __LINE__);
		fprintf(fichier, "Impossible de charger le niveau : cause possible le fichier 'niveaux.lvl' n'existe pas.\n");
		exit(EXIT_FAILURE);
	}

//Recherche de la position de mario sur la carte
	for (i = 0; i < NB_BLOC_LARGEUR; i++)
	{
		for (j = 0; j < NB_BLOC_HAUTEUR; j++)
		{
			if (carte[i][j] == MARIO)//Si mario se trouve a cette position
			{
				positionJoueur.x = i;
				positionJoueur.y = j;
				carte[i][j] = VIDE;
			}
		}
	}

//Activation de la repetiton des touches
	SDL_EnableKeyRepeat(100, 100);
//Affichage des instructions
	while(continuer)
	{
		SDL_WaitEvent(&event);
		switch(event.type)
		{
			case SDL_KEYDOWN:
				continuer = 0;
		}
		SDL_FillRect(ecran, NULL, SDL_MapRGB(ecran->format, 255, 255, 255));
		SDL_BlitSurface(instructions, NULL, ecran, &pos_instructions);
		SDL_Flip(ecran);
	}

//Boucle principale
	continuer = 1;
	while(continuer)
	{
		SDL_WaitEvent(&event);
		switch(event.type)
		{
			case SDL_QUIT :
				continuer = 0;
				break;
			case SDL_KEYDOWN:
				switch(event.key.keysym.sym)
				{
					case SDLK_ESCAPE:
						continuer = 0;
						break;
					case SDLK_r:
						if (!chargerNiveau(carte, niveau))
						{
							fprintf(fichier, "Time: %s --------- Date: %s ---------- File: %s --------- Line: %d\n", __TIME__, __DATE__, __FILE__, __LINE__);
							fprintf(fichier, "Impossible de charger le niveau : cause possible le fichier 'niveaux.lvl' n'existe pas.\n");
							exit(EXIT_FAILURE);
						}
						for (i = 0; i < NB_BLOC_LARGEUR; i++)
						{
							for (j = 0; j < NB_BLOC_HAUTEUR; j++)
							{
								if (carte[i][j] == MARIO)//Si mario se trouve a cette position
								{
									positionJoueur.x = i;
									positionJoueur.y = j;
									carte[i][j] = VIDE;
								}
							}
						}
						marioActuel = mario[BAS];
						break;
					case SDLK_UP:
						marioActuel = mario[HAUT];
						deplacerJoueur(carte, &positionJoueur, HAUT);
						break;
					case SDLK_DOWN:
						marioActuel = mario[BAS];
						deplacerJoueur(carte, &positionJoueur, BAS);
						break;
					case SDLK_RIGHT:
						marioActuel = mario[DROITE];
						deplacerJoueur(carte, &positionJoueur, DROITE);
						break;
					case SDLK_LEFT:
						marioActuel = mario[GAUCHE];
						deplacerJoueur(carte, &positionJoueur, GAUCHE);
						break;
				}
				break;
		}
		//Effacement de l'ecrant en coloriant en blanc
		SDL_FillRect(ecran, NULL, SDL_MapRGB(ecran->format, 255, 255, 255));

		//Placement des objets a l'ecran
		objectifsRestants = 0;
		
		for (i = 0; i < NB_BLOC_LARGEUR; i++)
		{
			for(j = 0; j < NB_BLOC_HAUTEUR; j++)
			{
				position.x = i * TAILLE_BLOC;
				position.y = j * TAILLE_BLOC;

				switch(carte[i][j])
				{
					case MUR:
						SDL_BlitSurface(mur, NULL, ecran, &position);
						break;
					case CAISSE:
						SDL_BlitSurface(caisse, NULL, ecran, &position);
						break;
					case CAISSE_OK:
						SDL_BlitSurface(caisse_ok, NULL, ecran, &position);
						break;
					case OBJECTIF:
						SDL_BlitSurface(objectif, NULL, ecran, &position);
						objectifsRestants = 1;
						break;
				}

			}
		}

		//Si on a trouvé aucun objectif sur la carte sa veut dire qu"on a gagné
		if(!objectifsRestants)
			{
			//Chargement du niveau
				niveau++;
				if (!chargerNiveau(carte, niveau))
				{
					fprintf(fichier, "Time: %s --------- Date: %s ---------- File: %s --------- Line: %d\n", __TIME__, __DATE__, __FILE__, __LINE__);
					fprintf(fichier, "Impossible de charger le niveau : cause possible le fichier 'niveaux.lvl' n'existe pas.\n");
					exit(EXIT_FAILURE);
				}
				for (i = 0; i < NB_BLOC_LARGEUR; i++)
				{
					for (j = 0; j < NB_BLOC_HAUTEUR; j++)
					{
						if (carte[i][j] == MARIO)//Si mario se trouve a cette position
						{
							positionJoueur.x = i;
							positionJoueur.y = j;
							carte[i][j] = VIDE;
						}
					}
				}
				marioActuel = mario[BAS];
				//Affichage de bravo
					pos_bravo.x = (ecran->w / 2) - (bravo->w / 2);
					pos_bravo.y = (ecran->h / 2) - (bravo->h / 2);
				while(continu)
				{
					SDL_WaitEvent(&event);
					switch(event.type)
					{
						case SDL_KEYDOWN:
							continu = 0;
					}
					//SDL_FillRect(ecran, NULL, SDL_MapRGB(ecran->format, 255, 255, 255));
					SDL_BlitSurface(bravo, NULL, ecran, &pos_bravo);
					SDL_Flip(ecran);
				}
				continu = 1;
			}

		//On place le joueur a la bonne position
		position.x = positionJoueur.x * TAILLE_BLOC;
		position.y = positionJoueur.y * TAILLE_BLOC;
		SDL_BlitSurface(marioActuel, NULL, ecran, &position);

		//Mise a jour de l'ecran 
		SDL_Flip(ecran);
	}

//Desactivation de la repetiton des touches
	SDL_EnableKeyRepeat(0, 0);

//Liberation de surface
	SDL_FreeSurface(mur);
	SDL_FreeSurface(caisse);
	SDL_FreeSurface(caisse_ok);
	SDL_FreeSurface(instructions);
	SDL_FreeSurface(objectif);
	for (i = 0; i < 4; ++i)
		SDL_FreeSurface(mario[i]);
	fclose(fichier);
}

/*-----------------------------------------------------------------------------------------------------------------------------------*/
void deplacerJoueur(int carte[][NB_BLOC_HAUTEUR], SDL_Rect *pos, int direction)
{
	switch(direction)
	{
		case HAUT:
		//Verification si le joueur a le droit de se deplacer ou de deplacer une caisse
			if(pos->y - 1 < 0)//Si le joueur se trouve au bord de la fenetre
				break;

			if (carte[pos->x][pos->y - 1] == MUR)//S'il y a un mur on arrete
				break;

			//Si on veut pousser une caisse il faut verifier qu'il y a pas un mur derriere ou une autre caisse ou le bord de la fenetre
			if((carte[pos->x][pos->y - 1] == CAISSE_OK || carte[pos->x][pos->y - 1] == CAISSE) && (pos->y - 2 < 0 || carte[pos->x][pos->y - 2] == MUR || carte[pos->x][pos->y - 2] == CAISSE || carte[pos->x][pos->y - 2] == CAISSE_OK))
				break;

			//SI on arrive là c'est qu'on peut deplacer le joueur
			//On verifie d'abord s'il y a pas de caisse a deplacer
			deplacerCaisse(&carte[pos->x][pos->y - 1], &carte[pos->x][pos->y - 2]);

			//On peut enfin faire monter le joueur Ouff !!
			pos->y--;
			break;

		case BAS:
			//Verification si le joueur a le droit de se deplacer ou de deplacer une caisse
			if(pos->y + 1 >= NB_BLOC_HAUTEUR)//Si le joueur se trouve au bord de la fenetre
				break;

			if (carte[pos->x][pos->y + 1] == MUR)//S'il y a un mur on arrete
				break;

			//Si on veut pousser une caisse il faut verifier qu'il y a pas un mur derriere ou une autre caisse ou le bord de la fenetre
			if((carte[pos->x][pos->y + 1] == CAISSE_OK || carte[pos->x][pos->y + 1] == CAISSE) && (pos->y + 2 >= NB_BLOC_HAUTEUR || carte[pos->x][pos->y + 2] == MUR || carte[pos->x][pos->y + 2] == CAISSE || carte[pos->x][pos->y + 2] == CAISSE_OK))
				break;

			//SI on arrive là c'est qu'on peut deplacer le joueur
			//On verifie d'abord s'il y a pas de caisse a deplacer
			deplacerCaisse(&carte[pos->x][pos->y + 1], &carte[pos->x][pos->y + 2]);

			//On peut enfin faire monter le joueur Ouff !!
			pos->y++;
			break;
		case GAUCHE:
		//Verification si le joueur a le droit de se deplacer ou de deplacer une caisse
			if(pos->x - 1 < 0)//Si le joueur se trouve au bord de la fenetre
				break;

			if (carte[pos->x - 1][pos->y] == MUR)//S'il y a un mur on arrete
				break;

			//Si on veut pousser une caisse il faut verifier qu'il y a pas un mur derriere ou une autre caisse ou le bord de la fenetre
			if((carte[pos->x- 1][pos->y] == CAISSE_OK || carte[pos->x - 1][pos->y] == CAISSE) && (pos->x - 2 < 0 || carte[pos->x - 2][pos->y] == MUR || carte[pos->x - 2][pos->y] == CAISSE || carte[pos->x - 2][pos->y] == CAISSE_OK))
				break;

			//SI on arrive là c'est qu'on peut deplacer le joueur
			//On verifie d'abord s'il y a pas de caisse a deplacer
			deplacerCaisse(&carte[pos->x - 1][pos->y], &carte[pos->x - 2][pos->y]);

			//On peut enfin faire monter le joueur Ouff !!
			pos->x--;
			break;
		case DROITE:
		//Verification si le joueur a le droit de se deplacer ou de deplacer une caisse
			if(pos->x + 1 >= NB_BLOC_LARGEUR)//Si le joueur se trouve au bord de la fenetre
				break;

			if (carte[pos->x + 1][pos->y] == MUR)//S'il y a un mur on arrete
				break;

			//Si on veut pousser une caisse il faut verifier qu'il y a pas un mur derriere ou une autre caisse ou le bord de la fenetre
			if((carte[pos->x + 1][pos->y] == CAISSE_OK || carte[pos->x + 1][pos->y] == CAISSE) && (pos->x + 2 >= NB_BLOC_LARGEUR|| carte[pos->x + 2][pos->y] == MUR || carte[pos->x + 2][pos->y] == CAISSE || carte[pos->x + 2][pos->y] == CAISSE_OK))
				break;

			//SI on arrive là c'est qu'on peut deplacer le joueur
			//On verifie d'abord s'il y a pas de caisse a deplacer
			deplacerCaisse(&carte[pos->x + 1][pos->y], &carte[pos->x + 2][pos->y]);

			//On peut enfin faire monter le joueur Ouff !!
			pos->x++;
			break;
	}
}

/*----------------------------------------------------------------------------------------------------------------------------------*/
void deplacerCaisse(int *premierCase, int *secondeCase)
{
	if (*premierCase == CAISSE || *premierCase == CAISSE_OK)
	{
		if(*secondeCase == OBJECTIF)
			*secondeCase = CAISSE_OK;
		else
			*secondeCase = CAISSE;

		if(*premierCase == CAISSE_OK) 
			*premierCase = OBJECTIF;
		else 
			*premierCase = VIDE;
	}
}