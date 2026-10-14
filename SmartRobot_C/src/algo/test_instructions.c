#include <stdio.h>
#include <stdlib.h>
#include <CUnit/Basic.h>
#include "astar_algo.h"

int init_suite(void) { return 0; }
int clean_suite(void) { return 0; }

void test_step_struct(void) {
    Step s;
    s.type = ACTION_TG;
    s.target_node = 10;
    
    CU_ASSERT_EQUAL(s.type, ACTION_TG);
    CU_ASSERT_EQUAL(s.target_node, 10);
}


void test_enums(void) {
    CU_ASSERT_EQUAL(NORTH, 0);
    CU_ASSERT_EQUAL(EAST, 1);
    CU_ASSERT_EQUAL(SOUTH, 2);
    CU_ASSERT_EQUAL(WEST, 3);
    
    CU_ASSERT_EQUAL(ACTION_AV, 0);
    CU_ASSERT_EQUAL(ACTION_TD, 1);
    CU_ASSERT_EQUAL(ACTION_TG, 2);
}

int main() {
    CU_pSuite pSuite = NULL;

    if (CUE_SUCCESS != CU_initialize_registry())
        return CU_get_error();

    pSuite = CU_add_suite("Suite_Instructions", init_suite, clean_suite);
    if (NULL == pSuite) {
        CU_cleanup_registry();
        return CU_get_error();
    }

    if ((NULL == CU_add_test(pSuite, "Step Structure", test_step_struct)) ||
        (NULL == CU_add_test(pSuite, "Enum Values", test_enums)))
    {
        CU_cleanup_registry();
        return CU_get_error();
    }

    CU_basic_set_mode(CU_BRM_VERBOSE);
    CU_basic_run_tests();
    CU_cleanup_registry();
    return CU_get_error();
}
