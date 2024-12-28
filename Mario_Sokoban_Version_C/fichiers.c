/*
	fichiers.c

	----------------------

	Par Mohamedkamara, pour un exo TP

	Rôle : pour la gestion des fichiers(chargement et sauvegarde)
*/
#include <stdlib.h>
#include <stdio.h>
#include "fichiers.h"

/*-----------------------------------------------------------------------------------------------------------------------------------*/
int chargerNiveau(int carte[][NB_BLOC_HAUTEUR], int niveau)
{
	FILE *fichier = NULL, *fichier2 = NULL;
	char ligneFichier[NB_BLOC_LARGEUR * NB_BLOC_HAUTEUR + 1] = {0};
	char caracter = 0;
	int i = 0, j = 0, nombreNiveau = 0;

	fichier2 = fopen("stdout.txt", "a+");
	if(fichier2 == NULL)
	{
		fprintf(stderr, "Impossible d'ouvrir le fichier 'stdout.txt'\n");
		exit(EXIT_FAILURE);
	}
	fprintf(fichier2, "Time: %s --------- Date: %s ---------- File: %s --------- Line: %d\n", __TIME__, __DATE__, __FILE__, __LINE__);
	fichier = fopen("niveaux.lvl", "r");
	if (fichier == NULL)
		return 0;
	do
	{
		caracter = fgetc(fichier);
		if(caracter == '\n')
			nombreNiveau++;
	} while (caracter != EOF);

	rewind(fichier);
		while(niveau > 0)
		{
			caracter = fgetc(fichier);
			if(caracter == '\n')
				niveau--;
		}

		fgets(ligneFichier, NB_BLOC_LARGEUR * NB_BLOC_HAUTEUR + 1, fichier);		
		for(i = 0; i < NB_BLOC_LARGEUR; i++)
		{
			for(j = 0; j < NB_BLOC_HAUTEUR; j++)
			{
				switch(ligneFichier[i * NB_BLOC_LARGEUR + j])
				{
					case '0':
						carte[i][j] = 0;
						break;
					case '1':
						carte[i][j] = 1;
						break;
					case '2':
						carte[i][j] = 2;
						break;
					case '3':
						carte[i][j] = 3;
						break;
					case '4':
						carte[i][j] = 4;
						break;
				}
			}
		}
	fclose(fichier);
	fclose(fichier2);
	return 1;
}
/*-----------------------------------------------------------------------------------------------------------------------------------*/
int sauvegarderNiveau(int carte[][NB_BLOC_HAUTEUR])
{
	FILE *fichier = NULL;
	int i = 0, j = 0;

	fichier = fopen("niveaux.lvl", "a+");
	if (fichier == NULL)
		return 0;

	for(i = 0; i < NB_BLOC_HAUTEUR; i++)	
	{
		for(j = 0; j < NB_BLOC_LARGEUR; j++)
		{
			fprintf(fichier, "%d", carte[i][j]);
		}
	}
	fprintf(fichier, "\n");
	fclose(fichier);
	return 1;
}