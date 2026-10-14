package fr.insarouen.iti.prog.sgbd.modele;
 
import org.junit.Before;
import org.junit.Test;
 
import static org.hamcrest.CoreMatchers.equalTo;
import static org.hamcrest.CoreMatchers.not;
import static org.hamcrest.MatcherAssert.assertThat;
 
import fr.insarouen.iti.prog.sgbd.exceptions.AttributInconnuException;
import fr.insarouen.iti.prog.sgbd.exceptions.TupleInconnuException;
 
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;
 
public class TestTable {
    private Table tableHeros;
    private Table tableVide;
    private Attribut attributId;
    private Attribut attributNom;
    private Attribut attributPuissance;
    private Tuple tuple1;
    private Tuple tuple2;
    private Tuple tuple3;


    @Before
    public void avantTest(){
        this.attributId = new Attribut("id", Type.SERIAL); 
        this.attributNom = new Attribut("nom", Type.VARCHAR); 
        this.attributPuissance = new Attribut("puissance",Type.INT);

        List<Attribut> attributs = new ArrayList<>();
        attributs.add(this.attributId);
        attributs.add(this.attributNom);
        attributs.add(this.attributPuissance);
        this.tableHeros = new Table("heros_de_l_insa", attributs); 
        
        this.tableVide = new Table("vide", new ArrayList<>()); 

        // Tuples
        List<Valeur> valeurs1 = new ArrayList<>();
        valeurs1.add(new ValeurInt(1));
        valeurs1.add(new ValeurVarchar("Batman"));
        valeurs1.add(new ValeurInt(100));
        this.tuple1 = new Tuple(valeurs1);

        List<Valeur> valeurs2 = new ArrayList<>();
        valeurs2.add(new ValeurInt(2));
        valeurs2.add(new ValeurVarchar("Robin"));
        valeurs2.add(new ValeurInt(60));
        this.tuple2 = new Tuple(valeurs2);

        List<Valeur> valeurs3 = new ArrayList<>();
        valeurs3.add(new ValeurInt(3));
        valeurs3.add(new ValeurVarchar("Batgirl"));
        valeurs3.add(new ValeurInt(80));
        this.tuple3 = new Tuple(valeurs3);
    }
    //getters
    @Test
    public void test_Table_getNom(){
        assertThat(this.tableHeros.getNom(), equalTo("heros_de_l_insa"));
    }

    @Test
    public void test_Table_getNom_vide(){
        assertThat(this.tableVide.getNom(), equalTo("vide"));
    }

    @Test
    public void test_Table_getAttributs_taille() {
        assertThat(new java.util.ArrayList<>(this.tableHeros.getAttributs()).size(), equalTo(3));
    }

    @Test
    public void test_Table_getAttributs(){
        List<Attribut> attributs = new java.util.ArrayList<>(this.tableHeros.getAttributs());
        assertThat(attributs.get(0), equalTo(this.attributId));
        assertThat(attributs.get(1), equalTo(this.attributNom));
        assertThat(attributs.get(2), equalTo(this.attributPuissance));
    }

    @Test
    public void test_Table_getAttributs_vide(){
        assertThat(this.tableVide.getAttributs().size(), equalTo(0));
    }

    @Test(expected = UnsupportedOperationException.class)
    public void test_Table_getAttributs_immutable() {
        this.tableHeros.getAttributs().add(new Attribut("test", Type.INT));
    }

        @Test
    public void test_Table_getAttribut_id() throws AttributInconnuException {
        assertThat(this.tableHeros.getAttribut("id"), equalTo(this.attributId));
    }

    @Test
    public void test_Table_getAttribut_nom() throws AttributInconnuException {
        assertThat(this.tableHeros.getAttribut("nom"), equalTo(this.attributNom));
    }
 
    @Test
    public void test_Table_getAttribut_puissance() throws AttributInconnuException {
        assertThat(this.tableHeros.getAttribut("puissance"), equalTo(this.attributPuissance));
    }
 
    @Test(expected = AttributInconnuException.class)
    public void test_Table_getAttribut_inconnu() throws AttributInconnuException {
        this.tableHeros.getAttribut("test");
    }

    @Test
    public void test_Table_getTuples_tableVide() {
        assertThat(this.tableHeros.getTuples().size(), equalTo(0));
    }
 
    @Test(expected = UnsupportedOperationException.class)
    public void test_Table_getTuples_immutable() {
        this.tableHeros.getTuples().add(this.tuple1);
    }
    // insererTuples
    @Test
    public void test_Table_insererTuple_taille(){
        this.tableHeros.insererTuple(this.tuple1);
        assertThat(this.tableHeros.getTuples().size(),equalTo(1)); 
    }

    @Test
    public void test_Table_insererTuple_contenu(){
        this.tableHeros.insererTuple(this.tuple1);
        assertThat(this.tableHeros.getTuples().get(0), equalTo(this.tuple1)); 
    }

    @Test
    public void test_Table_insererTuples(){
        this.tableHeros.insererTuple(this.tuple1);
        this.tableHeros.insererTuple(this.tuple2);
        this.tableHeros.insererTuple(this.tuple3);
        assertThat(this.tableHeros.getTuples().size(), equalTo(3)); 
    }

    @Test
    public void test_Table_insererTuple_ordre() {
        this.tableHeros.insererTuple(this.tuple1);
        this.tableHeros.insererTuple(this.tuple2);
        assertThat(this.tableHeros.getTuples().get(0), equalTo(this.tuple1));
        assertThat(this.tableHeros.getTuples().get(1), equalTo(this.tuple2));
    }
    //suppression

    @Test
    public void test_Table_supprimerTuples_un() throws TupleInconnuException {
        this.tableHeros.insererTuple(this.tuple1);
        this.tableHeros.insererTuple(this.tuple2);
        this.tableHeros.insererTuple(this.tuple3);
 
        List<Tuple> aSupprimer = new ArrayList<>();
        aSupprimer.add(this.tuple2);
 
        int nbSupprimes = this.tableHeros.supprimerTuples(aSupprimer);
 
        assertThat(nbSupprimes, equalTo(1));
        assertThat(this.tableHeros.getTuples().size(), equalTo(2));
        assertThat(this.tableHeros.getTuples().contains(this.tuple2), equalTo(false));
    }

    @Test
    public void test_Table_supprimerTuples_plusieurs() throws TupleInconnuException {
        this.tableHeros.insererTuple(this.tuple1);
        this.tableHeros.insererTuple(this.tuple2);
        this.tableHeros.insererTuple(this.tuple3);
 
        List<Tuple> aSupprimer = new ArrayList<>();
        aSupprimer.add(this.tuple2);
        aSupprimer.add(this.tuple3);
 
        int nbSupprimes = this.tableHeros.supprimerTuples(aSupprimer);
 
        assertThat(nbSupprimes, equalTo(2));
        assertThat(this.tableHeros.getTuples().size(), equalTo(1));
        assertThat(this.tableHeros.getTuples().contains(this.tuple2), equalTo(false));
        assertThat(this.tableHeros.getTuples().contains(this.tuple3), equalTo(false));
    }

    @Test
    public void test_Table_supprimerTuples_tous() throws TupleInconnuException {
        this.tableHeros.insererTuple(this.tuple1);
        this.tableHeros.insererTuple(this.tuple2);
        this.tableHeros.insererTuple(this.tuple3);
 
        List<Tuple> aSupprimer = new ArrayList<>();
        aSupprimer.add(this.tuple1);
        aSupprimer.add(this.tuple2);
        aSupprimer.add(this.tuple3);
 
        int nbSupprimes = this.tableHeros.supprimerTuples(aSupprimer);
 
        assertThat(nbSupprimes, equalTo(3));
        assertThat(this.tableHeros.getTuples().size(), equalTo(0));
    }

    @Test(expected = TupleInconnuException.class)
    public void test_Table_supprimerTuples_Inexistant() throws TupleInconnuException {
        this.tableHeros.insererTuple(this.tuple1);
        List<Tuple> aSupprimer = new ArrayList<>();
        aSupprimer.add(this.tuple2);
        this.tableHeros.supprimerTuples(aSupprimer);
    }

    @Test 
    public void test_Table_enommerAvecPrefixe() throws TupleInconnuException {
        Table test = this.tableHeros.renommerAvecPrefixe("test");
        List<Attribut> lesAttributs = new ArrayList<>(test.getAttributs()); 
        List<String> nomAttributs = lesAttributs.stream()
                                                .map(a -> a.nom())
                                                .collect(Collectors.toList());

        assertThat(nomAttributs.contains("test.id"), equalTo(true));
        assertThat(nomAttributs.contains("test.puissance"), equalTo(true));
        assertThat(nomAttributs.contains("test.nom"), equalTo(true));
        assertThat(lesAttributs.size(), equalTo(3));
    }

    

}