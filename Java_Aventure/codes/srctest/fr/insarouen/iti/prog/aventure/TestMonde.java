package fr.insarouen.iti.prog.aventure;

import org.junit.Test;
import org.junit.Before;
import static org.junit.Assert.*;
import java.util.Collection;

import fr.insarouen.iti.prog.aventure.elements.Entite;

public class TestMonde {

    public static Monde m1;
    public static Monde m2;
    public static Entite e1;
    public static Entite e2;
    public static Entite e3;

    @Before
    public void avantTests() throws NomDEntiteDejaUtiliseDansLeMondeException {
        m1 = new Monde("Tatooine");
        m2 = new Monde("Hoth");

        e1 = new EntiteConcrete("Luke", m1);
        e2 = new EntiteConcrete("Vador", m1);
        e3 = new EntiteConcrete("Yoda", m2);
    }

    @Test
    public void test_constructeur_et_getNom() {
        assertEquals("Test getNom() retourne Tatooine", "Tatooine", m1.getNom());
    }

    @Test
    public void test_getEntite() {
        assertEquals("Test getEntite(nom)", e1, m1.getEntite("Luke"));
        assertEquals("Test getEntite(nom)", e2, m1.getEntite("Vador"));
        assertNull("Test getEntite(nom) null si absent", m1.getEntite("Yoda"));
    }

    @Test
    public void test_getEntites() {
        Collection<Entite> entites = m1.getEntites();
        assertEquals("Test getEntites() taille", 2, entites.size());
        assertEquals("Test getEntites() contient e1", e1, m1.getEntite(e1.getNom()));
        assertEquals("Test getEntites() contient e2", e2, m1.getEntite(e2.getNom()));

    }

    @Test
    public void test_ajouter() throws EntiteDejaDansUnAutreMondeException, NomDEntiteDejaUtiliseDansLeMondeException {
        Entite e4 = new EntiteConcrete("Leia", m1);
        assertEquals("Test ajouter: taille", 3, m1.getEntites().size());
        assertEquals("Test ajouter: entite trouvee", e4, m1.getEntite("Leia"));
    }

    @Test
    public void test_ajouter_EntiteDejaDansUnAutreMondeException() {
        try {
            m1.ajouter(e3);
            fail("Echec : e3 est deja dans m2");
        } catch (EntiteDejaDansUnAutreMondeException e) {
            assertTrue("Test ajouter_EntiteDejaDansUnAutreMondeException", true);
        } catch (NomDEntiteDejaUtiliseDansLeMondeException e) {
            fail("Echec : Mauvaise exception");
        }
    }

    @Test
    public void test_ajouter_NomDEntiteDejaUtiliseDansLeMondeException() {
        try {
            Entite entitySansMonde = new EntiteConcrete("Luke", null);
            m1.ajouter(entitySansMonde);
            fail("Echec : Le nom Luke est deja utilise");
        } catch (NomDEntiteDejaUtiliseDansLeMondeException e) {
            assertTrue("Test ajouter_NomDEntiteDejaUtiliseDansLeMondeException", true);
        } catch (EntiteDejaDansUnAutreMondeException e) {
            fail("Echec : Mauvaise exception");
        }
    }

    @Test
    public void test_genererNom(){
        String nom = m1.genererNom("Hero_");
        String nom2 = m1.genererNom("Hero_");
        assertTrue("Test(Monde) test_genererNom : Le nom doit commencer par Hero :", nom.startsWith("Hero_"));
        assertNull("Test(Monde) test_genererNom : Le nom generer ne doit pas exister dans le monde :", m1.getEntite(nom));
        //System.out.println(String.format("%s et %s", nom, nom2));
    }
}

class EntiteConcrete extends Entite {
    public EntiteConcrete(String nom, Monde monde) throws NomDEntiteDejaUtiliseDansLeMondeException {
        super(nom, monde);
    }
}
