#include "labyrinth_parsing.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "graphe.h"


static Direction parse_direction(char c) {
    switch(c) {
        case 'H': case 'N': return NORTH;
        case 'B': case 'S': return SOUTH;
        case 'G': case 'O': case 'W': return WEST;
        case 'D': case 'E': return EAST;
        default: return NORTH; 
    }
}

CityConfig load_city(const char* filename) {
    CityConfig config;
    config.num_checkpoints = 0;
    
    FILE* f = fopen(filename, "r");
    if (!f) {
        fprintf(stderr, "Error: Could not open file %s\n", filename);
        exit(1);
    }

    char line[100];


    if (fgets(line, sizeof(line), f)) {
        int n = atoi(line);
        config.width = n;
        config.height = n;
    }


    if (fgets(line, sizeof(line), f)) {
        int node;
        char dir;
        sscanf(line, "%d%c", &node, &dir);
        config.start_node = node;
        config.start_dir = parse_direction(dir);
    }



    config.graph = G_graphe(0, NULL, NULL, NULL, NULL, NULL, NULL); 
    

    for(int i=1; i <= config.width * config.height; i++) {
        G_ajouterSommet(&config.graph, (unsigned int)i, NULL);
    }


    while (fgets(line, sizeof(line), f)) {
        if (line[0] == '.') break;
        
        int u, v;
            if (sscanf(line, "%d-%d", &u, &v) == 2) {
            if (!G_sommetPresent(config.graph, (unsigned int)u)) G_ajouterSommet(&config.graph, (unsigned int)u, NULL);
            if (!G_sommetPresent(config.graph, (unsigned int)v)) G_ajouterSommet(&config.graph, (unsigned int)v, NULL);
            
            G_ajouterArc(&config.graph, (unsigned int)u, (unsigned int)v, NULL);
            G_ajouterArc(&config.graph, (unsigned int)v, (unsigned int)u, NULL);
        } else if (sscanf(line, "%d", &u) == 1) {
            if (config.num_checkpoints < 100) {
                config.checkpoints[config.num_checkpoints++] = u;
            }
        }
    }

    fclose(f);
    return config;
}
