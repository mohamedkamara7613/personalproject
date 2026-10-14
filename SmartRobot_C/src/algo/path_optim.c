#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "labyrinth_parsing.h"
#include "tsp_algo.h"
#include "astar_algo.h"

int main(int argc, char** argv) {
    
    char* filename = "utils/labyTexte/labyrinthe.txt"; // Default relative path from bin/
    if (argc > 1) filename = argv[1];


    CityConfig city = load_city(filename);


    
    int* checkpoints = city.checkpoints;
    int num_cps = city.num_checkpoints;


    
    int tsp_astar_len = 0;
    int tsp_astar_cost = 0;
    int tsp_astar_rots = 0;
    
    Step* tsp_path = solve_tsp_astar(city.graph, city.width, city.start_node, city.start_dir, checkpoints, num_cps, &tsp_astar_len, &tsp_astar_cost, &tsp_astar_rots);

    if (tsp_path) {
        for(int i=0; i<tsp_astar_len; i++) {
            switch(tsp_path[i].type) {
                case ACTION_AV: printf("AV "); break;
                case ACTION_TD: printf("TD "); break;
                case ACTION_TG: printf("TG "); break;
            }
        }
        printf("\n");
        free(tsp_path);
    } else {
        printf("    FAILED (No path found)\n");
    }

    return 0;
}
