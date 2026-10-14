#include <stdio.h>
#include <stdlib.h>
#include <CUnit/Basic.h>
#include "graphe.h"

int init_suite(void) { return 0; }
int clean_suite(void) { return 0; }

void test_creation_graphe(void) {
    // Graphe non orienté, non étiqueté, non valué
    G_Graphe g = G_graphe(false, NULL, NULL, NULL, NULL, NULL, NULL);
    CU_ASSERT_FALSE(g.oriente);
    
    // Graphe orienté
    G_Graphe go = G_graphe(true, NULL, NULL, NULL, NULL, NULL, NULL);
    CU_ASSERT_TRUE(go.oriente);
    
    G_vider(&g); 
    G_vider(&go);
}

void test_ajout_suppression_sommet(void) {
    G_Graphe g = G_graphe(false, NULL, NULL, NULL, NULL, NULL, NULL);
    
    // Ajout sommets
    CU_ASSERT_EQUAL(G_ajouterSommet(&g, 0, NULL), 0);
    CU_ASSERT_EQUAL(G_ajouterSommet(&g, 1, NULL), 1);
    
    // Vérification présence
    CU_ASSERT_TRUE(G_sommetPresent(g, 0));
    CU_ASSERT_TRUE(G_sommetPresent(g, 1));
    CU_ASSERT_FALSE(G_sommetPresent(g, 2));
    
    // Suppression
    CU_ASSERT_EQUAL(G_supprimerSommet(&g, 1), 0);
    CU_ASSERT_FALSE(G_sommetPresent(g, 1));
    
    G_vider(&g);
}

void test_ajout_suppression_arc(void) {
    G_Graphe g = G_graphe(false, NULL, NULL, NULL, NULL, NULL, NULL); // Non orienté
    G_ajouterSommet(&g, 0, NULL);
    G_ajouterSommet(&g, 1, NULL);
    G_ajouterSommet(&g, 2, NULL);
    
    // Ajout arc 0-1
    CU_ASSERT_EQUAL(G_ajouterArc(&g, 0, 1, NULL), 0);
    CU_ASSERT_TRUE(G_arcPresent(g, 0, 1));
    CU_ASSERT_TRUE(G_arcPresent(g, 1, 0)); // Car non orienté
    
    // Arc pas encore là
    CU_ASSERT_FALSE(G_arcPresent(g, 0, 2));
    
    // Suppression
    CU_ASSERT_EQUAL(G_supprimerArc(&g, 0, 1), 0);
    CU_ASSERT_FALSE(G_arcPresent(g, 0, 1));
    CU_ASSERT_FALSE(G_arcPresent(g, 1, 0));
    
    G_vider(&g);
}

void test_sommets_adjacents(void) {
    G_Graphe g = G_graphe(true, NULL, NULL, NULL, NULL, NULL, NULL); // Orienté cette fois
    G_ajouterSommet(&g, 0, NULL);
    G_ajouterSommet(&g, 1, NULL);
    G_ajouterSommet(&g, 2, NULL);
    
    G_ajouterArc(&g, 0, 1, NULL); // 0 -> 1
    G_ajouterArc(&g, 0, 2, NULL); // 0 -> 2
    
    LCL_Liste adj = G_obtenirSommetsAdjacents(g, 0);
    CU_ASSERT_FALSE(adj.longueur == 0);
    
    LCL_Liste adj2 = G_obtenirSommetsAdjacents(g, 1);
    CU_ASSERT_TRUE(adj2.longueur == 0); // 1 n'a pas de sortants
    
    LCL_vider(&adj);
    LCL_vider(&adj2);
    G_vider(&g);
}

int main() {
    CU_pSuite pSuite = NULL;
    if (CUE_SUCCESS != CU_initialize_registry()) return CU_get_error();

    pSuite = CU_add_suite("Suite_Graphe", init_suite, clean_suite);
    if (NULL == pSuite) { CU_cleanup_registry(); return CU_get_error(); }

    if ((NULL == CU_add_test(pSuite, "Creation Graphe", test_creation_graphe)) ||
        (NULL == CU_add_test(pSuite, "Ajout/Suppression Sommet", test_ajout_suppression_sommet)) ||
        (NULL == CU_add_test(pSuite, "Ajout/Suppression Arc", test_ajout_suppression_arc)) ||
        (NULL == CU_add_test(pSuite, "Sommets Adjacents", test_sommets_adjacents)))
    {
        CU_cleanup_registry();
        return CU_get_error();
    }

    CU_basic_set_mode(CU_BRM_VERBOSE);
    CU_basic_run_tests();
    CU_cleanup_registry();
    return CU_get_error();
}
