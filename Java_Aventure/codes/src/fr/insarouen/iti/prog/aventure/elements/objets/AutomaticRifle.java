package fr.insarouen.iti.prog.aventure.elements.objets;

import fr.insarouen.iti.prog.aventure.Monde;
import fr.insarouen.iti.prog.aventure.NomDEntiteDejaUtiliseDansLeMondeException;

/**
 * Classe representant un fusil automatique.
 */
public class AutomaticRifle extends Objet {

	/**
	 * Constructeur de la classe AutomaticRifle.
	 * 
	 * @param nom Nom du fusil.
	 * @param m   Monde dans lequel se trouve l'objet.
	 */
	public AutomaticRifle(String nom, Monde m) throws NomDEntiteDejaUtiliseDansLeMondeException {
		super(nom, m);
	}

	@Override
	/**
	 * Indique si l'objet est deplacable.
	 * 
	 * @return Toujours vrai pour un fusil automatique évidement.
	 */
	public boolean estDeplacable() {
		return true;
	}

}
