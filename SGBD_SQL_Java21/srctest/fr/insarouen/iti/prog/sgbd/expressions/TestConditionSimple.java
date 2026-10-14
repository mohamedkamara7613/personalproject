package fr.insarouen.iti.prog.sgbd.expressions;

import fr.insarouen.iti.prog.sgbd.exceptions.AttributInconnuException;
import fr.insarouen.iti.prog.sgbd.exceptions.TypesIncompatibleException;
import fr.insarouen.iti.prog.sgbd.modele.Attribut;
import fr.insarouen.iti.prog.sgbd.modele.Table;
import fr.insarouen.iti.prog.sgbd.modele.Tuple;
import fr.insarouen.iti.prog.sgbd.modele.Type;
import fr.insarouen.iti.prog.sgbd.modele.ValeurInt;
import fr.insarouen.iti.prog.sgbd.modele.ValeurVarchar;

import java.util.Arrays;

import org.junit.Before;
import org.junit.Test;

import static org.hamcrest.CoreMatchers.equalTo;
import static org.hamcrest.MatcherAssert.assertThat;

public class TestConditionSimple {

    private Table table;
    private Tuple tuple;

    @Before
    public void avantTest() {
        this.table = new Table("personnes", Arrays.asList(
                new Attribut("id", Type.INT),
                new Attribut("nom", Type.VARCHAR),
                new Attribut("age", Type.INT)
        ));

        this.tuple = new Tuple(Arrays.asList(
                new ValeurInt(1),
                new ValeurVarchar("Youssef"),
                new ValeurInt(20)
        ));
    }

    @Test
    public void test_evaluerCondition_EGAL_retourneVrai() throws Exception {
        ConditionSimple condition = new ConditionSimple(
                new Operande("age"),
                Operateur.EGAL,
                new Operande(new ValeurInt(20))
        );

        assertThat(condition.evaluerCondition(this.tuple, this.table), equalTo(true));
    }

    @Test
    public void test_evaluerCondition_SUP_retourneVrai() throws Exception {
        ConditionSimple condition = new ConditionSimple(
                new Operande("age"),
                Operateur.SUP,
                new Operande(new ValeurInt(18))
        );

        assertThat(condition.evaluerCondition(this.tuple, this.table), equalTo(true));
    }

    @Test
    public void test_evaluerCondition_INF_retourneVrai() throws Exception {
        ConditionSimple condition = new ConditionSimple(
                new Operande("age"),
                Operateur.INF,
                new Operande(new ValeurInt(30))
        );

        assertThat(condition.evaluerCondition(this.tuple, this.table), equalTo(true));
    }

    @Test
    public void test_evaluerCondition_EGAL_surChaine_retourneVrai() throws Exception {
        ConditionSimple condition = new ConditionSimple(
                new Operande("nom"),
                Operateur.EGAL,
                new Operande(new ValeurVarchar("Youssef"))
        );

        assertThat(condition.evaluerCondition(this.tuple, this.table), equalTo(true));
    }

    @Test
    public void test_evaluerCondition_retourneFaux_siConditionFausse() throws Exception {
        ConditionSimple condition = new ConditionSimple(
                new Operande("age"),
                Operateur.SUP,
                new Operande(new ValeurInt(25))
        );

        assertThat(condition.evaluerCondition(this.tuple, this.table), equalTo(false));
    }

    @Test(expected = AttributInconnuException.class)
    public void test_evaluerCondition_leveException_siColonneInconnue() throws Exception {
        ConditionSimple condition = new ConditionSimple(
                new Operande("taille"),
                Operateur.EGAL,
                new Operande(new ValeurInt(180))
        );

        condition.evaluerCondition(this.tuple, this.table);
    }

    @Test(expected = TypesIncompatibleException.class)
    public void test_evaluerCondition_leveException_siTypesIncompatibles() throws Exception {
        ConditionSimple condition = new ConditionSimple(
                new Operande("age"),
                Operateur.EGAL,
                new Operande(new ValeurVarchar("20"))
        );

        condition.evaluerCondition(this.tuple, this.table);
    }
}