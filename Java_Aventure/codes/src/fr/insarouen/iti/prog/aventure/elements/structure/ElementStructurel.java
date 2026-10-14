package fr.insarouen.iti.prog.aventure.elements.structure;

import fr.insarouen.iti.prog.aventure.elements.Entite;
import fr.insarouen.iti.prog.aventure.Monde;
import fr.insarouen.iti.prog.aventure.NomDEntiteDejaUtiliseDansLeMondeException;

/**
* ElementStructurel est une sous classe abstraite d'Entite représentant
* un élément structurant l'environnement
*
*/
public abstract class ElementStructurel extends Entite {

	/**
	* <p> Constructeur de l'élément structurel
	* </p>
	* @param nom nom de l'élément structurel
	* @param monde monde auquel appartient l'élément structurel
 	*/
	public ElementStructurel(String nom, Monde monde) throws NomDEntiteDejaUtiliseDansLeMondeException {
		super(nom, monde);
	}
}
