/*
	Creer une fenetre colorier en  degradé noir vers blanc
	il faut creer 255 surfaces de 1 pixel de hauteur de couleurs diffenrentes et de plus en plus noire
*/
#include <stdlib.h>
#include <stdio.h>
#include <SDL.h>

void pause();

int main(int argc, char const *argv[])
{
	SDL_Surface *ecran = NULL, *lignes[256] = {NULL};
	SDL_Rect position;
	
	if (SDL_Init(SDL_INIT_VIDEO) == -1)
	{
		fprintf(stderr, "Impossible de charger la SDL : %s\n", SDL_GetError());
		exit(EXIT_FAILURE);
	}

		ecran = SDL_SetVideoMode(640, 256, 32, SDL_HWSURFACE);
		if (ecran == NULL)
		{
			fprintf(stderr, "Impossible de charger le mode VIDEO : %s\n", SDL_GetError());
			exit(EXIT_FAILURE);
		}
		SDL_WM_SetCaption("Fenetre en degrader", NULL);

		for (Uint32 i = 0; i < 256; ++i)
		{
			lignes[i] = SDL_CreateRGBSurface(SDL_HWSURFACE, 640, 1, 32, 0, 0, 0, 0);
			SDL_FillRect(lignes[i], NULL, SDL_MapRGB(ecran->format, i, i, i));
			
			position.x = 0; position.y = i;		
			SDL_BlitSurface(lignes[i], NULL, ecran, &position);
		}

		
		SDL_Flip(ecran);
		pause();
		for (Uint32 i = 0; i < 256; ++i)
		{
			SDL_FreeSurface(lignes[i]);
		}

	SDL_Quit();
	return EXIT_SUCCESS;
}

/*---------------------------------------------------------------------------------------------------*/
void pause()
{
    int continuer = 1;
    SDL_Event event;
 
    while (continuer)
    {
        SDL_WaitEvent(&event);
        switch(event.type)
        {
            case SDL_QUIT:
                continuer = 0;
        }
    }
}
