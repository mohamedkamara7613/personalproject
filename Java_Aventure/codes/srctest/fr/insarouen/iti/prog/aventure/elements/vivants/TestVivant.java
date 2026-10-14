
package fr.insarouen.iti.prog.aventure.elements.vivants;

import org.junit.Test;
import org.junit.Before;
import static org.junit.Assert.*;
import java.util.Collection;
import java.util.HashMap;
import static org.hamcrest.Matchers.containsInAnyOrder;
import static org.hamcrest.MatcherAssert.assertThat;

import fr.insarouen.iti.prog.aventure.elements.vivants.Vivant;
import fr.insarouen.iti.prog.aventure.elements.structure.Piece;
import fr.insarouen.iti.prog.aventure.Monde;
import fr.insarouen.iti.prog.aventure.elements.Entite;
import fr.insarouen.iti.prog.aventure.elements.TableauDynamique;
import fr.insarouen.iti.prog.aventure.elements.objets.Objet;

import fr.insarouen.iti.prog.aventure.NomDEntiteDejaUtiliseDansLeMondeException;
import fr.insarouen.iti.prog.aventure.elements.structure.ObjetAbsentDeLaPieceException;
import fr.insarouen.iti.prog.aventure.elements.structure.VivantAbsentDeLaPieceException;
import fr.insarouen.iti.prog.aventure.elements.objets.ObjetNonDeplacableException;
import fr.insarouen.iti.prog.aventure.elements.vivants.ObjetNonPossedeParLeVivantException;
import fr.insarouen.iti.prog.aventure.ITIAventureException;
//javac -cp classes:classestest/:lib/junit4.jar:/usr/share/java/hamcrest-all.jar srctest/fr/insarouen/iti/prog/aventure/elements/vivants/TestVivant.java -d classestest
//java -cp classes:classestest/:lib/junit4.jar:/usr/share/java/hamcrest-all.jar org.junit.runner.JUnitCore TestVivant

public class TestVivant {
	public static Monde m;
	public static Piece p1;
	public static Piece p2;
	public static ObjetConcret obj1;
	public static ObjetConcret obj2;
	public static ObjetConcretNonD obj3;
	public static Vivant viv;

	@Before
	public void avantTests() throws NomDEntiteDejaUtiliseDansLeMondeException, VivantAbsentDeLaPieceException {
		m = new Monde("Narnia");
		p1 = new Piece("Goulag", m);
		p2 = new Piece("The Pentagon", m);
		obj1 = new ObjetConcret("cravache", m);
		obj2 = new ObjetConcret("clef", m);
		obj3 = new ObjetConcretNonD("enclume", m);
		p1.deposer(obj2);
		p1.deposer(obj3);
		viv = new Vivant("Orchidée", m, 1, 1000, p1, obj1);
	}

	@Test
	public void test_getPointVie() {
		assertEquals("Test getPointVie", viv.getPointVie(), 1);
	}

	@Test
	public void test_getPointVieN() {
		assertFalse("Test getPointVieN", viv.getPointVie() == -1);
	}

	@Test
	public void test_getPointForce() {
		assertEquals("Test getPointForce", viv.getPointForce(), 1000);
	}

	@Test
	public void test_getPointForceN() {
		assertFalse("Test getPointForceN", viv.getPointForce() == -1);
	}

	@Test
	public void test_getPiece() {
		assertEquals("Test getPiece", viv.getPiece(), p1);
	}

	@Test
	public void test_getPieceN() {
		assertFalse("Test getPieceN", viv.getPiece().equals(p2));
	}

	@Test
	public void test_setPiece() throws VivantAbsentDeLaPieceException {
		viv.setPiece(p2);
		assertEquals("Test setPiece", viv.getPiece(), p2);
	}

	@Test
	public void test_getObjet() {
		assertEquals("Test getObjet", obj1, viv.getObjet("cravache"));
	}

	@Test
	public void test_possede1() {
		assertTrue("Test possede(obj)", viv.possede(obj1));
	}

	@Test
	public void test_possede1N() {
		assertFalse("Test possede(obj)N", viv.possede(obj2));
	}

	@Test
	public void test_possede2() {
		assertTrue("Test possede(str)", viv.possede("cravache"));
	}

	@Test
	public void test_possede2N() {
		assertFalse("Test possede(str)N", viv.possede("fleur"));
	}

	@Test
	public void test_getObjets() {
		assertThat("Test getObjets", viv.getObjets(), containsInAnyOrder(obj1));
	}

	@Test
	public void test_prendre_OkObj() throws ITIAventureException {
		viv.prendre(obj2);
		assertTrue("Test prendre(obj) ok", viv.possede(obj2));
	}

	@Test
	public void test_prendre_OkStr() throws ITIAventureException {
		viv.prendre("clef");
		assertTrue("Test prendre(obj) ok", viv.possede("clef"));
	}

	@Test
	public void test_prendre_ND() throws ITIAventureException {
		try {
			viv.prendre(obj3);
			fail("Échec : Le joueur a pu prendre un objet non déplaçable (l'exception n'a pas été levée).");
		} catch (ObjetNonDeplacableException e) {
			assertFalse("L'inventaire ne devrait pas contenir obj3", viv.possede(obj3));
		}
	}

	@Test
	public void test_prendre_NP() throws ITIAventureException {
		try {
			viv.prendre("roadkill");
			fail("Échec : Il ne devrait pas être possible de prendre un objet absent de la pièce");
		} catch (ObjetAbsentDeLaPieceException e) {
			assertFalse("Test prendre non présent", viv.possede("roadkill"));
		}
	}

	@Test
	public void test_deposer1() throws ITIAventureException {
		viv.deposer(obj1);
		assertFalse("Test deposer(obj)", viv.possede(obj1));
		assertTrue("Test deposer(obj) piece", p1.contientObjet(obj1));
	}

	@Test
	public void test_deposer1N() throws ITIAventureException {
		try {
			viv.deposer(obj2);
			fail("Échec : Le joueur a pu déposer un objet qu'il ne possède pas (l'exception n'a pas été levée).");
		} catch (ObjetNonPossedeParLeVivantException e) {
			assertFalse("Test deposer(obj)N", viv.possede(obj2));
			assertTrue("Test deposer(obj)N piece", p1.contientObjet(obj2));
		}
	}

	@Test
	public void test_deposer2() throws ITIAventureException {
		viv.deposer("cravache");
		assertFalse("Test deposer(str)", viv.possede(obj1));
		assertTrue("Test deposer(str) piece", p1.contientObjet(obj1));
	}

}

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
