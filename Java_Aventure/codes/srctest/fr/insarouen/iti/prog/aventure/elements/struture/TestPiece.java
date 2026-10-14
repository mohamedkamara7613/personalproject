package fr.insarouen.iti.prog.aventure.elements.structure;

import static org.junit.Assert.*;
import org.junit.Test;
import org.junit.Before;
import static org.hamcrest.MatcherAssert.assertThat;
import static org.hamcrest.CoreMatchers.is;
import java.util.Collection;
import static org.hamcrest.Matchers.containsInAnyOrder;

import fr.insarouen.iti.prog.aventure.elements.vivants.Vivant;
import fr.insarouen.iti.prog.aventure.elements.structure.Piece;
import fr.insarouen.iti.prog.aventure.Monde;
import fr.insarouen.iti.prog.aventure.elements.objets.Objet;

import fr.insarouen.iti.prog.aventure.NomDEntiteDejaUtiliseDansLeMondeException;
import fr.insarouen.iti.prog.aventure.elements.objets.ObjetNonDeplacableException;
import fr.insarouen.iti.prog.aventure.elements.structure.ObjetAbsentDeLaPieceException;
import fr.insarouen.iti.prog.aventure.elements.structure.VivantAbsentDeLaPieceException;
import fr.insarouen.iti.prog.aventure.ITIAventureException;

// ------------------------------------------------------------------------------------

public class TestPiece {
    public static Monde m;
    public static Piece p;
    public static ObjetConcret obj1;
    public static ObjetConcret obj2;
    public static ObjetConcretNonD obj3;
    public static Vivant viv1;
    public static Vivant viv2;

    @Before
    public void avantTests() throws NomDEntiteDejaUtiliseDansLeMondeException, VivantAbsentDeLaPieceException {
        m = new Monde("Narnia");
        p = new Piece("Goulag", m);
        obj1 = new ObjetConcret("cravache", m);
        obj2 = new ObjetConcret("Plume", m);
        obj3 = new ObjetConcretNonD("Marteau de Thor", m);
        p.deposer(obj1);
        viv1 = new Vivant("Batman", m, 1000, 1000, p, obj2);
        viv2 = new Vivant("Orchidee", m, 1, 1000, p, obj1);
        p.entrer(viv2);

    }

    @Test
    public void test_contient() {
        assertTrue("Test(Piece) contient", p.contientObjet(obj1));
    }

    @Test
    public void test_contientN() {
        assertFalse("Test(Piece) contientN", p.contientObjet(obj2));
    }

    @Test
    public void test_contientString() {
        assertTrue("Test(Piece) contientString", p.contientObjet("cravache"));
    }

    @Test
    public void test_contientStringN() {
        assertFalse("Test(Piece) contientStringN", p.contientObjet("Plume"));
    }

    @Test
    public void test_deposer() {
        p.deposer(obj3);
        assertTrue("Test(Piece) deposer", p.contientObjet(obj3));
    }

    @Test

    public void test_deposerN() {
        assertFalse("Test(Piece) deposerN", p.contientObjet(obj3));
    }

    @Test
    public void test_retirer() throws ITIAventureException {
        p.deposer(obj2);
        p.retirer(obj2);
        assertFalse("Test(Piece) retirer", p.contientObjet(obj2));
    }

    @Test
    public void test_retirerString() throws ITIAventureException {
        p.deposer(obj2);
        p.retirer("Plume");
        assertFalse("Test(Piece) retirerString", p.contientObjet(obj2));
    }

    @Test
    public void test_retirer_Objet_Absent() throws ITIAventureException {
        try {
            p.retirer(obj2);
            fail("Echec : on n'est pas censé pouvoir retirer un objet absent de la piece");
        } catch (ObjetAbsentDeLaPieceException e) {
            assertFalse("Test(Piece) retirer_Objet_Absent", p.contientObjet(obj2));
        }
    }

    @Test
    public void test_retirer_Objet_NonDeplacable() throws ITIAventureException {
        try {
            p.deposer(obj3);
            p.retirer(obj3);
            fail("Echec : on n'est pas censé pouvoir retirer un objet non deplacable");
        } catch (ObjetNonDeplacableException e) {
            assertTrue("Test(Piece) retirer_Objet_NonDeplacable", p.contientObjet(obj3));
        }
    }

    @Test
    public void test_retirer_Objet_Absent_String() throws ITIAventureException {
        try {
            p.retirer("Plume");
            fail("Echec : on n'est pas censé pouvoir retirer un objet absent de la piece");
        } catch (ObjetAbsentDeLaPieceException e) {
            assertFalse("Test(Piece) retirer_Objet_Absent_String", p.contientObjet(obj2));
        }
    }

    @Test
    public void test_retirer_Objet_NonDeplacable_String() throws ITIAventureException {
        try {
            p.deposer(obj3);
            p.retirer("Marteau de Thor");
            fail("Echec : on n'est pas censé pouvoir retirer un objet non deplacable");
        } catch (ObjetNonDeplacableException e) {
            assertTrue("Test(Piece) retirer_Objet_NonDeplacable_String : ", p.contientObjet(obj3));
        }
    }

    @Test
    public void test_contientVivant() throws ITIAventureException {
        assertTrue("Test(Piece) contientVivant : ", p.contientVivant(viv2));
    }

    @Test
    public void test_contientVivantN() throws ITIAventureException {
        p.sortir(viv1);
        assertFalse("Test(Piece) contientVivantN : ", p.contientVivant(viv1));
    }

    @Test
    public void test_contientVivant_String() throws ITIAventureException {
        assertTrue("Test(Piece) contientVivant : ", p.contientVivant("Orchidee"));
    }

    @Test
    public void test_contientVivantN_String() throws ITIAventureException {
        p.sortir("Batman");
        assertFalse("Test(Piece) contientVivantN : ", p.contientVivant("Batman"));
    }

    @Test
    public void test_entrer() throws ITIAventureException {
        p.entrer(viv1);
        assertTrue("Test(Piece) entrer : ", p.contientVivant(viv1));
    }

    @Test
    public void test_sortir() throws ITIAventureException {
        p.entrer(viv1);
        p.sortir(viv1);
        assertFalse("Test(Piece) sortir : ", p.contientVivant(viv1));
    }

    @Test
    public void test_sortir_String() throws ITIAventureException {
        p.entrer(viv1);
        p.sortir("Batman");
        assertFalse("Test(Piece) sortir : ", p.contientVivant(viv1));
    }

    @Test
    public void test_sortir_VivantAbsent() throws ITIAventureException {
        p.sortir(viv1);
        try {
            p.sortir(viv1);
            fail("Erreur : On ne peut pas sortir un vivant qui n'est pas dans la piece");
        } catch (VivantAbsentDeLaPieceException e) {
            assertFalse("Test(Piece) sortir_VivantAbsent : ", p.contientVivant(viv1));
        }
    }

    @Test
    public void test_sortir_VivantAbsent_String() throws ITIAventureException {
        p.sortir("Batman");
        try {
            p.sortir("Batman");
            fail("Erreur : On ne peut pas sortir un vivant qui n'est pas dans la piece");
        } catch (VivantAbsentDeLaPieceException | ArrayIndexOutOfBoundsException e) {
            assertFalse("Test(Piece) sortir_VivantAbsent : ", p.contientVivant("Batman"));
        }
    }

    @Test
    public void test_getVivants() {
        Collection<Vivant> vivants = p.getVivants();
        assertEquals("Test(Piece) getVivants : longueur", 2, vivants.size());
        assertThat("Test(Piece) getVivants : element 0", vivants, containsInAnyOrder(viv1, viv2));
    }

    @Test
    public void test_getObjets() {
        Collection<Objet> objets = p.getObjets();
        assertEquals("Test(Piece) getObjets : longueur", 1, objets.size());
        assertThat("Test(Piece) getObjets : ", objets, containsInAnyOrder(obj1));
    }
}

// ------------------------------------------------------------------------------------
class ObjetConcret extends Objet {
    public ObjetConcret(String nom, Monde monde) throws NomDEntiteDejaUtiliseDansLeMondeException {
        super(nom, monde);
    }

    public boolean estDeplacable() {
        return true;
    }
}

class ObjetConcretNonD extends Objet {
    public ObjetConcretNonD(String nom, Monde monde) throws NomDEntiteDejaUtiliseDansLeMondeException {
        super(nom, monde);
    }

    public boolean estDeplacable() {
        return false;
    }
}