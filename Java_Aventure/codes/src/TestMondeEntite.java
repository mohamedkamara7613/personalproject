
import fr.insarouen.iti.prog.aventure.elements.Entite;
import fr.insarouen.iti.prog.aventure.elements.objets.Objet;
import fr.insarouen.iti.prog.aventure.elements.objets.PiedDeBiche;
import fr.insarouen.iti.prog.aventure.elements.objets.AutomaticRifle;
import fr.insarouen.iti.prog.aventure.elements.structure.ElementStructurel;
import fr.insarouen.iti.prog.aventure.Monde;
import fr.insarouen.iti.prog.aventure.elements.TableauDynamique;
import fr.insarouen.iti.prog.aventure.NomDEntiteDejaUtiliseDansLeMondeException;


public class TestMondeEntite {

	public static void TestEntite() throws NomDEntiteDejaUtiliseDansLeMondeException {
		System.out.println("------------------------\nTestEntite\n--------\n");
		Monde m = new Monde("Fourmiland");
		String nom = "fourmis";
		Entite ant = new EntiteConcrete(nom,m);
		Entite ant2 = new EntiteConcrete("fourmis",m);
		System.out.println(String.format("Test Entite Equals : %b\n",ant.equals(ant2)));
		System.out.println(String.format("Test Entite getNom : %b\n",nom.equals(ant.getNom())));
		System.out.println(String.format("Test Entite getMonde : %b\n",m.equals(ant.getMonde())));
		
		System.out.println(String.format("%s\n",ant.toString()));
		
		System.out.println(String.format("HashCode ant : %d, HashCode ant2 : %d\n",ant.hashCode(),ant2.hashCode()));
		
		System.out.println(String.format("Egalite Hashcodes ant : %b\n",ant.hashCode() == ant2.hashCode()));
		
	}
	
	public static void TestObjet() throws NomDEntiteDejaUtiliseDansLeMondeException{
		System.out.println("------------------------\nTestObjet\n--------\n");
		Monde m = new Monde("Armes -land");
		PiedDeBiche p = new PiedDeBiche(m);
		AutomaticRifle AK_47 = new AutomaticRifle("AK-47", m);
		ObjetConcret Brique = new ObjetConcret("Brique rouge anglaise", m);
		System.out.println("Oki\n");
	}
	public static void TestElementStructurel() {
		System.out.println("------------------------\nTestElementStructurel\n--------\n");
		System.out.println("Rien à tester\n");
	}
	
	public static void TestTableauDynamique() throws NomDEntiteDejaUtiliseDansLeMondeException{
		System.out.println("------------------------\nTestTableauDynamique\n--------\n");
		TableauDynamique tab = new TableauDynamique();
		
		Monde m = new Monde("Armes -land");
		ObjetConcret Brique = new ObjetConcret("Brique rouge anglaise", m);
		AutomaticRifle AK_47 = new AutomaticRifle("AK-47", m);
		EntiteConcrete ps4 = new EntiteConcrete("ps4",m);
		
		tab.ajouter(Brique);
		tab.ajouter(AK_47);
		
		System.out.println(String.format("Test TableauD contient entite : %b\n",( tab.contient(Brique) )));
		System.out.println(String.format("Test TableauD contient nom : %b\n",( !tab.contient("ps5") )));
		
		System.out.println(String.format("Test TableauD get entite : %b\n",tab.get(0).equals(Brique)));
		System.out.println(String.format("Test TableauD get nom : %b\n",tab.get("AK-47").equals(AK_47)));
		
		tab.set(1,ps4);
		
		System.out.println(String.format("Test TableauD set : %b\n",(tab.get(1).equals(ps4))));
		tab.ajouter(AK_47);
		System.out.println(String.format("Test TableauD taille : %b\n",( tab.taille() == 3 )));
		
		tab.retirer(ps4);
		System.out.println(String.format("Test TableauD retirer entite: %b\n",( !tab.contient(ps4) )));
		tab.retirer("Brique rouge anglaise");
		
		System.out.println(String.format("Test TableauD retirer nom : %b\n",( !tab.contient(Brique) )));
	}
	
	
	
	public static void main(String[] args) throws NomDEntiteDejaUtiliseDansLeMondeException {
		TestEntite();
		TestObjet();
		TestElementStructurel();
		TestTableauDynamique();
	}
}



class EntiteConcrete extends Entite {
	public EntiteConcrete(String nom, Monde monde) throws NomDEntiteDejaUtiliseDansLeMondeException{
		super(nom, monde);
	}
}

class ObjetConcret extends Objet {
	public ObjetConcret(String nom, Monde monde) throws NomDEntiteDejaUtiliseDansLeMondeException{
		super(nom, monde);
	}
	
	public boolean estDeplacable(){
		return true;
	}
}

class ElementStructurelConcret extends ElementStructurel {
	public ElementStructurelConcret(String nom, Monde monde) throws NomDEntiteDejaUtiliseDansLeMondeException{
		super(nom, monde);
	}
}
