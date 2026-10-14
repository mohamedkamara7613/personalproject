package fr.insarouen.iti.prog.aventure.elements.objets;
import fr.insarouen.iti.prog.aventure.Monde;
import fr.insarouen.iti.prog.aventure.NomDEntiteDejaUtiliseDansLeMondeException;

public class TestObjets {

	public static void main(String[] args) throws NomDEntiteDejaUtiliseDansLeMondeException {
		Monde m = new Monde("Armes -land");
		PiedDeBiche p = new PiedDeBiche(m);
		AutomaticRifle AK_47 = new AutomaticRifle("AK-47", m);
		System.out.println("Oki");
		
	}
}


