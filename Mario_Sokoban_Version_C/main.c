/*

	main.c

	--------------

	Par Mohamedkamara, pour un exo TP

	Rôle : programme principale, initie la bibliotheque SDL, affiche le menu et redirige vers la bonne section

*/
#include <SDL/SDL.h>
#include <SDL/SDL_image.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#include "constantes.h"
#include "jeu.h"
#include "editeur.h"

int main(int argc, char const *argv[])
{

//Declaration variable
	FILE *fichier = NULL;
	SDL_Surface *ecran = NULL, *menu = NULL;
	SDL_Rect pos_menu;
	pos_menu.x = 0;
	pos_menu.y = 0;
	int continuer = 1;
	SDL_Event event;

	fichier = fopen("stdout.txt", "a+");
	if(fichier == NULL)
	{
		fprintf(stderr, "Impossible d'ouvrir le fichier 'stdout.txt'\n");
		exit(EXIT_FAILURE);		
	}
	fprintf(fichier, "Time: %s --------- Date: %s ---------- File: %s --------- Line: %d\n", __TIME__, __DATE__, __FILE__, __LINE__);
//Initialisation de la SDL
	if(SDL_Init(SDL_INIT_VIDEO) == -1) 
	{
		fprintf(fichier, "Time: %s --------- Date: %s ---------- File: %s --------- Line: %d\n", __TIME__, __DATE__, __FILE__, __LINE__);
		fprintf(fichier, "Erreur d'initialisation de la SDL : %s\n", SDL_GetError());
		exit(EXIT_FAILURE);
	}
	atexit(SDL_Quit);
		SDL_WM_SetIcon(IMG_Load("src_img/caisse.jpg"), NULL);
		ecran = SDL_SetVideoMode(LARGEUR_FENETRE, HAUTEUR_FENETRE, 32, SDL_HWSURFACE | SDL_DOUBLEBUF);
		if (ecran == NULL)
		{
			fprintf(fichier, "Time: %s --------- Date: %s ---------- File: %s --------- Line: %d\n", __TIME__, __DATE__, __FILE__, __LINE__);
			fprintf(fichier, "Erreur d'initialisation du mode video : %s\n", SDL_GetError());
			exit(EXIT_FAILURE);
		}
		SDL_WM_SetCaption("Mario Sokoban", NULL);

		menu = IMG_Load("src_img/menu.jpg");

//Boucle principale
		while(continuer)
		{
			SDL_WaitEvent(&event);
			switch(event.type)
				{
					case SDL_QUIT: 
						continuer = 0;
						break;
					case SDL_KEYDOWN:
						switch(event.key.keysym.sym)
						{
							case SDLK_ESCAPE:
								continuer = 0;
								break;
							case SDLK_KP1 :
								jouer(ecran);
								SDL_FillRect(ecran, NULL, SDL_MapRGB(ecran->format, 0, 0, 0));
								break;
							case SDLK_KP2:
								edit(ecran);
								SDL_FillRect(ecran, NULL, SDL_MapRGB(ecran->format, 255, 255, 255));
								break;
						}
					break;
				}
			SDL_FillRect(ecran, NULL, SDL_MapRGB(ecran->format, 0, 0, 0));
			SDL_BlitSurface(menu, NULL, ecran, &pos_menu);
			SDL_Flip(ecran);
		}
	SDL_FreeSurface(menu);
	fclose(fichier);
	return EXIT_SUCCESS;
}
