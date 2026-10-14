package fr.insarouen.iti.prog.aventure.elements;

import org.junit.Test;
import org.junit.BeforeClass;
import static org.junit.Assert.*;
import fr.insarouen.iti.prog.aventure.elements.Entite;
import fr.insarouen.iti.prog.aventure.Monde;
import fr.insarouen.iti.prog.aventure.NomDEntiteDejaUtiliseDansLeMondeException;

//javac -cp classes:classestest/:lib/junit4.jar:/usr/share/java/hamcrest-all.jar srctest/fr/insarouen/iti/prog/aventure/elements/TestEntite.java -d classestest
//java -cp classes:classestest/:lib/junit4.jar:/usr/share/java/hamcrest-all.jar org.junit.runner.JUnitCore TestEntite

public class TestEntite {

	public static Monde m;
	public static Monde russie;
	public static EntiteConcrete ant;
	public static EntiteConcrete ant2;

	@BeforeClass
	public static void avantTest() throws NomDEntiteDejaUtiliseDansLeMondeException {
		m = new Monde("Allemagne de l'ouest");
		ant = new EntiteConcrete("Hans", m);
		russie = new Monde("Allemagne de l'est");
		ant2 = new EntiteConcrete("Freud", russie);
	}

	@Test
	public void test_getNom() {
		assertEquals("Test getNom", ant.getNom(), "Hans");
	}

	@Test
	public void test_getNomN() {
		assertFalse("Test getNomN", ant.getNom().equals("Müll3r"));
	}

	@Test
	public void test_getMonde() {
		assertEquals("Test getMonde", ant.getMonde(), m);
	}

	@Test
	public void test_getMondeN() {
		assertFalse("Test getMondeN", ant.getNom().equals(russie));
	}

	@Test
	public void test_hashcode() throws NomDEntiteDejaUtiliseDansLeMondeException {
		assertFalse("Test hashcode", ant.hashCode() == ant2.hashCode());
	}

	@Test
	public void test_equals() throws NomDEntiteDejaUtiliseDansLeMondeException {
		assertFalse("Test equals", ant.equals(ant2));
	}

}

class EntiteConcrete extends Entite {
	public EntiteConcrete(String nom, Monde monde) throws NomDEntiteDejaUtiliseDansLeMondeException {
		super(nom, monde);
	}
}
