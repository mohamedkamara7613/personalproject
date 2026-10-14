package fr.insarouen.iti.prog.sgbd.expressions;

import org.junit.Test;

import static org.hamcrest.CoreMatchers.equalTo;
import static org.hamcrest.MatcherAssert.assertThat;

public class TestOperateurLogique {

    @Test
    public void test_operateurLogique_AND_existe() {
        assertThat(OperateurLogique.AND.name(), equalTo("AND"));
    }

    @Test
    public void test_operateurLogique_OR_existe() {
        assertThat(OperateurLogique.OR.name(), equalTo("OR"));
    }

    @Test
    public void test_operateurLogique_valueOf_AND() {
        assertThat(OperateurLogique.valueOf("AND"), equalTo(OperateurLogique.AND));
    }

    @Test
    public void test_operateurLogique_valueOf_OR() {
        assertThat(OperateurLogique.valueOf("OR"), equalTo(OperateurLogique.OR));
    }

    @Test
    public void test_operateurLogique_values_contientDeuxOperateurs() {
        assertThat(OperateurLogique.values().length, equalTo(2));
    }
}