package fr.insarouen.iti.prog.aventure.elements.objets;

import fr.insarouen.iti.prog.aventure.elements.Entite;
import fr.insarouen.iti.prog.aventure.Monde;
import fr.insarouen.iti.prog.aventure.NomDEntiteDejaUtiliseDansLeMondeException;

/**
 * Objet abstrait principal, appartenant à un monde.
 * Gère notamment si l'objet est transportable ou non.
 */
public abstract class Objet extends Entite {
	
    //####################################################### Constructeurs #######################################################

	/**
	* Crée un objet avec un nom donné et l'insère dans le monde choisi.
	* @param nom le nom de l'objet
	* @param monde le monde où se trouve l'objet
 	*/
	public Objet(String nom, Monde monde) throws NomDEntiteDejaUtiliseDansLeMondeException {
		super(nom, monde);
	}
	
    //####################################################### Getters #######################################################

	/**
	* Vérifie si l'objet peut être ramassé et déplacé.
	* @return true si on peut le déplacer, false sinon
 	*/
	public abstract boolean estDeplacable();

    //####################################################### Methodes #######################################################

}
