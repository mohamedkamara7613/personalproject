
import fr.insarouen.iti.prog.aventure.Monde;
import fr.insarouen.iti.prog.aventure.ITIAventureException;
import fr.insarouen.iti.prog.aventure.NomDEntiteDejaUtiliseDansLeMondeException;
import fr.insarouen.iti.prog.aventure.EntiteDejaDansUnAutreMondeException;
import fr.insarouen.iti.prog.aventure.elements.Entite;

public class TestMondeEntiteException {


    public static void main(String[] args) throws ITIAventureException {
	Monde m1 = new Monde("Le monde impitoyable d'ITI");
	Monde m2 = new Monde("INSA");

	// avec une classe EntiteTest (choix 1)
	Entite e1 = new EntiteTest("Nicolat", m1);
	System.out.println(String.format("L'entite %s",e1));
	Entite e2 = new EntiteTest("Nicolad", m2);

	System.out.println("--- Test1  NomDEntiteDejaUtiliseDansLeMondeException ---");
	try {
	    new EntiteTest("Nicolat", m1);
	} catch(NomDEntiteDejaUtiliseDansLeMondeException ex) {
	    ex.printStackTrace();
	}

	System.out.println("--- Test2 NomDEntiteDejaUtiliseDansLeMondeException ---");
	try {
	    m1.ajouter(e1);
	} catch(NomDEntiteDejaUtiliseDansLeMondeException ex) {
	    ex.printStackTrace();
	}

	System.out.println("--- Test  EntiteDejaDansUnAutreMondeException ---");
	try {
	    m1.ajouter(e2);
	} catch(EntiteDejaDansUnAutreMondeException ex) {
	    ex.printStackTrace();
	}




	// System.out.println(String.format("Egalité e1.equals(e2):%b",e1.equals(e2)));
	// System.out.println(String.format("Egalité e1.equals(e3):%b",e1.equals(e3)));
	// System.out.println(String.format("Egalité e1.equals(e1):%b",e1.equals(e1)));

	System.out.println(m1);

	// avec des classes anonymes (choix 2)
	// Entite e42 = new Entite("Nicolas", m) {};
	// Entite e43 = new Entite("Nicolas", m) {};
	// System.out.println(String.format("Egalité e42.equals(e43):%b",e42.equals(e43)));
	// System.out.println(m);

    }

}


/**
 * InnerTestMondeEntite
 */
class EntiteTest extends Entite {

    public EntiteTest(String nom, Monde monde) throws NomDEntiteDejaUtiliseDansLeMondeException {
	super(nom,monde);
    }


}
