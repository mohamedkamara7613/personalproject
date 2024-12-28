/*
	editeur.c

	----------------------

	Par Mohamedkamara, pour un exo TP

	Rôle : gere toutes les fonctions de l'editeur
*/
#include <SDL/SDL.h>
#include <SDL/SDL_image.h>
#include <stdlib.h>
#include <stdio.h>

#include "editeur.h"
#include "fichiers.h"

/*-----------------------------------------------------------------------------------------------------------------------------------*/
void edit(SDL_Surface *ecran)
{
//Declaration des variable
	SDL_Surface *objectActuelle[4] = {0};
	SDL_Surface *mur = NULL, *caisse = NULL, *objectif = NULL, *mario = NULL, *instructions = NULL;
	SDL_Rect position, pos_Actuel, pos_instructions, pos_mario;
	SDL_Event event;
	FILE *fichier = NULL;
	pos_instructions.x = 0; pos_instructions.y = 0;

	int continuer = 1, clicGaucheEnCours = 0, clicDroiteEnCours = 0, marioBlitter = 0, marioTest = 0;
	int objectActuel = MUR, i = 0, j = 0;
	int carte[NB_BLOC_LARGEUR][NB_BLOC_HAUTEUR] = {0}, niveau = 1;

	//Chargement des srites
	mur = IMG_Load("src_img/mur.jpg");
	caisse = IMG_Load("src_img/caisse.jpg");
	objectif = IMG_Load("src_img/objectif.png");
	mario = IMG_Load("src_img/mario_bas.gif");
	instructions = IMG_Load("src_img/instructions.jpg");
	objectActuelle[0] = IMG_Load("src_img/mur.jpg");
	objectActuelle[1] = IMG_Load("src_img/caisse.jpg");
	objectActuelle[2] = IMG_Load("src_img/objectif.png");
	objectActuelle[3] = IMG_Load("src_img/mario_bas.gif");

//Ouverture du fichier journal
	fichier = fopen("stdout.txt", "a+");
	if (fichier == NULL)
	{
		fprintf(stderr, "Impossible d'ouvrir le fichier 'stdout.txt'\n");
		exit(EXIT_FAILURE);
	}
	fprintf(fichier, "Time: %s --------- Date: %s ---------- File: %s --------- Line: %d\n", __TIME__, __DATE__, __FILE__, __LINE__);

	//Chargement de la carte
	if (!chargerNiveau(carte, niveau))
	{
		fprintf(fichier, "Time: %s --------- Date: %s ---------- File: %s --------- Line: %d\n", __TIME__, __DATE__, __FILE__, __LINE__);
		fprintf(fichier, "Impossible de charger le niveau : cause possible le fichier 'niveaux.lvl' n'existe pas.\n");
		exit(EXIT_FAILURE);
	}
//Affichage des instructions de l'editeur
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
	//Recherche et la sauvegarde de mario
	for(i = 0; i < NB_BLOC_LARGEUR; i++)
	{
		for(j = 0; j < NB_BLOC_HAUTEUR; j++)
		{
			if(carte[i][j] == MARIO)
			{
				pos_mario.x = i * TAILLE_BLOC;
				pos_mario.y = j * TAILLE_BLOC;
				marioBlitter = 1;
			}
		}
	}

//Boucle principale
	continuer = 1;
	while(continuer)
	{
		SDL_WaitEvent(&event);
		switch(event.type)
		{
			case SDL_QUIT:
				continuer = 0;
				break;
			case SDL_MOUSEBUTTONDOWN:
				if (event.button.button == SDL_BUTTON_LEFT)
				{
					//On met l'objet choisi (mur, caisse...) a l'endroit du clic
					carte[event.button.x / TAILLE_BLOC][event.button.y / TAILLE_BLOC] = objectActuel;
					/*if(event.button.x / TAILLE_BLOC][event.button.y / TAILLE_BLOC] != MARIO)
					{
							switch(carte[event.button.x / TAILLE_BLOC][event.button.y / TAILLE_BLOC])
							{
								case CAISSE:
									SDL_BlitSurface()
							}
					}*/
					if(objectActuel == MARIO)
					{
						pos_mario.x = (event.button.x / TAILLE_BLOC) * TAILLE_BLOC;
						pos_mario.y = (event.button.y / TAILLE_BLOC) * TAILLE_BLOC;
						marioBlitter = 1;
					}
					/*if(objectActuel == MARIO && marioBlitter == 1)
					{
						pos_mario.x = pos_mario.x;
						pos_mario.y = pos_mario.y;
					}
					else
					{
						pos_mario.x = (event.button.x / TAILLE_BLOC) * TAILLE_BLOC;
						pos_mario.y = (event.button.y / TAILLE_BLOC) * TAILLE_BLOC;
					}*/
					clicGaucheEnCours = 1;
				}
				else if(event.button.button == SDL_BUTTON_RIGHT)
				{
					if(carte[event.button.x / TAILLE_BLOC][event.button.y / TAILLE_BLOC] == MARIO)
						{
							pos_mario.x = 0;
							pos_mario.y = 0;
							marioBlitter = 0;
						}

					carte[event.button.x / TAILLE_BLOC][event.button.y / TAILLE_BLOC] = VIDE;
					clicDroiteEnCours = 1;
				}

			break;
			case SDL_MOUSEMOTION:
				if(clicGaucheEnCours)
				{
					carte[event.motion.x / TAILLE_BLOC][event.motion.y / TAILLE_BLOC] = objectActuel;
				}
				if(clicDroiteEnCours)
				{
					carte[event.motion.x / TAILLE_BLOC][event.motion.y / TAILLE_BLOC] = VIDE;
				}
				pos_Actuel.x = event.motion.x;
				pos_Actuel.y = event.motion.y;
			break;
			case SDL_MOUSEBUTTONUP:
				if(event.button.button == SDL_BUTTON_LEFT)
					clicGaucheEnCours = 0;
				if(event.button.button == SDL_BUTTON_RIGHT)
					clicDroiteEnCours = 0;
			break;
			case SDL_KEYDOWN:
				switch(event.key.keysym.sym)
				{
					case SDLK_ESCAPE:
						continuer = 0;
						break;
					case SDLK_s:
						sauvegarderNiveau(carte);
						break;
					case SDLK_KP1:
						objectActuel = MUR;
						marioTest = 0;
						break;
					case SDLK_KP2:
						objectActuel = CAISSE;
						marioTest = 0;
						break;
					case SDLK_KP3:
						objectActuel = OBJECTIF;
						marioTest = 0;
						break;
					case SDLK_KP4:
						marioTest = 1;
						/*//Recherche de la position de mario sur la carte
							for (i = 0; i < NB_BLOC_LARGEUR; i++)
							{
								for (j = 0; j < NB_BLOC_HAUTEUR; j++)
								{
									if (carte[i][j] == MARIO)//Si mario se trouve a cette position
									{
										position.x = i * TAILLE_BLOC;
										position.y = j * TAILLE_BLOC;
										pos_test.x = position.x; pos_test.y = position.y;
										//marioBlitter = 1;
									}
									//else
									//	marioBlitter = 0;
								}
							}*/
							//if (marioBlitter == 0)
							//{
								objectActuel = MARIO;
							//}
							//else
							//	objectActuel = OBJECTIF;
							break;
				}
		}

		SDL_FillRect(ecran, NULL, SDL_MapRGB(ecran->format, 255, 255, 255));

		//Placement des objets a l'ecran
		for(i = 0; i < NB_BLOC_LARGEUR; i++)
		{
			for(j = 0; j < NB_BLOC_HAUTEUR; j++)
			{
				position.x = i * TAILLE_BLOC;
				position.y = j * TAILLE_BLOC;

				switch(carte[i][j])
				{
					case MARIO:
						if(marioBlitter == 1)
							SDL_BlitSurface(mario, NULL, ecran, &pos_mario);
						break;
					case MUR:
						SDL_BlitSurface(mur, NULL, ecran, &position);
						break;
					case CAISSE:
						SDL_BlitSurface(caisse, NULL, ecran, &position);
						break;
					case OBJECTIF:
						SDL_BlitSurface(objectif, NULL, ecran, &position);
						break;
				}
			}
		}

//Affichage constant de l'object selectionné
		if(objectActuel == MUR)
			SDL_BlitSurface(objectActuelle[0], NULL, ecran, &pos_Actuel);
		else if(objectActuel == CAISSE)
			SDL_BlitSurface(objectActuelle[1], NULL, ecran, &pos_Actuel);
		else if(objectActuel == OBJECTIF)
			SDL_BlitSurface(objectActuelle[2], NULL, ecran, &pos_Actuel);
		else if(marioTest == 1)
			SDL_BlitSurface(objectActuelle[3], NULL, ecran, &pos_Actuel);

		//Mise a jour de l'ecran
		SDL_Flip(ecran);
	}

//Liberation de la memoire
	SDL_FreeSurface(mur);
	SDL_FreeSurface(caisse);
	SDL_FreeSurface(objectif);
	SDL_FreeSurface(mario);
	SDL_FreeSurface(instructions);
	for (i = 0; i < 4; i++)
		SDL_FreeSurface(objectActuelle[i]);
	fclose(fichier);
}
