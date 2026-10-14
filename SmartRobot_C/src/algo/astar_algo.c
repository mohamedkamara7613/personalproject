#include "astar_algo.h"
#include "ListeChaineeListeOrdonnee.h"
#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <limits.h>

#define MAX_NODES 2500 // Support up to 50x50
#define MAX_STATES (MAX_NODES * 4) // 4 directions per node

typedef struct {
    int node;
    Direction dir;
} State;

typedef struct {
    State state;
    int g_score;
    int f_score;
    State parent_state; // detecting path
    ActionType action_from_parent;
} NodeData;


static int get_manhattan(int u, int v, int width) {
    // 1-based index
    int r1 = (u-1)/width;
    int c1 = (u-1)%width;
    int r2 = (v-1)/width;
    int c2 = (v-1)%width;
    return abs(r1 - r2) + abs(c1 - c2);
}

// Check connectivity and direction
static int get_neighbor_in_dir(G_Graphe g, int u, Direction dir, int width) {
    // Determine target coordinate
    int r = (u-1)/width;
    int c = (u-1)%width;
    
    int next_r = r, next_c = c;
    switch(dir) {
        case NORTH: next_r--; break;
        case SOUTH: next_r++; break;
        case EAST:  next_c++; break;
        case WEST:  next_c--; break;
    }

    if (next_r < 0 || next_r >= width || next_c < 0 || next_c >= width) return -1;
    
    int target = next_r * width + next_c + 1;
    
    // Check if edge exists in Graph
    if (G_arcPresent(g, u, target)) return target;
    return -1;
}


void* copy_node_data(void* src) {
    NodeData* n = malloc(sizeof(NodeData));
    *n = *((NodeData*)src);
    return n;
}
void free_node_data(void* d) { free(d); }
int compare_node_data(void* a, void* b) {
    NodeData* na = (NodeData*)a;
    NodeData* nb = (NodeData*)b;
    return na->f_score - nb->f_score; // ascending
}

Step* astar_search(G_Graphe g, int width, int start_node, Direction start_dir, int target_node, int* total_cost, int* rotation_count, int* steps_len) {
    // Closed Set: array of best g_scores
    int best_g[MAX_NODES][4];
    // Parent Pointers for reconstruction
    State parents[MAX_NODES][4];
    ActionType actions[MAX_NODES][4];

    for(int i=0; i<MAX_NODES; i++) {
        for(int d=0; d<4; d++) {
            best_g[i][d] = INT_MAX;
        }
    }

    LCLO_ListeOrdonnee openSet = LCLO_listeOrdonnee(copy_node_data, free_node_data, compare_node_data);
    
    NodeData start;
    start.state.node = start_node;
    start.state.dir = start_dir;
    start.g_score = 0;
    start.f_score = get_manhattan(start_node, target_node, width);
    start.parent_state.node = -1; // Root
    
    LCLO_inserer(&openSet, &start);
    best_g[start_node][start_dir] = 0;

    NodeData* final_node = NULL;


    while (!LCLO_estVide(openSet)) {
        NodeData* current = (NodeData*)LCLO_element(openSet, 0); // Peek/Pop min
        LCLO_supprimer(&openSet, 0); // Pop
        

        if (current->g_score > best_g[current->state.node][current->state.dir]) {
            free(current);
            continue;
        }


        if (current->state.node == target_node) {
            final_node = current; // Keep it to reconstruct

            break; 
        }

        // Explore Neighbors
        

        int neighbor = get_neighbor_in_dir(g, current->state.node, current->state.dir, width);
        if (neighbor != -1) {
            int new_g = current->g_score + COST_MOVE;
            if (new_g < best_g[neighbor][current->state.dir]) {
                best_g[neighbor][current->state.dir] = new_g;
                NodeData next;
                next.state.node = neighbor;
                next.state.dir = current->state.dir;
                next.g_score = new_g;
                next.f_score = new_g + get_manhattan(neighbor, target_node, width);
                next.parent_state = current->state;
                next.action_from_parent = ACTION_AV;
                
                parents[neighbor][current->state.dir] = current->state;
                actions[neighbor][current->state.dir] = ACTION_AV;

                LCLO_inserer(&openSet, &next);
            }
        }


        Direction right_dir = (current->state.dir + 1) % 4;
        int new_g_r = current->g_score + COST_TURN;
        if (new_g_r < best_g[current->state.node][right_dir]) {
             best_g[current->state.node][right_dir] = new_g_r;
             NodeData next;
             next.state.node = current->state.node;
             next.state.dir = right_dir;
             next.g_score = new_g_r; // + heuristic (same position)
             next.f_score = new_g_r + get_manhattan(current->state.node, target_node, width);
             next.parent_state = current->state;
             next.action_from_parent = ACTION_TD;
             
             parents[current->state.node][right_dir] = current->state;
             actions[current->state.node][right_dir] = ACTION_TD;

             LCLO_inserer(&openSet, &next);
        }


        Direction left_dir = (current->state.dir + 3) % 4;
        int new_g_l = current->g_score + COST_TURN;
        if (new_g_l < best_g[current->state.node][left_dir]) {
             best_g[current->state.node][left_dir] = new_g_l;
             NodeData next;
             next.state.node = current->state.node;
             next.state.dir = left_dir;
             next.g_score = new_g_l; 
             next.f_score = new_g_l + get_manhattan(current->state.node, target_node, width);
             next.parent_state = current->state;
             next.action_from_parent = ACTION_TG;
             
             parents[current->state.node][left_dir] = current->state;
             actions[current->state.node][left_dir] = ACTION_TG;

             LCLO_inserer(&openSet, &next);
        }

        free(current);
    }
    LCLO_vider(&openSet);

    if (final_node) {
        *total_cost = final_node->g_score;
        // Reconstruct
        // Use a temp buffer
        Step buffer[1000];
        int idx = 0;
        State curr = final_node->state;
        free(final_node);

        int rots = 0;
        *rotation_count = 0;

        while (curr.node != start_node || curr.dir != start_dir) {
            State p = parents[curr.node][curr.dir];
            ActionType act = actions[curr.node][curr.dir];
            Step s;
            s.type = act;
            s.target_node = curr.node; 
            buffer[idx++] = s;
            
            if (act == ACTION_TD || act == ACTION_TG) rots++;

            curr = p;
        }
        *rotation_count = rots;

        // Reverse
        Step* result = malloc(sizeof(Step) * (idx + 1));
        for(int i=0; i<idx; i++) {
            result[i] = buffer[idx - 1 - i];
        }
        result[idx].type = -1; // Terminator
        *steps_len = idx;
        return result;
    }

    return NULL;
}


Step* greedy_astar_patrol(G_Graphe g, int width, int start_node, Direction start_dir, int* checkpoints, int num_checkpoints, int* total_len, int* total_cost, int* total_rotations) {

    Step* full_path = malloc(sizeof(Step) * 5000);
    int fp_idx = 0;
    
    int current_node = start_node;
    Direction current_dir = start_dir;
    
    bool visited[20];
    for(int i=0; i<num_checkpoints; i++) visited[i] = false;
    int visited_count = 0;

    int grand_total_cost = 0;
    int grand_total_rots = 0;

    while (visited_count < num_checkpoints) {
        int best_cost = INT_MAX;
        Step* best_fragment = NULL;
        int best_frag_len = 0;
        int best_frag_rots = 0;
        int best_cp_idx = -1;
        
        // Find cheapest CP to reach
        for(int i=0; i<num_checkpoints; i++) {
            if(visited[i]) continue;
            
            int cost = 0, rots = 0, len = 0;
            Step* frag = astar_search(g, width, current_node, current_dir, checkpoints[i], &cost, &rots, &len);
            
            if (frag) {
                if(cost < best_cost) {
                    if (best_fragment) free(best_fragment);
                    best_cost = cost;
                    best_fragment = frag;
                    best_frag_len = len;
                    best_frag_rots = rots;
                    best_cp_idx = i;
                } else {
                    free(frag);
                }
            }
        }

        if (best_cp_idx != -1) {
             // Append
             for(int k=0; k<best_frag_len; k++) {
                 full_path[fp_idx++] = best_fragment[k];
             }
             
             // Update State
             // We can infer final direction from actions.
             for(int k=0; k<best_frag_len; k++) {
                 ActionType a = best_fragment[k].type;
                 if (a == ACTION_TD) current_dir = (current_dir+1)%4;
                 else if (a == ACTION_TG) current_dir = (current_dir+3)%4;
             }
             current_node = checkpoints[best_cp_idx];
             
             grand_total_cost += best_cost;
             grand_total_rots += best_frag_rots;
             visited[best_cp_idx] = true;
             visited_count++;
             free(best_fragment);
        } else {
             break;
        }
    }
    
     // Return to Start
    int cost = 0, rots = 0, len = 0;
    Step* frag_home = astar_search(g, width, current_node, current_dir, start_node, &cost, &rots, &len);
    if(frag_home) {
         for(int k=0; k<len; k++) {
             full_path[fp_idx++] = frag_home[k];
         }
         grand_total_cost += cost;
         grand_total_rots += rots;
         free(frag_home);
    }

    full_path[fp_idx].type = -1;
    *total_len = fp_idx;
    *total_cost = grand_total_cost;
    *total_rotations = grand_total_rots;

    return full_path;
}
