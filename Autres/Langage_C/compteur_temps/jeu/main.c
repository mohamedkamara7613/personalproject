#include <SDL/SDL.h>
#include <SDL/SDL_image.h>
#include <SDL/SDL_ttf.h>
#include <stdlib.h>
#include <stdio.h>
#include "constante.h"

int main(int argc, char const *argv[])
{
	SDL_Surface *ecran = NULL, *texte = NULL, *texte2 = NULL;
	SDL_Event event; 
	SDL_Rect position;
	SDL_Color couleurNoire = {0, 0, 0, 0}, couleurBlanche = {255, 255, 255, 0};
	TTF_Font *police = NULL;
	FILE *fichier = NULL;
	Bool continuer = true, fini = true;
	signed char compteur[20], fin[50];
	int tempsActuel = 0, tempsPrecedent = 0, tempsAproximatif = 5000, nombreClic = 0;

//Ouverture du fichier d'erreur
	fichier = fopen("stdout.err", "a+");
	if(fichier == NULL)
	{
		fprintf(stdout, "Impossible d'ouvrir le fichier 'stdout.err'\n");
		exit(EXIT_FAILURE);
	}
//Initialisation de la TTF
	if(TTF_Init() == -1)
	{
		fprintf(fichier, "Erreur  d'initialisation de la TTF: %s\n", TTF_GetError());
		exit(EXIT_FAILURE);
	}
//Initialisation et fermiture de la SDL 
	if (SDL_Init(SDL_INIT_VIDEO | SDL_INIT_TIMER) == -1)
	{
		fprintf(fichier, "Erreur d'initialisation de la SDL : %s\n", SDL_GetError());
		exit(EXIT_FAILURE);
	}
	atexit(SDL_Quit);

//Ouverture d'une fenetre
	ecran = SDL_SetVideoMode(680, 480, 32, SDL_HWSURFACE | SDL_DOUBLEBUF);
	if(ecran == NULL)
	{
		fprintf(fichier, "Erreur d'initialisation de la video Mode: %s\n", SDL_GetError());
	}
	SDL_WM_SetCaption("Compteur de temps", NULL);

//Chargement de la police et ecriture a la surface
	police = TTF_OpenFont("angelina.ttf", 65);
	if(police == NULL)
	{
		fprintf(fichier, "Erreur de chargement de la police\n");
		exit(EXIT_FAILURE);
	}
//Initialisation du temps et du texte
	tempsActuel = SDL_GetTicks();
	sprintf(compteur, "Temps : %d ms", tempsAproximatif);
	texte = TTF_RenderText_Shaded(police, compteur, couleurNoire, couleurBlanche);

	//Boucle principale
	while(continuer)
		{
			SDL_WaitEvent(&event);
			switch(event.type)
			{
				case SDL_KEYDOWN:
					continuer = false;
					break;
			}
			texte2 = TTF_RenderText_Shaded(police, "maximum de clic en 5s", couleurNoire, couleurBlanche);
			SDL_FillRect(ecran, NULL, SDL_MapRGB(ecran->format, 255, 255, 255));
			position.x = ecran->w / 2 - texte->w / 2; position.y = ecran->h / 2 - texte->h / 2;
			SDL_BlitSurface(texte2, NULL, ecran, &position);
			SDL_Flip(ecran);
		}
		continuer = true;
	while(continuer)
		{
			SDL_PollEvent(&event);
			switch(event.type)
			{
				case SDL_QUIT:
					continuer = false;
					break;
				case SDL_MOUSEBUTTONDOWN:
					nombreClic++;
					printf("clic\n");
					break;
			}
			if(tempsAproximatif == 0)
				continuer = false;
		//Effacement de l'ecran
			SDL_FillRect(ecran, NULL, SDL_MapRGB(ecran->format, 255, 255, 255));
		//compteur
			tempsActuel = SDL_GetTicks();
			if(tempsActuel - tempsPrecedent >= 100)
			{
				tempsAproximatif -= 100;//On ajoute 100ms au compteur 
				sprintf(compteur, "Temps : %d ms", tempsAproximatif);
				SDL_FreeSurface(texte);
				//Ecriture du temps a la surface
				texte = TTF_RenderText_Shaded(police, compteur, couleurNoire, couleurBlanche);
				tempsPrecedent = tempsActuel;
			}
			else
				SDL_Delay(100 - (tempsActuel - tempsPrecedent));
		//Blittage du texte a l'ecran
			SDL_BlitSurface(texte, NULL, ecran, &position);

		//Mise a jour de la surface
			SDL_Flip(ecran);
		}
		continuer = true;
	while(continuer)
		{
			SDL_WaitEvent(&event);
			switch(event.type)
			{
				case SDL_QUIT:
					continuer = false;
				case SDL_KEYDOWN:
					continuer = false;
					break;
			}
		//Effacement de l'ecran
			SDL_FillRect(ecran, NULL, SDL_MapRGB(ecran->format, 255, 255, 255));
			sprintf(fin, "Vous avez fait %d clics", nombreClic);
			//Ecriture du temps a la surface
			texte = TTF_RenderText_Shaded(police, fin, couleurNoire, couleurBlanche);
			SDL_BlitSurface(texte, NULL, ecran, &position);
			SDL_Flip(ecran);
		}

//Liberation de la memoire
	fclose(fichier);
	SDL_FreeSurface(texte);
	TTF_CloseFont(police);
	TTF_Quit();
	return EXIT_SUCCESS;
}