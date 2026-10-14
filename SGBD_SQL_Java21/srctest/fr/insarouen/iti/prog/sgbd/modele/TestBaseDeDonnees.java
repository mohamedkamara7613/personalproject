package fr.insarouen.iti.prog.sgbd.modele;

import org.junit.Before;
import org.junit.Test;

import static org.hamcrest.CoreMatchers.equalTo;
import static org.hamcrest.CoreMatchers.not;
import static org.hamcrest.CoreMatchers.hasItem;
import static org.hamcrest.MatcherAssert.assertThat;
import fr.insarouen.iti.prog.sgbd.exceptions.TableExistanteException;
import fr.insarouen.iti.prog.sgbd.exceptions.TableInconnueException;
import java.util.ArrayList;
import java.util.List;

public class TestBaseDeDonnees {

    private BaseDeDonnees db;
    private Table tableHeros;
    private Table tableBases;
    private Table tableGadgets;

    @Before
    public void avantTest() throws TableExistanteException {
        this.db = new BaseDeDonnees("mabase"); //base sur test_bat_creation
        // table heros
        List<Attribut> attributsHeros = new ArrayList<>();
        attributsHeros.add(new Attribut("id", Type.SERIAL));
        attributsHeros.add(new Attribut("nom", Type.VARCHAR));
        attributsHeros.add(new Attribut("alias", Type.VARCHAR));
        this.tableHeros = new Table("Heros", attributsHeros);
        //table bases
        List<Attribut> attributsBases = new ArrayList<>();
        attributsBases.add(new Attribut("id", Type.SERIAL));
        attributsBases.add(new Attribut("nom", Type.VARCHAR));
        attributsBases.add(new Attribut("ville", Type.VARCHAR));
        this.tableBases = new Table("bases", attributsBases);
        //table gadgets
        List<Attribut> attributsGadgets = new ArrayList<>();
        attributsGadgets.add(new Attribut("id", Type.SERIAL));
        attributsGadgets.add(new Attribut("nom", Type.VARCHAR));
        attributsGadgets.add(new Attribut("puissance", Type.INT));
        this.tableGadgets = new Table("gadgets", attributsGadgets);
    }

    @Test
    public void test_BD_getNom() {
        assertThat(this.db.getNom(), equalTo("mabase"));
    }

    @Test
    public void test_BD_tableExiste_faux() {
        assertThat(this.db.tableExiste("Heros"), equalTo(false));
    }

    @Test
    public void test_BD_tableExiste_vrai() throws TableExistanteException {
        this.db.creerTable(this.tableHeros);
        assertThat(this.db.tableExiste("Heros"), equalTo(true));
    }

    @Test
    public void test_BD_tableExiste_faux_apresSupression() throws TableExistanteException, TableInconnueException {
        this.db.creerTable(this.tableHeros);
        this.db.supprimerTable("Heros");
        assertThat(this.db.tableExiste("Heros"), equalTo(false));
    }

    @Test
    public void test_BD_creerTable_une() throws TableExistanteException {
        this.db.creerTable(this.tableHeros);
        assertThat(this.db.tableExiste("Heros"), equalTo(true));
    }

    @Test
    public void test_BD_creerTable_plusieurs() throws TableExistanteException {
        this.db.creerTable(this.tableHeros);
        this.db.creerTable(this.tableBases);
        this.db.creerTable(this.tableGadgets);
        assertThat(this.db.tableExiste("Heros"), equalTo(true));
        assertThat(this.db.tableExiste("bases"), equalTo(true));
        assertThat(this.db.tableExiste("gadgets"), equalTo(true));
    }

    @Test(expected = TableExistanteException.class)
    public void test_BD_creerTable_doublon() throws TableExistanteException {
        this.db.creerTable(this.tableHeros);
        this.db.creerTable(this.tableHeros);// comme dans test_duplicate.sql
    }

    @Test
    public void test_BD_supprimerTable_simple() throws TableExistanteException, TableInconnueException {
        this.db.creerTable(this.tableHeros);
        this.db.supprimerTable("Heros");
        assertThat(this.db.tableExiste("Heros"), equalTo(false));//comme dans test_drop.sql
    }

    @Test
    public void test_BD_supprimerTable_nAffectePasAutres() throws TableExistanteException, TableInconnueException {
        this.db.creerTable(this.tableHeros);
        this.db.creerTable(this.tableBases);
        this.db.supprimerTable("Heros");
        assertThat(this.db.tableExiste("bases"), equalTo(true));
    }

    @Test(expected = TableInconnueException.class)
    public void test_BD_supprimerTable_inconnue() throws TableInconnueException {
        this.db.supprimerTable("Heros");//comme dans test_drop.sql, DROP lève une erreur
    }

    @Test(expected = TableInconnueException.class)
    public void test_BD_supprimerTable_dejaSupprrimee()  throws TableExistanteException, TableInconnueException {
        this.db.creerTable(this.tableHeros);
        this.db.supprimerTable("Heros");
        this.db.supprimerTable("Heros");
    }

    @Test
    public void test_BD_getTable_simple() throws TableExistanteException, TableInconnueException {
        this.db.creerTable(this.tableHeros);
        assertThat(this.db.getTable("Heros"), equalTo(this.tableHeros));
    }

    @Test
    public void test_BD_getTable_bonneTable()throws TableExistanteException, TableInconnueException {
        this.db.creerTable(this.tableHeros);
        this.db.creerTable(this.tableBases);
        assertThat(this.db.getTable("bases"), equalTo(this.tableBases));
        assertThat(this.db.getTable("Heros"), not(equalTo(this.tableBases)));
    }

    @Test(expected = TableInconnueException.class)
    public void test_BD_getTable_inconnue() throws TableInconnueException {
        this.db.getTable("Heros");
    }

    @Test
    public void test_BD_listerTables_vide() {
        assertThat(this.db.listerTables().size(), equalTo(0));
    }

    @Test
    public void test_BD_listerTables_uneTable() throws TableExistanteException {
        this.db.creerTable(this.tableHeros);
        assertThat(this.db.listerTables().size(), equalTo(1));
        assertThat(this.db.listerTables(), hasItem("Heros"));
    }

    @Test
    public void test_BD_listerTables_plusieurs() throws TableExistanteException {
        this.db.creerTable(this.tableHeros);
        this.db.creerTable(this.tableBases);
        this.db.creerTable(this.tableGadgets);
        assertThat(this.db.listerTables().size(), equalTo(3));
        assertThat(this.db.listerTables(), hasItem("Heros"));
        assertThat(this.db.listerTables(), hasItem("bases"));
        assertThat(this.db.listerTables(), hasItem("gadgets"));
    }

    @Test
    public void test_BD_listerTables_apresSupression() throws TableExistanteException, TableInconnueException {
        this.db.creerTable(this.tableHeros);
        this.db.creerTable(this.tableBases);
        this.db.supprimerTable("Heros");
        assertThat(this.db.listerTables().size(), equalTo(1));
        assertThat(this.db.listerTables(), hasItem("bases"));
    }

    @Test(expected = UnsupportedOperationException.class)
    public void test_BD_listerTables_immutable() throws TableExistanteException {
        this.db.creerTable(this.tableHeros);
        this.db.listerTables().add("youssef");
    }


    @Test
    public void test_BD_prochainSerial_premierAppel() {
        assertThat(this.db.prochainSerial(), equalTo(1));
    }

    @Test// Commande inserte qui s'occupe du bon comportement des serial 
    public void test_BD_prochainSerial_incrementation() {
        this.db.prochainSerial();
        this.db.prochainSerial();
        assertThat(this.db.prochainSerial(), equalTo(3));
    }

        /** 
    // ============ TESTS PROJECTION ============
    // projection sur une colonne
    @Test
    public void test_Table_projection_uneColonne() throws AttributInconnuException {
        this.tableHeros.insererTuple(this.tuple1);
        this.tableHeros.insererTuple(this.tuple2);

        List<String> colonnes = new ArrayList<>();
        colonnes.add("nom");

        Table result = this.tableHeros.projection(colonnes);

        assertThat(result.getAttributs().size(), equalTo(1));
        assertThat(new java.util.ArrayList<>(result.getAttributs()).get(0), equalTo(this.attributNom));
}
    // projection sur plusieurs colonnes
    @Test
    public void test_Table_projection_plusieursColonnes() throws AttributInconnuException {
        this.tableHeros.insererTuple(this.tuple1);

        List<String> colonnes = new ArrayList<>();
        colonnes.add("nom");
        colonnes.add("puissance");

        Table result = this.tableHeros.projection(colonnes);

        assertThat(result.getAttributs().size(), equalTo(2));
        assertThat(new java.util.ArrayList<>(result.getAttributs()).get(0), equalTo(this.attributNom));
        assertThat(new java.util.ArrayList<>(result.getAttributs()).get(1), equalTo(this.attributPuissance));
    }


    @Test
    public void test_Table_projection_valeursTuples() throws AttributInconnuException {
        this.tableHeros.insererTuple(this.tuple1); // [1, "Batman", 100]
        this.tableHeros.insererTuple(this.tuple2); // [2, "Robin", 60]

        List<String> colonnes = new ArrayList<>();
        colonnes.add("nom");
        colonnes.add("puissance");

        Table result = this.tableHeros.projection(colonnes);

        // Vérification du nombre de tuples
        assertThat(result.getTuples().size(), equalTo(2));

        // Construction des tuples attendus
        List<Valeur> valeursAttendues1 = new ArrayList<>();
        valeursAttendues1.add(new ValeurVarchar("Batman"));
        valeursAttendues1.add(new ValeurInt(100));
        Tuple tupleAttendu1 = new Tuple(valeursAttendues1);

        List<Valeur> valeursAttendues2 = new ArrayList<>();
        valeursAttendues2.add(new ValeurVarchar("Robin"));
        valeursAttendues2.add(new ValeurInt(60));
        Tuple tupleAttendu2 = new Tuple(valeursAttendues2);

        assertThat(result.getTuples().get(0), equalTo(tupleAttendu1));
        assertThat(result.getTuples().get(1), equalTo(tupleAttendu2));
    }

    // Vérification de l'ordre des colonnes demandé
    @Test
    public void test_Table_projection_ordreColonnes() throws AttributInconnuException {
        this.tableHeros.insererTuple(this.tuple1); // [1, "Batman", 100]

        List<String> colonnes = new ArrayList<>();
        colonnes.add("puissance"); // inversé par rapport à la table originale
        colonnes.add("nom");

        Table result = this.tableHeros.projection(colonnes);

        assertThat(new java.util.ArrayList<>(result.getAttributs()).get(0), equalTo(this.attributPuissance));
        assertThat(new java.util.ArrayList<>(result.getAttributs()).get(1), equalTo(this.attributNom));
    }

    // Projection sur toutes les colonnes
    @Test
    public void test_Table_projection_toutesLesColonnes() throws AttributInconnuException {
        this.tableHeros.insererTuple(this.tuple1);

        List<String> colonnes = new ArrayList<>();
        colonnes.add("id");
        colonnes.add("nom");
        colonnes.add("puissance");

        Table result = this.tableHeros.projection(colonnes);

        assertThat(result.getAttributs().size(), equalTo(3));
        assertThat(result.getTuples().size(), equalTo(1));
    }

    @Test
    public void test_Table_projection_sanstuples() throws AttributInconnuException {
        List<String> colonnes = new ArrayList<>();
        colonnes.add("nom");

        Table result = this.tableHeros.projection(colonnes);

        assertThat(result.getAttributs().size(), equalTo(1));
        assertThat(result.getTuples().size(), equalTo(0));
    }

    // Colonne inconnue — exception attendue
    @Test(expected = AttributInconnuException.class)
    public void test_Table_projection_colonneInconnue() throws AttributInconnuException {
        List<String> colonnes = new ArrayList<>();
        colonnes.add("inconnu");

        this.tableHeros.projection(colonnes);
    }

    // Mélange colonne valide + invalide — exception attendue
    @Test(expected = AttributInconnuException.class)
    public void test_Table_projection_melange_valide_invalide() throws AttributInconnuException {
        List<String> colonnes = new ArrayList<>();
        colonnes.add("nom");
        colonnes.add("colonne_inexistante");

        this.tableHeros.projection(colonnes);
    }

        // ============ TESTS PRODUIT CARTESIEN ============

    // Vérification du nom de la nouvelle table
    @Test
    public void test_Table_produitCartesien_nom() {
        Table result = this.tableHeros.produitCartesien(this.tableVide);
        assertThat(result.getNom(), equalTo("heros_de_l_insa_vide"));
    }

    // Vérification de la fusion des attributs
    @Test
    public void test_Table_produitCartesien_attributs() {
        Attribut attributVille = new Attribut("ville", Type.VARCHAR);
        List<Attribut> attributsVille = new ArrayList<>();
        attributsVille.add(attributVille);
        Table tableVilles = new Table("villes", attributsVille);

        Table result = this.tableHeros.produitCartesien(tableVilles);

        assertThat(result.getAttributs().size(), equalTo(4)); // id, nom, puissance, ville
        assertThat(new java.util.ArrayList<>(result.getAttributs()).get(0), equalTo(new Attribut("heros_de_l_insa.id", Type.SERIAL)));
        assertThat(new java.util.ArrayList<>(result.getAttributs()).get(1), equalTo(new Attribut("heros_de_l_insa.nom", Type.VARCHAR)));
        assertThat(new java.util.ArrayList<>(result.getAttributs()).get(2), equalTo(new Attribut("heros_de_l_insa.puissance", Type.INT)));
        assertThat(new java.util.ArrayList<>(result.getAttributs()).get(3), equalTo(new Attribut("villes.ville", Type.VARCHAR)));
    }

    // Vérification du nombre de tuples (n × m)
    @Test
    public void test_Table_produitCartesien_nbTuples() {
        Attribut attributVille = new Attribut("ville", Type.VARCHAR);
        List<Attribut> attributsVille = new ArrayList<>();
        attributsVille.add(attributVille);
        Table tableVilles = new Table("villes", attributsVille);

        List<Valeur> valeursVille1 = new ArrayList<>();
        valeursVille1.add(new ValeurVarchar("Paris"));
        tableVilles.insererTuple(new Tuple(valeursVille1));

        List<Valeur> valeursVille2 = new ArrayList<>();
        valeursVille2.add(new ValeurVarchar("Londres"));
        tableVilles.insererTuple(new Tuple(valeursVille2));

        this.tableHeros.insererTuple(this.tuple1); // Batman
        this.tableHeros.insererTuple(this.tuple2); // Robin

        Table result = this.tableHeros.produitCartesien(tableVilles);

        assertThat(result.getTuples().size(), equalTo(4)); // 2 × 2
    }

    // Vérification de l'ordre et du contenu des tuples
    @Test
    public void test_Table_produitCartesien_contenuTuples() {
        Attribut attributVille = new Attribut("ville", Type.VARCHAR);
        List<Attribut> attributsVille = new ArrayList<>();
        attributsVille.add(attributVille);
        Table tableVilles = new Table("villes", attributsVille);

        List<Valeur> valeursVille1 = new ArrayList<>();
        valeursVille1.add(new ValeurVarchar("Paris"));
        tableVilles.insererTuple(new Tuple(valeursVille1));

        this.tableHeros.insererTuple(this.tuple1); // [1, Batman, 100]
        this.tableHeros.insererTuple(this.tuple2); // [2, Robin, 60]

        Table result = this.tableHeros.produitCartesien(tableVilles);

        // 2 tuples × 1 tuple = 2 tuples
        assertThat(result.getTuples().size(), equalTo(2));

        // Vérification du premier tuple fusionné [1, Batman, 100, Paris]
        assertThat(result.getTuples().get(0).getValeur(0).toString(), equalTo("1"));
        assertThat(result.getTuples().get(0).getValeur(1).toString(), equalTo("Batman"));
        assertThat(result.getTuples().get(0).getValeur(2).toString(), equalTo("100"));
        assertThat(result.getTuples().get(0).getValeur(3).toString(), equalTo("Paris"));

        // Vérification du second tuple fusionné [2, Robin, 60, Paris]
        assertThat(result.getTuples().get(1).getValeur(0).toString(), equalTo("2"));
        assertThat(result.getTuples().get(1).getValeur(1).toString(), equalTo("Robin"));
        assertThat(result.getTuples().get(1).getValeur(2).toString(), equalTo("60"));
        assertThat(result.getTuples().get(1).getValeur(3).toString(), equalTo("Paris"));
    }

    // Table vide à gauche → résultat vide
    @Test
    public void test_Table_produitCartesien_gaucheVide() {
        this.tableHeros.insererTuple(this.tuple1);

        Table result = this.tableVide.produitCartesien(this.tableHeros);

        assertThat(result.getTuples().size(), equalTo(0));
    }

    // Table vide à droite → résultat vide
    @Test
    public void test_Table_produitCartesien_droiteVide() {
        this.tableHeros.insererTuple(this.tuple1);

        Table result = this.tableHeros.produitCartesien(this.tableVide);

        assertThat(result.getTuples().size(), equalTo(0));
    }

    // Les deux tables vides → résultat vide
    @Test
    public void test_Table_produitCartesien_deuxTablesVides() {
        Table autreVide = new Table("autreVide", new ArrayList<>());

        Table result = this.tableVide.produitCartesien(autreVide);

        assertThat(result.getTuples().size(), equalTo(0));
        assertThat(result.getAttributs().size(), equalTo(0));
    }

    // Vérification que la table originale n'est pas modifiée
    @Test
    public void test_Table_produitCartesien_sansModificationOriginale() {
        this.tableHeros.insererTuple(this.tuple1);
        this.tableHeros.insererTuple(this.tuple2);

        Attribut attributVille = new Attribut("ville", Type.VARCHAR);
        List<Attribut> attributsVille = new ArrayList<>();
        attributsVille.add(attributVille);
        Table tableVilles = new Table("villes", attributsVille);
        tableVilles.insererTuple(new Tuple(List.of(new ValeurVarchar("Paris"))));

        this.tableHeros.produitCartesien(tableVilles);

        // La table originale ne doit pas avoir été modifiée
        assertThat(this.tableHeros.getTuples().size(), equalTo(2));
        assertThat(new java.util.ArrayList<>(this.tableHeros.getAttributs()).size(), equalTo(3));
    }
*/
}