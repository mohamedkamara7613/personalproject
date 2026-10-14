package fr.insarouen.iti.prog.aventure.elements.structure;

import static org.junit.Assert.*;
import org.junit.Test;
import org.junit.Before;

import fr.insarouen.iti.prog.aventure.Monde;
import fr.insarouen.iti.prog.aventure.elements.Etat;
import fr.insarouen.iti.prog.aventure.elements.vivants.Vivant;
import fr.insarouen.iti.prog.aventure.elements.objets.Coffre;
import fr.insarouen.iti.prog.aventure.elements.objets.PiedDeBiche;

import fr.insarouen.iti.prog.aventure.NomDEntiteDejaUtiliseDansLeMondeException;
import fr.insarouen.iti.prog.aventure.elements.ActivationImpossibleAvecObjetException;
import fr.insarouen.iti.prog.aventure.elements.ActivationImpossibleException;
import fr.insarouen.iti.prog.aventure.ITIAventureException;

public class TestPorte {

    public static Monde m;
    public static Piece p1;
    public static Piece p2;
    public static Porte porte1;
    public static Vivant viv;
    public static Coffre coffre;
    public static PiedDeBiche pdb;

    @Before
    public void avantTests() throws NomDEntiteDejaUtiliseDansLeMondeException, VivantAbsentDeLaPieceException {
        m = new Monde("Narnia");
        p1 = new Piece("Goulag", m);
        p2 = new Piece("Pentagone", m);
        coffre = new Coffre("Coffre magique", m);
        pdb = new PiedDeBiche("Pied de biche", m);
        p1.deposer(coffre);
        viv = new Vivant("Batman", m, 1000, 1000, p1, pdb);
        porte1 = new Porte("Porte en rose", m, p1, p2);
    }

    // -------------------------------------------------------
    // Tests sur l'état initial

    @Test
    public void test_getEtat_initial() {
        assertEquals("Test(Porte) getEtat: porte fermée par défaut", Etat.FERME, porte1.getEtat());
    }

    // -------------------------------------------------------
    // Tests sur getPieceAutreCote

    @Test
    public void test_getPieceAutreCote_depuisA() {
        assertEquals("Test(Porte) getPieceAutreCote depuis p1 -> p2", p2, porte1.getPieceAutreCote(p1));
    }

    @Test
    public void test_getPieceAutreCote_depuisB() {
        assertEquals("Test(Porte) getPieceAutreCote depuis p2 -> p1", p1, porte1.getPieceAutreCote(p2));
    }

    // -------------------------------------------------------
    // Tests sur activableAvec

    @Test
    public void test_activableAvec_coffre() {
        assertFalse("Test(Porte) activableAvec(Coffre): false", porte1.activableAvec(coffre));
    }

    @Test
    public void test_activableAvec_piedDeBiche() {
        assertFalse("Test(Porte) activableAvec(PiedDeBiche): false", porte1.activableAvec(pdb));
    }

    // -------------------------------------------------------

    @Test
    public void test_activer_FERME_vers_OUVERT() throws ActivationImpossibleException {
        porte1.activer();
        assertEquals("Test(Porte) activer: FERME -> OUVERT", Etat.OUVERT, porte1.getEtat());
    }

    @Test
    public void test_activer_OUVERT_vers_FERME() throws ActivationImpossibleException {
        porte1.activer(); // FERME -> OUVERT
        porte1.activer(); // OUVERT -> FERME
        assertEquals("Test(Porte) activer: OUVERT -> FERME", Etat.FERME, porte1.getEtat());
    }

    // -------------------------------------------------------

    @Test
    public void test_activerAvec_leveException() throws ActivationImpossibleException {
        try {
            porte1.activerAvec(pdb);
            fail("Echec : activerAvec devrait lever ActivationImpossibleAvecObjetException");
        } catch (ActivationImpossibleAvecObjetException e) {
            assertTrue("Test(Porte) activerAvec: exception levée", true);
        }
    }

    // -------------------------------------------------------
    // Tests sur l'intégration avec Piece (addPorte automatique)

    @Test
    public void test_piece_aLaPorte_p1() {
        assertTrue("Test(Porte) p1.aLaPorte(porte1)", p1.aLaPorte(porte1));
    }

    @Test
    public void test_piece_aLaPorte_p2() {
        assertTrue("Test(Porte) p2.aLaPorte(porte1)", p2.aLaPorte(porte1));
    }

    @Test
    public void test_piece_aLaPorte_string() {
        assertTrue("Test(Porte) p1.aLaPorte(string)", p1.aLaPorte("Porte en rose"));
    }

    // -------------------------------------------------------
    // Tests sur franchir (via Vivant)

    @Test
    public void test_franchir_PorteFermee() throws ITIAventureException {
        // La porte est FERME par défaut
        try {
            viv.franchir(porte1);
            fail("Echec : on ne devrait pas franchir une porte fermée");
        } catch (PorteFermeException e) {
            assertEquals("Test(Porte) franchir porte fermée: vivant reste en p1", p1, viv.getPiece());
        }
    }

    @Test
    public void test_franchir_ok() throws ITIAventureException {
        porte1.activer(); // FERME -> OUVERT
        viv.franchir(porte1);
        assertEquals("Test(Porte) franchir ok: vivant passe en p2", p2, viv.getPiece());
    }

    @Test
    public void test_franchir_string_ok() throws ITIAventureException {
        porte1.activer(); // FERME -> OUVERT
        viv.franchir("Porte en rose");
        assertEquals("Test(Porte) franchir(String) ok: vivant passe en p2", p2, viv.getPiece());
    }

    @Test
    public void test_franchir_PorteInexistante() throws ITIAventureException {
        porte1.activer(); // FERME -> OUVERT
        try {
            viv.franchir("Porte inexistante");
            fail("Echec : la porte n'existe pas dans la pièce");
        } catch (PorteInexistanteDansLaPieceException e) {
            assertEquals("Test(Porte) franchir porte inexistante: vivant reste en p1", p1, viv.getPiece());
        }
    }
}