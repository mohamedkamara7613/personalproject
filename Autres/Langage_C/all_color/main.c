#include <stdlib.h>
#include <stdio.h>
#include <SDL.h>

void pause();

int main(int argc, char const *argv[])
{
//Declaration de variable
	SDL_Surface *ecran = NULL, *lignes[256] = {NULL};
	SDL_Rect position;
	int rouge = 255, bleu = 255, vert = 255;

//Initialisation de la SDL VIDEO
	if (SDL_Init(SDL_INIT_VIDEO) == -1)
	{
		fprintf(stderr, "Impossible de charger la SDL : %s\n", SDL_GetError());
		exit(EXIT_FAILURE);
	}
//Ouverture de fenetre
		ecran = SDL_SetVideoMode(256, 256, 32, SDL_HWSURFACE);
		if (ecran == NULL)
		{
			fprintf(stderr, "Impossible de charger le mode VIDEO : %s\n", SDL_GetError());
			exit(EXIT_FAILURE);
		}
		SDL_WM_SetCaption("Fenetre en degrader", NULL);

//Creation de surface
		//lignes[0] = SDL_CreateRGBSurface(SDL_HWSURFACE, 10, 10, 32, 0, 0, 0, 0);
		//lignes[1] = SDL_CreateRGBSurface(SDL_HWSURFACE, 10, 10, 32, 0, 0, 0, 0);
		position.x = 0; position.y = 0 ;
		for (Uint32 i = 0; i < 256; ++i)
		{
			lignes[i] = SDL_CreateRGBSurface(SDL_HWSURFACE, 1, 10, 32, 0, 0, 0, 0);
		SDL_FillRect(lignes[i], NULL, SDL_MapRGB(ecran->format, rouge, vert, bleu));
			rouge--;
			bleu--;
			SDL_BlitSurface(lignes[i], NULL, ecran, &position);
			position.x = i;
		}
		position.y += 10;
		rouge = 255;
		bleu = 255;
		vert = 255;
				for (Uint32 i = 0; i < 256; ++i)
		{
			lignes[i] = SDL_CreateRGBSurface(SDL_HWSURFACE, 1, 10, 32, 0, 0, 0, 0);
		SDL_Fill   Rect(lignes[i], NULL, SDL_MapRGB(ecran->format, rouge, vert, bleu));
			vert--;
			rouge--;
			
			SDL_BlitSurface(lignes[i], NULL, ecran, &position);
			position.x = i;
		}


		SDL_Flip(ecran);
		pause();
//Liberation de la surface
	for (Uint32 i = 0; i < 256; ++i)
	{
		SDL_FreeSurface(lignes[i]);
	}

		/*SDL_FillRect(lignes[0], NULL, SDL_MapRGB(ecran->format, rouge, vert, bleu));
		position.x = 1; position.y = 0;
		SDL_BlitSurface(lignes[0], NULL, ecran, &position);

		rouge = 0;
		SDL_FillRect(lignes[1], NULL, SDL_MapRGB(ecran->format, rouge, vert, bleu));
		position.x = 11; position.y = 0;
		SDL_BlitSurface(lignes[1], NULL, ecran, &position);

		SDL_FreeSurface(lignes[0]);
		SDL_FreeSurface(lignes[1]);*/
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
