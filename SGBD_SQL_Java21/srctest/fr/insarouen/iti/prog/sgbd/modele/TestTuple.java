package fr.insarouen.iti.prog.sgbd.modele;

import org.junit.Before;
import org.junit.Test;
import static org.hamcrest.CoreMatchers.equalTo;
import static org.hamcrest.MatcherAssert.assertThat;
import java.util.Arrays;
import java.util.ArrayList;
import java.util.List;

public class TestTuple {
    private Tuple tupleInt;
    private Tuple tupleVarchar;
    private Tuple tupleMixte;
    private Tuple tupleSingleton;
    private Tuple tupleVide;

    @Before
    public void avantTest(){
        List<Valeur> valeursInt = new ArrayList<>();
        valeursInt.add(new ValeurInt(5));
        valeursInt.add(new ValeurInt(10));
        valeursInt.add(new ValeurInt(15));
        this.tupleInt = new Tuple(valeursInt);

        List<Valeur> valeursVarchar = new ArrayList<>();
        valeursVarchar.add(new ValeurVarchar("Selasi"));
        valeursVarchar.add(new ValeurVarchar("Youssef"));
        valeursVarchar.add(new ValeurVarchar("Marwan"));
        this.tupleVarchar = new Tuple(valeursVarchar);

        List<Valeur> valeursMixte = new ArrayList<>();
        valeursMixte.add(new ValeurInt(42));
        valeursMixte.add(new ValeurVarchar("Test"));
        valeursMixte.add(new ValeurInt(100));
        this.tupleMixte = new Tuple(valeursMixte);

        List<Valeur> valeursSingleton = new ArrayList<>();
        valeursSingleton.add(new ValeurInt(7));
        this.tupleSingleton = new Tuple(valeursSingleton);

        this.tupleVide = new Tuple(new ArrayList<>());
    }

    @Test
    public void test_Tuple_Int_index0() {
        assertThat(this.tupleInt.get(0), equalTo(new ValeurInt(5)));
    }
    
    @Test
    public void test_Tuple_Int_index1() {
        assertThat(this.tupleInt.get(1), equalTo(new ValeurInt(10)));
    }
    
    @Test
    public void test_Tuple_Int_index2() {
        assertThat(this.tupleInt.get(2), equalTo(new ValeurInt(15)));
    }
    
    @Test
    public void test_Tuple_Int_size() {
        assertThat(this.tupleInt.size(), equalTo(3));
    }
    
    @Test
    public void test_Tuple_Int_getValeurs() {
        List<Valeur> valeurs = this.tupleInt;
        assertThat(valeurs.size(), equalTo(3));
        assertThat(valeurs.get(0), equalTo(new ValeurInt(5)));
        assertThat(valeurs.get(1), equalTo(new ValeurInt(10)));
        assertThat(valeurs.get(2), equalTo(new ValeurInt(15)));
    }

    @Test
    public void test_Tuple_Varchar_index0() {
        assertThat(this.tupleVarchar.get(0), equalTo(new ValeurVarchar("Selasi")));
    }
    
    @Test
    public void test_Tuple_Varchar_index1() {
        assertThat(this.tupleVarchar.get(1), equalTo(new ValeurVarchar("Youssef")));
    }
    
    @Test
    public void test_Tuple_Varchar_index2() {
        assertThat(this.tupleVarchar.get(2), equalTo(new ValeurVarchar("Marwan")));
    }
    
    @Test
    public void test_Tuple_Varchar_size() {
        assertThat(this.tupleVarchar.size(), equalTo(3));
    }
    
    @Test
    public void test_Tuple_Varchar_getValeurs() {
        List<Valeur> valeurs = this.tupleVarchar;
        assertThat(valeurs.size(), equalTo(3));
        assertThat(valeurs.get(0), equalTo(new ValeurVarchar("Selasi")));
        assertThat(valeurs.get(1), equalTo(new ValeurVarchar("Youssef")));
        assertThat(valeurs.get(2), equalTo(new ValeurVarchar("Marwan")));
    }

        @Test
    public void test_Tuple_Mixte_getValeur_int() {
        assertThat(this.tupleMixte.get(0), equalTo(new ValeurInt(42)));
    }
    
    @Test
    public void test_Tuple_Mixte_getValeur_varchar() {
        assertThat(this.tupleMixte.get(1), equalTo(new ValeurVarchar("Test")));
    }
    
    @Test
    public void test_Tuple_Mixte_getValeur_int2() {
        assertThat(this.tupleMixte.get(2), equalTo(new ValeurInt(100)));
    }
    
    @Test
    public void test_Tuple_Mixte_size() {
        assertThat(this.tupleMixte.size(), equalTo(3));
    }
    
    
    
    @Test
    public void test_Tuple_Singleton_size() {
        assertThat(this.tupleSingleton.size(), equalTo(1));
    }
    
    @Test
    public void test_Tuple_Singleton_getValeur() {
        assertThat(this.tupleSingleton.get(0), equalTo(new ValeurInt(7)));
    }
    
    @Test
    public void test_Tuple_Vide_size() {
        assertThat(this.tupleVide.size(), equalTo(0));
    }
    
    @Test
    public void test_Tuple_Vide_getValeurs() {
        assertThat(this.tupleVide.size(), equalTo(0));
    }

    @Test(expected = UnsupportedOperationException.class)
    public void test_Tuple_getValeurs_immuable(){
        this.tupleInt.add(new ValeurInt(10)); 
    }

    @Test
    public void test_Tuple_constructeur_copie(){
        List<Valeur> valeurs = new ArrayList<>();
        valeurs.add(new ValeurInt(1));
        Tuple t = new Tuple(valeurs);
        valeurs.add(new ValeurInt(2));
        assertThat(t.size(), equalTo(1));
    }
    @Test
    public void test_Tuple_Mixte_getValeurs() {
        List<Valeur> valeurs = this.tupleMixte;
        assertThat(valeurs.size(), equalTo(3));
}
}