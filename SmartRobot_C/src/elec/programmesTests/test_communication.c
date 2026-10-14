#include <stdio.h>
#include <unistd.h>
#include <string.h>

// CECI EST UN FICHIER TEST POUR LA COMMMUNICATION AVEC LE ROBOT

// depuis la racine il faut compiler comme ça : gcc -o bin/test_comm src/test_communication.c src/elec/*.c -Iinclude -Iinclude/elec -lwiringPi -lwiringPiDev
#include "elec/deplacementRobot.h"
#include "elec/setup.h"

#define DELAY_US 500000 // 0.5 seconds per action for testing

int main(int argc, char** argv) {
    if (argc > 1) {
        if (!freopen(argv[1], "r", stdin)) {
            perror("Error opening file");
            return 1;
        }
    }

    printf("TEST COMMUNICATION: Starting...\n");
    
    // Initialize WiringPi and Pins
    setup();
    printf("Setup complete. Waiting for commands (AV, TD, TG)...\n");

    char cmd[16];
    while (scanf("%15s", cmd) == 1) {
        printf("Received: %s -> Executing...\n", cmd);
        
        if (strcmp(cmd, "AV") == 0) {
            avance();
            usleep(DELAY_US);
            stop();
        } else if (strcmp(cmd, "TD") == 0) {
            droite();
            usleep(DELAY_US);
            stop();
        } else if (strcmp(cmd, "TG") == 0) {
            gauche();
            usleep(DELAY_US);
            stop();
        } else {
            printf("Unknown Command: %s\n", cmd);
        }
        
        // Small pause between commands
        usleep(100000);
    }

    printf("TEST COMMUNICATION: Finished.\n");
    return 0;
}
