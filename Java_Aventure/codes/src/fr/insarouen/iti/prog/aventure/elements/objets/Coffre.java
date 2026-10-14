package fr.insarouen.iti.prog.aventure.elements.objets;

import fr.insarouen.iti.prog.aventure.Monde;
import fr.insarouen.iti.prog.aventure.NomDEntiteDejaUtiliseDansLeMondeException;

/**
* Type d'objet non déplaçable
*
*/
public class Coffre extends Objet{
	
	
	/**
	* <p> Constructeur de Coffre
	* </p>
	* @param nom le nom du Coffre
	* @param monde le monde auquel le Coffre appartient
 	*/
	public Coffre(String nom, Monde m) throws NomDEntiteDejaUtiliseDansLeMondeException {
		super(nom, m);
		//la liste complète en allemand des fromages régionnaux français
	}

	/**
	* <p> Constructeur par defaut de Coffre (Nom: Coffre)
	* </p>
	* @param monde le monde auquel le Coffre appartient
 	*/
	public Coffre(Monde m) throws NomDEntiteDejaUtiliseDansLeMondeException {
		super("Coffre", m);
	}

	/**
	* Renvoit que l'objet est pas déplaçable
	*
 	*/
	@Override
	public boolean estDeplacable() {
		return false;
	}
}
