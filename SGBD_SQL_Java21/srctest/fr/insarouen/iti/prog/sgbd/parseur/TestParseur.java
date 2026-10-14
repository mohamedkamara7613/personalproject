package fr.insarouen.iti.prog.sgbd.parseur;

import org.junit.Before;
import org.junit.Test;

import static org.hamcrest.CoreMatchers.equalTo;
import static org.hamcrest.MatcherAssert.assertThat;

import fr.insarouen.iti.prog.sgbd.modele.BaseDeDonnees;
import fr.insarouen.iti.prog.sgbd.modele.Table;
import fr.insarouen.iti.prog.sgbd.modele.Type;
import fr.insarouen.iti.prog.sgbd.exceptions.TableInconnueException;

import java.io.ByteArrayInputStream;
import java.io.InputStream;
import java.nio.charset.StandardCharsets;

/**
 * Tests d'intégration du parseur JavaCC.
 *
 * Principe : on injecte une chaîne SQL dans le parseur via un InputStream,
 * on exécute les commandes, puis on vérifie l'état de la BaseDeDonnees.
 * Cela valide la chaîne complète : grammaire → logique métier → modèle.
 */
public class TestParseur {

    private BaseDeDonnees db;

    /**
     * Crée un parseur branché sur la chaîne SQL donnée et exécute
     * toutes les commandes qu'elle contient.
     */
    private void executer(String sql) throws ParseException {
        InputStream is = new ByteArrayInputStream(sql.getBytes(StandardCharsets.UTF_8));
        SGBDParser parser = new SGBDParser(is);
        parser.setDatabase(db);
        // Boucle jusqu'à la fin du flux (EOF détecté via TokenMgrError)
        while (true) {
            try {
                parser.Commande();
            } catch (ParseException e) {
                if (e.getMessage() != null && e.getMessage().contains("EOF")) break;
                throw e;
            } catch (TokenMgrError e) {
                if (e.getMessage() != null && e.getMessage().contains("EOF")) break;
                throw e;
            }
        }
    }

    @Before
    public void avantTest() {
        db = new BaseDeDonnees("testBase");
    }

    // -------------------------------------------------------------------------
    // CREATE TABLE
    // -------------------------------------------------------------------------

    @Test
    public void test_parseur_createTable_tableCreee() throws Exception {
        executer("CREATE TABLE heroes (id SERIAL, nom VARCHAR, puissance INT);");
        assertThat(db.tableExiste("heroes"), equalTo(true));
    }

    @Test
    public void test_parseur_createTable_schema_nbAttributs() throws Exception {
        executer("CREATE TABLE heroes (id SERIAL, nom VARCHAR, puissance INT);");
        Table t = db.getTable("heroes");
        assertThat(t.getAttributs().size(), equalTo(3));
    }

    @Test
    public void test_parseur_createTable_schema_types() throws Exception {
        executer("CREATE TABLE heroes (id SERIAL, nom VARCHAR, puissance INT);");
        Table t = db.getTable("heroes");
        assertThat(new java.util.ArrayList<>(t.getAttributs()).get(0).type(), equalTo(Type.SERIAL));
        assertThat(new java.util.ArrayList<>(t.getAttributs()).get(1).type(), equalTo(Type.VARCHAR));
        assertThat(new java.util.ArrayList<>(t.getAttributs()).get(2).type(), equalTo(Type.INT));
    }

    @Test
    public void test_parseur_createTable_insensibleCasse() throws Exception {
        executer("create table Heroes (id serial, nom varchar);");
        assertThat(db.tableExiste("heroes"), equalTo(true));
    }

    @Test
    public void test_parseur_createTable_doublon_neLevesPas() throws Exception {
        // Le parseur gère l'erreur en interne (message sur stderr) sans planter
        executer("CREATE TABLE heroes (id SERIAL);");
        executer("CREATE TABLE heroes (id SERIAL);"); // doublon : erreur loggée, pas d'exception
        assertThat(db.tableExiste("heroes"), equalTo(true));
    }

    // -------------------------------------------------------------------------
    // DROP TABLE
    // -------------------------------------------------------------------------

    @Test
    public void test_parseur_dropTable_tableDisparait() throws Exception {
        executer("CREATE TABLE gadgets (id SERIAL, nom VARCHAR);");
        executer("DROP TABLE gadgets;");
        assertThat(db.tableExiste("gadgets"), equalTo(false));
    }

    @Test
    public void test_parseur_dropTable_inconnue_neLevesPas() throws Exception {
        // Table inexistante : erreur loggée en interne, pas d'exception parseur
        executer("DROP TABLE tableFantome;");
        // Pas d'exception == succès du test
    }

    // -------------------------------------------------------------------------
    // INSERT INTO
    // -------------------------------------------------------------------------

    @Test
    public void test_parseur_insert_uneTuple() throws Exception {
        executer("CREATE TABLE heroes (id SERIAL, nom VARCHAR, puissance INT);");
        executer("INSERT INTO heroes (nom, puissance) VALUES (\"Batman\", 100);");
        Table t = db.getTable("heroes");
        assertThat(t.getTuples().size(), equalTo(1));
    }

    @Test
    public void test_parseur_insert_serial_autoIncrement() throws Exception {
        executer("CREATE TABLE heroes (id SERIAL, nom VARCHAR);");
        executer("INSERT INTO heroes (nom) VALUES (\"Batman\");");
        executer("INSERT INTO heroes (nom) VALUES (\"Robin\");");
        Table t = db.getTable("heroes");
        // id doit être 1 pour Batman et 2 pour Robin
        assertThat((Integer) t.getTuples().get(0).get(0).getDonnee(), equalTo(1));
        assertThat((Integer) t.getTuples().get(1).get(0).getDonnee(), equalTo(2));
    }

    @Test
    public void test_parseur_insert_valeur_varchar() throws Exception {
        executer("CREATE TABLE heroes (id SERIAL, nom VARCHAR);");
        executer("INSERT INTO heroes (nom) VALUES (\"Batgirl\");");
        Table t = db.getTable("heroes");
        assertThat(t.getTuples().get(0).get(1).getDonnee(), equalTo("Batgirl"));
    }

    @Test
    public void test_parseur_insert_plusieursLignes() throws Exception {
        executer("CREATE TABLE heroes (id SERIAL, nom VARCHAR, puissance INT);\n" +
                 "INSERT INTO heroes (nom, puissance) VALUES (\"Batman\", 100);\n" +
                 "INSERT INTO heroes (nom, puissance) VALUES (\"Robin\", 60);\n" +
                 "INSERT INTO heroes (nom, puissance) VALUES (\"Batgirl\", 80);");
        assertThat(db.getTable("heroes").getTuples().size(), equalTo(3));
    }

    // -------------------------------------------------------------------------
    // DELETE FROM (sans WHERE)
    // -------------------------------------------------------------------------

    @Test
    public void test_parseur_delete_videTable() throws Exception {
        executer("CREATE TABLE heroes (id SERIAL, nom VARCHAR);\n" +
                 "INSERT INTO heroes (nom) VALUES (\"Batman\");\n" +
                 "INSERT INTO heroes (nom) VALUES (\"Robin\");\n" +
                 "DELETE FROM heroes;");
        assertThat(db.getTable("heroes").getTuples().size(), equalTo(0));
    }

    @Test
    public void test_parseur_delete_tableVideRestante() throws Exception {
        executer("CREATE TABLE heroes (id SERIAL, nom VARCHAR);\n" +
                 "DELETE FROM heroes;"); // aucune ligne — ne doit pas planter
        assertThat(db.getTable("heroes").getTuples().size(), equalTo(0));
    }

    // -------------------------------------------------------------------------
    // Plusieurs commandes enchaînées
    // -------------------------------------------------------------------------

    @Test
    public void test_parseur_scenarioComplet() throws Exception {
        executer("CREATE TABLE bases (id SERIAL, nom VARCHAR);\n" +
                 "CREATE TABLE heroes (id SERIAL, nom VARCHAR, base_id INT);\n" +
                 "INSERT INTO bases (nom) VALUES (\"BureauInfo\");\n" +
                 "INSERT INTO heroes (nom, base_id) VALUES (\"Batman\", 1);\n" +
                 "INSERT INTO heroes (nom, base_id) VALUES (\"Robin\", 1);\n" +
                 "DROP TABLE bases;");
        assertThat(db.tableExiste("bases"),  equalTo(false));
        assertThat(db.tableExiste("heroes"), equalTo(true));
        assertThat(db.getTable("heroes").getTuples().size(), equalTo(2));
        assertThat(db.listerTables().size(), equalTo(1));
    }

    // -------------------------------------------------------------------------
    // Les Alias 
    // -------------------------------------------------------------------------
    @Test
    public void test_parseur_reconnaisance_alias_guillements_simple() throws Exception {
        executer("CREATE TABLE employes (id INT, nom VARCHAR, manager_id INT);");
        executer("INSERT INTO employes (id, nom, manager_id) VALUES (1, 'Bruce Wayne', 0);");
        executer("INSERT INTO employes (id, nom, manager_id) VALUES (2, 'Alfred Pennyworth', 1);");
        executer("INSERT INTO employes (id, nom, manager_id) VALUES (4, 'Jason Todd', 3);");
        executer("INSERT INTO employes (id, nom, manager_id) VALUES (3, 'Dick Grayson', 1);");
        executer("SELECT E.nom, M.nom FROM employes E, employes M WHERE E.manager_id = M.id;");
        executer("SELECT E.nom, M.nom FROM employes AS E, employes AS M WHERE E.manager_id = M.id;");
        executer("EXIT;");
    }
}
