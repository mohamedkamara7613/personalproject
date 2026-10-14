package fr.insarouen.iti.prog.aventure.elements.objets;

import fr.insarouen.iti.prog.aventure.Monde;
import fr.insarouen.iti.prog.aventure.NomDEntiteDejaUtiliseDansLeMondeException;

/**
* Type d'objet déplaçable
*
*/
public class PiedDeBiche extends Objet{
	
	
	/**
	* <p> Constructeur de PiedDeBiche
	* </p>
	* @param nom le nom du PiedDeBiche
	* @param monde le monde auquel le PiedDeBiche appartient
 	*/
	public PiedDeBiche(String nom, Monde m) throws NomDEntiteDejaUtiliseDansLeMondeException {
		super(nom, m);
		//super("Pied de biche",m); 
		// SINON TOUS LES PIED DE BICHE S'APPELLERONT "Pied de biche"
		// Bah oui c'est l'idée. En général j'appelle les pieds de biche "pied de biche" et pas "orange d'espagne"
		// Puis c'est pratique pour savoir dans l'inventaire si j'ai un Pied de biche de pouvoir juste chercher "Pied de biche" et pas la liste complète
		//en allemand des fromages régionnaux français
	}

	/**
	* <p> Constructeur par defaut de PiedDeBiche (Nom: Pied de biche)
	* </p>
	* @param monde le monde auquel le PiedDeBiche appartient
 	*/
	public PiedDeBiche(Monde m) throws NomDEntiteDejaUtiliseDansLeMondeException {
		super("Pied de biche", m);
	}

	/**
	* Renvoit que l'objet est déplaçable
	*
 	*/
	@Override
	public boolean estDeplacable() {
		return true;
	}
}
