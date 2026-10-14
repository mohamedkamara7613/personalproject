package fr.insarouen.iti.prog.sgbd.expressions;

import fr.insarouen.iti.prog.sgbd.exceptions.AttributInconnuException;
import fr.insarouen.iti.prog.sgbd.modele.Attribut;
import fr.insarouen.iti.prog.sgbd.modele.Table;
import fr.insarouen.iti.prog.sgbd.modele.Tuple;
import fr.insarouen.iti.prog.sgbd.modele.Type;
import fr.insarouen.iti.prog.sgbd.modele.Valeur;
import fr.insarouen.iti.prog.sgbd.modele.ValeurInt;
import fr.insarouen.iti.prog.sgbd.modele.ValeurVarchar;

import java.util.Arrays;

import org.junit.Before;
import org.junit.Test;

import static org.hamcrest.CoreMatchers.equalTo;
import static org.hamcrest.CoreMatchers.instanceOf;
import static org.hamcrest.MatcherAssert.assertThat;

public class TestOperande {

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
    public void test_constructeur_colonne() {
        Operande operande = new Operande("age");

        assertThat(operande.getType(), equalTo(Operande.TypeOperande.COLONNE));
        assertThat(operande.getNomColonne(), equalTo("age"));
    }

    @Test
    public void test_constructeur_nombre() {
        Operande operande = new Operande(new ValeurInt(20));

        assertThat(operande.getType(), equalTo(Operande.TypeOperande.NOMBRE));
    }

    @Test
    public void test_constructeur_chaine() {
        Operande operande = new Operande(new ValeurVarchar("Youssef"));

        assertThat(operande.getType(), equalTo(Operande.TypeOperande.CHAINE));
    }

    @Test
    public void test_evaluer_colonne_int_retourneValeurDuTuple() throws Exception {
        Operande operande = new Operande("age");

        Valeur resultat = operande.evaluer(this.tuple, this.table);

        assertThat(resultat, instanceOf(ValeurInt.class));
        assertThat(resultat, equalTo(new ValeurInt(20)));
    }

    @Test
    public void test_evaluer_colonne_varchar_retourneValeurDuTuple() throws Exception {
        Operande operande = new Operande("nom");

        Valeur resultat = operande.evaluer(this.tuple, this.table);

        assertThat(resultat, instanceOf(ValeurVarchar.class));
        assertThat(resultat, equalTo(new ValeurVarchar("Youssef")));
    }

    @Test
    public void test_evaluer_nombre_retourneValeurNombre() throws Exception {
        Operande operande = new Operande(new ValeurInt(18));

        Valeur resultat = operande.evaluer(this.tuple, this.table);

        assertThat(resultat, instanceOf(ValeurInt.class));
        assertThat(resultat, equalTo(new ValeurInt(18)));
    }

    @Test
    public void test_evaluer_chaine_retourneValeurChaine() throws Exception {
        Operande operande = new Operande(new ValeurVarchar("Batman"));

        Valeur resultat = operande.evaluer(this.tuple, this.table);

        assertThat(resultat, instanceOf(ValeurVarchar.class));
        assertThat(resultat, equalTo(new ValeurVarchar("Batman")));
    }

    @Test(expected = AttributInconnuException.class)
    public void test_evaluer_colonneInconnue_leveException() throws Exception {
        Operande operande = new Operande("taille");

        operande.evaluer(this.tuple, this.table);
    }
}