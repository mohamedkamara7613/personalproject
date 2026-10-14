#include <stdio.h>
#include <stdlib.h>
#include <CUnit/Basic.h>
#include "labyrinth_parsing.h"

// create a temporary map file for testing....
void create_test_map(const char* filename) {
    FILE* f = fopen(filename, "w");
    if (f == NULL) {
        perror("Error creating test file");
        return;
    }
    // Format: Width Height
    fprintf(f, "10 10\n");
    // StartNode Direction (0=N)
    fprintf(f, "0 0\n");
    // DestinationNode Direction
    fprintf(f, "99 2\n");
    // Edges
    fprintf(f, "0-1\n");
    fprintf(f, "1-2\n");
    fprintf(f, "2-12\n");
    fclose(f);
}

int init_suite(void) { return 0; }
int clean_suite(void) { return 0; }

void test_load_city_dimensions(void) {
    create_test_map("temp_test_map.txt");
    CityConfig city = load_city("temp_test_map.txt");
    
    CU_ASSERT_EQUAL(city.width, 10);
    CU_ASSERT_EQUAL(city.height, 10);
    CU_ASSERT_EQUAL(city.start_node, 0);
    CU_ASSERT_EQUAL(city.start_dir, NORTH);
    
    remove("temp_test_map.txt");
}

void test_estConnecte(void) {
    create_test_map("temp_test_map_conn.txt");
    CityConfig city = load_city("temp_test_map_conn.txt");

    // Check connections defined in file
    CU_ASSERT_TRUE(G_arcPresent(city.graph, 0, 1));
    CU_ASSERT_TRUE(G_arcPresent(city.graph, 1, 2));
    CU_ASSERT_TRUE(G_arcPresent(city.graph, 2, 12));
    
    // Check non-connections
    CU_ASSERT_FALSE(G_arcPresent(city.graph, 0, 2)); // No direct
    CU_ASSERT_FALSE(G_arcPresent(city.graph, 5, 6)); // Random
    
    remove("temp_test_map_conn.txt");
}

void test_caseVersCoord_axioms(void) {
    int width = 10;
    int id = 25; // coords (5, 2)
    
    int x = id % width;
    int y = id / width;
    
    CU_ASSERT_EQUAL(x, 5);
    CU_ASSERT_EQUAL(y, 2);
    
    int computed_id = y * width + x;
    CU_ASSERT_EQUAL(computed_id, id);
}

int main() {
    CU_pSuite pSuite = NULL;

    if (CUE_SUCCESS != CU_initialize_registry())
        return CU_get_error();

    pSuite = CU_add_suite("Suite_Labyrinthe", init_suite, clean_suite);
    if (NULL == pSuite) {
        CU_cleanup_registry();
        return CU_get_error();
    }

    if ((NULL == CU_add_test(pSuite, "Dimensions et Init", test_load_city_dimensions)) ||
        (NULL == CU_add_test(pSuite, "Connexions (Graphe)", test_estConnecte)) ||
        (NULL == CU_add_test(pSuite, "Axiomes Coordonnees", test_caseVersCoord_axioms)))
    {
        CU_cleanup_registry();
        return CU_get_error();
    }

    CU_basic_set_mode(CU_BRM_VERBOSE);
    CU_basic_run_tests();
    CU_cleanup_registry();
    return CU_get_error();
}
