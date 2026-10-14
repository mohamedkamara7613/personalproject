#include "tsp_algo.h"
#include "astar_algo.h"
#include <stdio.h>
#include <stdlib.h>
#include <limits.h>
#include <string.h>


void swap(int *x, int *y) {
    int temp = *x;
    *x = *y;
    *y = temp;
}

// Global best state for A* TSP
static int min_cost_astar = INT_MAX;
static int* best_perm_astar = NULL;
static int best_rots_astar = 0;

// Recursive permutation generator for A* TSP
void permute_astar(int *a, int l, int r, G_Graphe g, int width, int start_node, Direction start_dir, int* checkpoints, int num_cps) {
    if (l == r) {
        // Evaluate this permutation

        
        int current_total_cost = 0;
        int current_total_rots = 0;
        
        int curr_node = start_node;
        Direction curr_dir = start_dir;
        bool possible = true;

        for(int i=0; i<num_cps; i++) {
            int target_cp = checkpoints[a[i]];
            int seg_cost=0, seg_rots=0, seg_len=0;
            
            Step* path = astar_search(g, width, curr_node, curr_dir, target_cp, &seg_cost, &seg_rots, &seg_len);
            
            if (!path) { possible = false; break; }
            
            current_total_cost += seg_cost;
            current_total_rots += seg_rots;

            // Update state based on path
            for(int k=0; k<seg_len; k++) {
                if(path[k].type == ACTION_TD) curr_dir = (curr_dir + 1) % 4;
                else if(path[k].type == ACTION_TG) curr_dir = (curr_dir + 3) % 4;
            }
            curr_node = target_cp;
            free(path);
        }

        if (possible) {
            // Return to start
            int seg_cost=0, seg_rots=0, seg_len=0;
            Step* path = astar_search(g, width, curr_node, curr_dir, start_node, &seg_cost, &seg_rots, &seg_len);
            if (path) {
                current_total_cost += seg_cost;
                current_total_rots += seg_rots;
                free(path);
            } else {
                possible = false;
            }
        }

        if (possible && current_total_cost < min_cost_astar) {
            min_cost_astar = current_total_cost;
            best_rots_astar = current_total_rots;
            for(int i=0; i<num_cps; i++) best_perm_astar[i] = a[i];
        }

    } else {
         for (int i = l; i <= r; i++) {
            swap((a + l), (a + i));
            permute_astar(a, l + 1, r, g, width, start_node, start_dir, checkpoints, num_cps);
            swap((a + l), (a + i)); 
        }
    }
}

Step* solve_tsp_astar(G_Graphe g, int width, int start_node, Direction start_dir, int* checkpoints, int num_checkpoints, int* total_actions, int* total_cost, int* total_rots) {
    int* p_indices = malloc(num_checkpoints * sizeof(int));
    for(int i=0; i<num_checkpoints; i++) p_indices[i] = i;

    best_perm_astar = malloc(num_checkpoints * sizeof(int));
    min_cost_astar = INT_MAX;
    best_rots_astar = 0;

    permute_astar(p_indices, 0, num_checkpoints - 1, g, width, start_node, start_dir, checkpoints, num_checkpoints);
    
    if (min_cost_astar == INT_MAX) {
        free(p_indices);
        free(best_perm_astar);
        return NULL;
    }

    // Reconstruct Best Path
    Step* full_path_buffer = malloc(sizeof(Step) * 5000);
    int fp_idx = 0;
    
    int curr_node = start_node;
    Direction curr_dir = start_dir;
    
    for(int i=0; i<num_checkpoints; i++) {
        int target_cp = checkpoints[best_perm_astar[i]];
        int len=0, c=0, r=0;
        Step* path = astar_search(g, width, curr_node, curr_dir, target_cp, &c, &r, &len);
        
        for(int k=0; k<len; k++) {
             full_path_buffer[fp_idx++] = path[k];
             if(path[k].type == ACTION_TD) curr_dir = (curr_dir + 1) % 4;
             else if(path[k].type == ACTION_TG) curr_dir = (curr_dir + 3) % 4;
        }
        curr_node = target_cp;
        free(path);
    }
    
    // Return
    int len=0, c=0, r=0;
    Step* path = astar_search(g, width, curr_node, curr_dir, start_node, &c, &r, &len);
    if (path) {
        for(int k=0; k<len; k++) {
             full_path_buffer[fp_idx++] = path[k];
        }
        free(path);
    }
    
    full_path_buffer[fp_idx].type = -1;
    
    *total_actions = fp_idx;
    *total_cost = min_cost_astar;
    *total_rots = best_rots_astar;

    free(p_indices);
    free(best_perm_astar);
    return full_path_buffer;
}
