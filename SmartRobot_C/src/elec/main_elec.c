/**
 * @file main_elec.c
 * @brief Programme principal du robot.
 */

#include "gestionRobot.h"
#include "stdio.h"
#include <stdlib.h>
#include <string.h>
#include <pthread.h>
#include "rgb_color.h"
#include <unistd.h>
#include "lcd_display.h"
#include <wiringPi.h>

/**
 * Lit les instructions depuis un flux (ex: stdin) et retourne un tableau dynamique de chaînes.
 * 
 * @param flux : Le flux d'entrée (stdin).
 * @param nb_instructions_out : Pointeur pour retourner le nombre total d'instructions lues.
 * @return Un tableau de chaînes (char**) alloué dynamiquement. 
 *         L'utilisateur DOIT libérer la mémoire (free les chaînes PUIS le tableau).
 */

char** charger_instructions_dynamique(FILE* flux, int* nb_instructions_out) {
    int capacite = 10; // Capacité initiale
    int nb_lues = 0;
    
    char** instructions = malloc(capacite * sizeof(char*));
    if (!instructions) {
        perror("Erreur allocation mémoire");
        exit(EXIT_FAILURE);
    }
    
    char buffer[16];
    
    while (fscanf(flux, "%15s", buffer) == 1) {
        // Agrandissement du tableau si nécessaire
        if (nb_lues >= capacite) {
            capacite *= 2;
            char** temp = realloc(instructions, capacite * sizeof(char*));
            if (!temp) {
                perror("Erreur réallocation mémoire");
                exit(EXIT_FAILURE);
            }
            instructions = temp;
        }
        
        instructions[nb_lues] = strdup(buffer); // strdup alloue et copie
        nb_lues++;
    }
    
    *nb_instructions_out = nb_lues;
    return instructions;
}

/**
 * @brief Fonction principale du programme.
 *
 * Initialise le robot, lance les threads et exécute les instructions.
 *
 * @return Code de sortie.
 */
int main(void) {
	long long debut,fin,duree;
	
	setupPin();
    lcd_display_init();

	debut = (long long)millis();
	int nb_instr = 0;

    pthread_t tid1;
    pthread_create(&tid1, NULL, rgb_color_thread_loop,NULL);

    char** mes_instructions = charger_instructions_dynamique(stdin, &nb_instr);
    
    printf("J'ai recu %d instructions.\n", nb_instr);
    
   
    for(int i=0; i < nb_instr; i++) {
        printf("Instruction %d : %s\n", i, mes_instructions[i]);
        int instr;
        if (strcmp(mes_instructions[i], "AV") == 0) {
            instr = 0;
        } else if (strcmp(mes_instructions[i], "TD") == 0) {
            instr = 2;
        } else if (strcmp(mes_instructions[i], "TG") == 0) {
            instr = 1;
        } else {
            printf("Instruction inconnue: %s\n", mes_instructions[i]);
	    stop();
            continue;
        }

        switch (instr) {
            case 0:
                afficher_LCD(1,"Avancer");
                break;
            case 1:
                afficher_LCD(1,"Gauche");
                break;
            case 2:
                afficher_LCD(1,"Droite");
                break;
            default;
                printf("Instruction invalide");
                break;
        }
        gestionIntersection(instr);
    }

    // Libération de la mémoire
    for(int i=0; i < nb_instr; i++) {
        free(mes_instructions[i]);
    }
    free(mes_instructions);
    
	afficher_LCD(0,"Circuit");

	fin = (long long)millis();
	duree = fin - debut;

	char buffer[17];
	snprintf(buffer, sizeof(buffer), "temps: %f", duree/1000.0);
	afficher_LCD(1,buffer);

	printf("fini boucle %f \n", duree/1000.0);
	stop();

    pthread_join(tid1,NULL);
	return 0;
}
