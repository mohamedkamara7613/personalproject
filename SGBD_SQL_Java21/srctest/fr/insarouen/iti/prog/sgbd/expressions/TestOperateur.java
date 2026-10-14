package fr.insarouen.iti.prog.sgbd.expressions;

import org.junit.Test;

import static org.hamcrest.CoreMatchers.equalTo;
import static org.hamcrest.MatcherAssert.assertThat;

public class TestOperateur {

    @Test
    public void test_operateur_EGAL_existe() {
        assertThat(Operateur.EGAL.name(), equalTo("EGAL"));
    }

    @Test
    public void test_operateur_SUP_existe() {
        assertThat(Operateur.SUP.name(), equalTo("SUP"));
    }

    @Test
    public void test_operateur_INF_existe() {
        assertThat(Operateur.INF.name(), equalTo("INF"));
    }

    @Test
    public void test_operateur_valueOf_EGAL() {
        assertThat(Operateur.valueOf("EGAL"), equalTo(Operateur.EGAL));
    }

    @Test
    public void test_operateur_valueOf_SUP() {
        assertThat(Operateur.valueOf("SUP"), equalTo(Operateur.SUP));
    }

    @Test
    public void test_operateur_valueOf_INF() {
        assertThat(Operateur.valueOf("INF"), equalTo(Operateur.INF));
    }

    @Test
    public void test_operateur_values_contientTroisOperateurs() {
        assertThat(Operateur.values().length, equalTo(3));
    }
}