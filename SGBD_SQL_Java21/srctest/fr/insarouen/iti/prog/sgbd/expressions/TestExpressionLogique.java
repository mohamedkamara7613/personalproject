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

public class TestExpressionLogique {

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
    public void test_evaluerexpression_avecUneSeuleConditionVraie() throws Exception {
        ExpressionLogique expression = new ExpressionLogique();

        ConditionSimple condition = new ConditionSimple(
                new Operande("age"),
                Operateur.SUP,
                new Operande(new ValeurInt(18))
        );

        expression.ajouterCondition(condition);

        assertThat(expression.evaluerexpression(this.tuple, this.table), equalTo(true));
    }

    @Test
    public void test_evaluerexpression_avecUneSeuleConditionFausse() throws Exception {
        ExpressionLogique expression = new ExpressionLogique();

        ConditionSimple condition = new ConditionSimple(
                new Operande("age"),
                Operateur.SUP,
                new Operande(new ValeurInt(25))
        );

        expression.ajouterCondition(condition);

        assertThat(expression.evaluerexpression(this.tuple, this.table), equalTo(false));
    }

    @Test
    public void test_evaluerexpression_AND_retourneVrai_siLesDeuxConditionsSontVraies() throws Exception {
        ExpressionLogique expression = new ExpressionLogique();

        ConditionSimple condition1 = new ConditionSimple(
                new Operande("age"),
                Operateur.SUP,
                new Operande(new ValeurInt(18))
        );

        ConditionSimple condition2 = new ConditionSimple(
                new Operande("nom"),
                Operateur.EGAL,
                new Operande(new ValeurVarchar("Youssef"))
        );

        expression.ajouterCondition(condition1);
        expression.ajouterOperateurEtCondition(OperateurLogique.AND, condition2);

        assertThat(expression.evaluerexpression(this.tuple, this.table), equalTo(true));
    }

    @Test
    public void test_evaluerexpression_AND_retourneFaux_siUneConditionEstFausse() throws Exception {
        ExpressionLogique expression = new ExpressionLogique();

        ConditionSimple condition1 = new ConditionSimple(
                new Operande("age"),
                Operateur.SUP,
                new Operande(new ValeurInt(18))
        );

        ConditionSimple condition2 = new ConditionSimple(
                new Operande("nom"),
                Operateur.EGAL,
                new Operande(new ValeurVarchar("Batman"))
        );

        expression.ajouterCondition(condition1);
        expression.ajouterOperateurEtCondition(OperateurLogique.AND, condition2);

        assertThat(expression.evaluerexpression(this.tuple, this.table), equalTo(false));
    }

    @Test
    public void test_evaluerexpression_OR_retourneVrai_siUneConditionEstVraie() throws Exception {
        ExpressionLogique expression = new ExpressionLogique();

        ConditionSimple condition1 = new ConditionSimple(
                new Operande("age"),
                Operateur.SUP,
                new Operande(new ValeurInt(25))
        );

        ConditionSimple condition2 = new ConditionSimple(
                new Operande("nom"),
                Operateur.EGAL,
                new Operande(new ValeurVarchar("Youssef"))
        );

        expression.ajouterCondition(condition1);
        expression.ajouterOperateurEtCondition(OperateurLogique.OR, condition2);

        assertThat(expression.evaluerexpression(this.tuple, this.table), equalTo(true));
    }

    @Test
    public void test_evaluerexpression_OR_retourneFaux_siLesDeuxConditionsSontFausses() throws Exception {
        ExpressionLogique expression = new ExpressionLogique();

        ConditionSimple condition1 = new ConditionSimple(
                new Operande("age"),
                Operateur.SUP,
                new Operande(new ValeurInt(25))
        );

        ConditionSimple condition2 = new ConditionSimple(
                new Operande("nom"),
                Operateur.EGAL,
                new Operande(new ValeurVarchar("Batman"))
        );

        expression.ajouterCondition(condition1);
        expression.ajouterOperateurEtCondition(OperateurLogique.OR, condition2);

        assertThat(expression.evaluerexpression(this.tuple, this.table), equalTo(false));
    }

    @Test
    public void test_evaluerexpression_avecTroisConditions() throws Exception {
        ExpressionLogique expression = new ExpressionLogique();

        ConditionSimple condition1 = new ConditionSimple(
                new Operande("age"),
                Operateur.SUP,
                new Operande(new ValeurInt(18))
        );

        ConditionSimple condition2 = new ConditionSimple(
                new Operande("nom"),
                Operateur.EGAL,
                new Operande(new ValeurVarchar("Youssef"))
        );

        ConditionSimple condition3 = new ConditionSimple(
                new Operande("id"),
                Operateur.EGAL,
                new Operande(new ValeurInt(1))
        );

        expression.ajouterCondition(condition1);
        expression.ajouterOperateurEtCondition(OperateurLogique.AND, condition2);
        expression.ajouterOperateurEtCondition(OperateurLogique.AND, condition3);

        assertThat(expression.evaluerexpression(this.tuple, this.table), equalTo(true));
    }

    @Test(expected = AttributInconnuException.class)
    public void test_evaluerexpression_leveException_siColonneInconnue() throws Exception {
        ExpressionLogique expression = new ExpressionLogique();

        ConditionSimple condition = new ConditionSimple(
                new Operande("taille"),
                Operateur.EGAL,
                new Operande(new ValeurInt(180))
        );

        expression.ajouterCondition(condition);

        expression.evaluerexpression(this.tuple, this.table);
    }

    @Test(expected = TypesIncompatibleException.class)
    public void test_evaluerexpression_leveException_siTypesIncompatibles() throws Exception {
        ExpressionLogique expression = new ExpressionLogique();

        ConditionSimple condition = new ConditionSimple(
                new Operande("age"),
                Operateur.EGAL,
                new Operande(new ValeurVarchar("20"))
        );

        expression.ajouterCondition(condition);

        expression.evaluerexpression(this.tuple, this.table);
    }
}