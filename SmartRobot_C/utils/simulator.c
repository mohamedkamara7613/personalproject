#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "labyrinth_parsing.h"
#include "astar_algo.h" 

// ANSI Colors
#define RED "\033[31m"
#define GREEN "\033[32m"
#define RESET "\033[0m"

void update_pos(int* node, Direction* dir, ActionType action, int width, int height, G_Graphe graph) {
    if (action == ACTION_TD) {
        *dir = (*dir + 1) % 4;
        printf("Turned RIGHT (Now %d)\n", *dir);
    } else if (action == ACTION_TG) {
        *dir = (*dir + 3) % 4;
        printf("Turned LEFT (Now %d)\n", *dir);
    } else if (action == ACTION_AV) {
        int idx = *node - 1;
        int r = idx / width;
        int c = idx % width;
        
        int nr = r, nc = c;
        if (*dir == NORTH) nr--;
        else if (*dir == SOUTH) nr++;
        else if (*dir == WEST) nc--;
        else if (*dir == EAST) nc++;
        
        if (nr < 0 || nr >= height || nc < 0 || nc >= width) {
            printf(RED "CRASH! Wall/Boundary at %d (%d,%d) moving to (%d,%d)\n" RESET, *node, r, c, nr, nc);
            exit(1);
        }
        
        int next_node = nr * width + nc + 1;
        
        // Check connectivity in Graph (Wall check)
        if (!G_arcPresent(graph, *node, next_node)) {
             printf(RED "CRASH! Wall detected between %d and %d\n" RESET, *node, next_node);
             exit(1);
        }
        
        *node = next_node;
        printf(GREEN "Moved to %d (%d,%d)\n" RESET, *node, nr, nc);
    }
}

int main(int argc, char** argv) {
    if (argc < 2) {
        fprintf(stderr, "Usage: %s <map_file> < (pipe commands)\n", argv[0]);
        return 1;
    }

    // Load Map
    CityConfig city = load_city(argv[1]);
    
    int current_node = city.start_node;
    Direction current_dir = city.start_dir;
    
    printf("SIMULATOR: Started at %d, Dir %d\n", current_node, current_dir);

    // Read Commands from Stdin
    // Expecting words like "AV", "TD", "TG"
    char word[10];
    int goal_visited = 0;
    if (current_node == city.end_node) goal_visited = 1;

    while (scanf("%9s", word) == 1) {
        if (strcmp(word, "AV") == 0) update_pos(&current_node, &current_dir, ACTION_AV, city.width, city.height, city.graph);
        else if (strcmp(word, "TD") == 0) update_pos(&current_node, &current_dir, ACTION_TD, city.width, city.height, city.graph);
        else if (strcmp(word, "TG") == 0) update_pos(&current_node, &current_dir, ACTION_TG, city.width, city.height, city.graph);
        
        if (current_node == city.end_node) {
             goal_visited = 1;
             printf(GREEN ">>> VISITED CHECKPOINT/GOAL %d <<<\n" RESET, current_node);
        }
    }
    
    if (goal_visited) {
        printf(GREEN "SUCCESS: Mission Accomplished (Goal visited)!\n" RESET);
    } else {
        printf(RED "FAILURE: Goal %d never reached.\n" RESET, city.end_node);
    }

    return 0;
}
