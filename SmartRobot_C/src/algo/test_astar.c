#include <stdio.h>
#include <stdlib.h>
#include <CUnit/Basic.h>
#include "astar_algo.h"

int init_suite(void) { return 0; }
int clean_suite(void) { return 0; }

// grid graph 3x3
// 0(N)-1-2
// |    |
// 3    4-5
// |      |
// 6-7-8--+
// Width = 3
// Nodes: 0..8
// Connections: 0-1, 1-2, 0-3, 3-6, 1-4, 4-5, 5-8, 6-7, 7-8
void build_simple_grid(G_Graphe* g) {
    for(int i=0; i<9; i++) G_ajouterSommet(g, i, NULL);
    
    // Horizontal
    G_ajouterArc(g, 0, 1, NULL);
    G_ajouterArc(g, 1, 2, NULL);
    G_ajouterArc(g, 4, 5, NULL);
    G_ajouterArc(g, 6, 7, NULL);
    G_ajouterArc(g, 7, 8, NULL);
    
    // Vertical
    G_ajouterArc(g, 0, 3, NULL); // 0 is (0,0), 3 is (0,1)
    G_ajouterArc(g, 3, 6, NULL);
    G_ajouterArc(g, 1, 4, NULL);
    G_ajouterArc(g, 5, 8, NULL);
}

void test_astar_simple_path(void) {
    G_Graphe g = G_graphe(false, NULL, NULL, NULL, NULL, NULL, NULL);
    build_simple_grid(&g);
    
    int width = 3;
    int start = 0; // (0,0)
    Direction startStruct = NORTH;
    int target = 8; // (2,2)
    
    int total_cost, rotation_count, steps_len;
    
    
    Step* path = astar_search(g, width, start, startStruct, target, &total_cost, &rotation_count, &steps_len);
    
    CU_ASSERT_PTR_NOT_NULL(path);
    CU_ASSERT_TRUE(steps_len > 0);
    
   
    if (steps_len > 0) {
        
        CU_ASSERT_EQUAL(path[steps_len-1].target_node, target);
        
        CU_ASSERT_TRUE(steps_len >= 4);
        
        CU_ASSERT_TRUE(total_cost >= 4);
    }
    
    free(path);
    G_vider(&g);
}

void test_astar_no_path(void) {
    G_Graphe g = G_graphe(false, NULL, NULL, NULL, NULL, NULL, NULL);
    G_ajouterSommet(&g, 0, NULL);
    G_ajouterSommet(&g, 1, NULL);
    // No edges
    
    int width = 2;
    int total_cost, rotation_count, steps_len;
    Step* path = astar_search(g, width, 0, NORTH, 1, &total_cost, &rotation_count, &steps_len);
    
    CU_ASSERT_PTR_NULL(path);
    CU_ASSERT_EQUAL(steps_len, 0);
    
    G_vider(&g);
}

int main() {
    CU_pSuite pSuite = NULL;
    if (CUE_SUCCESS != CU_initialize_registry()) return CU_get_error();

    pSuite = CU_add_suite("Suite_Astar", init_suite, clean_suite);
    if (NULL == pSuite) { CU_cleanup_registry(); return CU_get_error(); }

    if ((NULL == CU_add_test(pSuite, "A* Simple Path", test_astar_simple_path)) ||
        (NULL == CU_add_test(pSuite, "A* No Path", test_astar_no_path)))
    {
        CU_cleanup_registry();
        return CU_get_error();
    }

    CU_basic_set_mode(CU_BRM_VERBOSE);
    CU_basic_run_tests();
    CU_cleanup_registry();
    return CU_get_error();
}
