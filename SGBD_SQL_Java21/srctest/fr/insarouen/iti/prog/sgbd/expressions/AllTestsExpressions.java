package fr.insarouen.iti.prog.sgbd.expressions;

import org.junit.runner.RunWith;
import org.junit.runners.Suite;
import org.junit.runners.Suite.SuiteClasses;

@RunWith(Suite.class)
@SuiteClasses({
    TestConditionSimple.class,
    TestExpressionLogique.class,
    TestOperateur.class,
    TestOperateurLogique.class,
    TestOperande.class
})
public class AllTestsExpressions {}