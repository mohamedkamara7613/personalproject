package fr.insarouen.iti.prog.sgbd.data;

import fr.insarouen.iti.prog.sgbd.modele.Attribut;
import fr.insarouen.iti.prog.sgbd.modele.BaseDeDonnees;
import fr.insarouen.iti.prog.sgbd.modele.Table;
import fr.insarouen.iti.prog.sgbd.modele.Tuple;
import fr.insarouen.iti.prog.sgbd.modele.Type;
import fr.insarouen.iti.prog.sgbd.modele.Valeur;
import fr.insarouen.iti.prog.sgbd.modele.ValeurInt;
import fr.insarouen.iti.prog.sgbd.modele.ValeurVarchar;

import java.io.File;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import org.junit.After;
import org.junit.Before;
import org.junit.Test;

import static org.hamcrest.CoreMatchers.equalTo;
import static org.hamcrest.MatcherAssert.assertThat;

public class TestGestionnaireStockage {

    private File fichierSauvegarde;
    private GestionnaireStockage stockage;

    @Before
    public void avantTest() throws Exception {
        this.fichierSauvegarde = File.createTempFile("sgbd-test-", ".data");
        this.fichierSauvegarde.delete();
        this.stockage = new GestionnaireStockage(
                new LecteurSerialisation(),
                new EnregistreurSerialisation());
    }

    @After
    public void apresTest() {
        if (this.fichierSauvegarde != null && this.fichierSauvegarde.exists()) {
            this.fichierSauvegarde.delete();
        }
    }

    @Test
    public void test_GestionnaireStockage_baseExiste_faux_siFichierAbsent() {
        assertThat(GestionnaireStockage.baseExiste(this.fichierSauvegarde.getAbsolutePath()), equalTo(false));
    }

    @Test
    public void test_GestionnaireStockage_sauvegarder_creeFichier() throws Exception {
        BaseDeDonnees db = new BaseDeDonnees("gotham");

        this.stockage.sauvegarder(db, this.fichierSauvegarde.getAbsolutePath());

        assertThat(GestionnaireStockage.baseExiste(this.fichierSauvegarde.getAbsolutePath()), equalTo(true));
    }

    @Test
    public void test_GestionnaireStockage_sauvegarderPuisCharger_conserveNomEtCompteurSerial() throws Exception {
        BaseDeDonnees db = construireBaseComplete();

        this.stockage.sauvegarder(db, this.fichierSauvegarde.getAbsolutePath());
        BaseDeDonnees chargee = this.stockage.charger(this.fichierSauvegarde.getAbsolutePath());

        assertThat(chargee.getNom(), equalTo("gotham"));
        assertThat(chargee.getCompteurSerial(), equalTo(2));
        assertThat(chargee.prochainSerial(), equalTo(3));
    }

    @Test
    public void test_GestionnaireStockage_sauvegarderPuisCharger_conserveTablesEtAttributs() throws Exception {
        BaseDeDonnees db = construireBaseComplete();

        this.stockage.sauvegarder(db, this.fichierSauvegarde.getAbsolutePath());
        BaseDeDonnees chargee = this.stockage.charger(this.fichierSauvegarde.getAbsolutePath());

        assertThat(chargee.tableExiste("heroes"), equalTo(true));
        assertThat(chargee.tableExiste("bases"), equalTo(true));

        Table heroes = chargee.getTable("heroes");
        assertThat(heroes.getNom(), equalTo("heroes"));
        assertThat(new ArrayList<>(heroes.getAttributs()), equalTo(Arrays.asList(
                new Attribut("id", Type.SERIAL),
                new Attribut("nom", Type.VARCHAR),
                new Attribut("puissance", Type.INT))));
    }

    @Test
    public void test_GestionnaireStockage_sauvegarderPuisCharger_conserveTuplesEtValeurs() throws Exception {
        BaseDeDonnees db = construireBaseComplete();

        this.stockage.sauvegarder(db, this.fichierSauvegarde.getAbsolutePath());
        BaseDeDonnees chargee = this.stockage.charger(this.fichierSauvegarde.getAbsolutePath());

        Table heroes = chargee.getTable("heroes");
        List<Tuple> tuples = heroes.getTuples();

        assertThat(tuples.size(), equalTo(2));
        assertThat(tuples.get(0).get(0), equalTo(new ValeurInt(1)));
        assertThat(tuples.get(0).get(1), equalTo(new ValeurVarchar("Batman")));
        assertThat(tuples.get(0).get(2), equalTo(new ValeurInt(100)));
        assertThat(tuples.get(1).get(0), equalTo(new ValeurInt(2)));
        assertThat(tuples.get(1).get(1), equalTo(new ValeurVarchar("Robin")));
        assertThat(tuples.get(1).get(2), equalTo(new ValeurInt(60)));
    }

    private BaseDeDonnees construireBaseComplete() throws Exception {
        BaseDeDonnees db = new BaseDeDonnees("gotham");

        Table heroes = new Table("heroes", Arrays.asList(
                new Attribut("id", Type.SERIAL),
                new Attribut("nom", Type.VARCHAR),
                new Attribut("puissance", Type.INT)));

        int idBatman = db.prochainSerial();
        int idRobin = db.prochainSerial();

        heroes.insererTuple(new Tuple(Arrays.asList(
                new ValeurInt(idBatman),
                new ValeurVarchar("Batman"),
                new ValeurInt(100))));

        heroes.insererTuple(new Tuple(Arrays.asList(
                new ValeurInt(idRobin),
                new ValeurVarchar("Robin"),
                new ValeurInt(60))));

        Table bases = new Table("bases", Arrays.asList(
                new Attribut("id", Type.INT),
                new Attribut("ville", Type.VARCHAR)));

        bases.insererTuple(new Tuple(Arrays.<Valeur>asList(
                new ValeurInt(1),
                new ValeurVarchar("Gotham"))));

        db.creerTable(heroes);
        db.creerTable(bases);

        return db;
    }
}
