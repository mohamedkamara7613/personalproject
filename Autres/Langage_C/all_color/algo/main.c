#include <SDL/SDL.h>
#include <stdlib.h>
#include <stdio.h>

#define LARGEUR_FENETRE 255
#define HAUTEUR_FENETRE 255
#define TAILLE_TAB 256

void pause(void);

int main(int argc, char const *argv[])
{
	SDL_Surface *ecran = NULL;
	SDL_Surface *pixel[TAILLE_TAB] = {0};
	SDL_Rect position;
	int rouge = 255, vert = 255, bleu = 255;

	if(SDL_Init(SDL_INIT_VIDEO) == -1)
	{
		fprintf(stderr, "%s\n", SDL_GetError());
		exit(EXIT_FAILURE);
	}
	atexit(SDL_Quit);
	
	ecran = SDL_SetVideoMode(LARGEUR_FENETRE, HAUTEUR_FENETRE, 32, SDL_HWSURFACE | SDL_DOUBLEBUF);
	if(ecran == NULL)
	{
		fprintf(stderr, "%s\n", SDL_GetError());
		exit(EXIT_FAILURE);
	}
	SDL_WM_SetCaption("All Color", NULL);

	for (int i = 0; i < TAILLE_TAB; ++i)
	{
		pixel[i] = SDL_CreateRGBSurface(SDL_HWSURFACE, 10, 1, 32, 0, 0, 0, 0);
		position.y = 0;
		position.x = i;
		//Traitement des couleurs
		rouge--;

		//Coloriage et Blittage de surface 
		SDL_FillRect(pixel[i], NULL, SDL_MapRGB(pixel[i]->format, rouge, vert, bleu));
		SDL_BlitSurface(pixel[i], NULL, ecran, &position);
	}

	for (int i = 0; i < TAILLE_TAB; ++i)
	{
		pixel[i] = SDL_CreateRGBSurface(SDL_HWSURFACE, 10, 1, 32, 0, 0, 0, 0);
		position.y++;
		//Traitement des couleurs
		bleu--;

		//Coloriage et Blittage de surface 
		SDL_FillRect(pixel[i], NULL, SDL_MapRGB(pixel[i]->format, rouge, vert, bleu));
		SDL_BlitSurface(pixel[i], NULL, ecran, &position);
		position.x++;
	}
	/*for (int i = 0; i < TAILLE_TAB; ++i)
	{
		position.y++;
		rouge++;
		bleu--;
				//Coloriage et Blittage de surface 
		SDL_FillRect(pixel[i], NULL, SDL_MapRGB(pixel[i]->format, rouge, vert, bleu));
		SDL_BlitSurface(pixel[i], NULL, ecran, &position);

	}*/

	SDL_Flip(ecran);
	pause();
	for (int i = 0; i < TAILLE_TAB; ++i)
	{
		SDL_FreeSurface(pixel[i]);
		printf("%d", TAILLE_TAB);
	}
	return EXIT_SUCCESS;
}

void pause(void)
{
	int continuer = 1;
	SDL_Event event;

	while(continuer)
	{
		SDL_WaitEvent(&event);
		if(event.type == SDL_QUIT)
			continuer = 0;
	}
}