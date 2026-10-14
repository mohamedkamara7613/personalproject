package fr.insarouen.iti.prog.aventure.elements;

import java.io.Serializable;
import fr.insarouen.iti.prog.aventure.Monde;
import fr.insarouen.iti.prog.aventure.EntiteDejaDansUnAutreMondeException;
import fr.insarouen.iti.prog.aventure.NomDEntiteDejaUtiliseDansLeMondeException;

/**
 * Représente une entité abstraite.
 * Une entité possède un nom et appartient à un monde.
 */

public abstract class Entite implements Serializable {
	
	/**
	* nom de l'entité
	*/
	protected String nom;
	
	/**
	* monde de l'entité
	*/
	protected Monde monde;
	
    //####################################################### Constructeurs #######################################################

	/**
	* Crée une entité avec un nom et un monde donné, en l'ajoutant à ce dernier.
	* @param nom le nom de l'entité
	* @param monde le monde de l'entité
 	*/
	public Entite(String nom, Monde monde) throws NomDEntiteDejaUtiliseDansLeMondeException {
		this.nom = nom;
		this.monde = monde;
		if (this.monde != null) {
			try {
				this.monde.ajouter(this);
			}
			catch (EntiteDejaDansUnAutreMondeException e) {
				throw new Error("Error vraiment pas normale.");
			}
		}
	}
	
    //####################################################### Getters #######################################################

	/**
	* Permet de récupérer le nom de l'entité.
	* @return le nom de l'entité
 	*/
	public String getNom() {
		return this.nom;
	}

    //-----------
	
	/**
	* Permet de récupérer le monde de l'entité.
	* @return le monde de l'entité
 	*/
	public Monde getMonde() {
		return this.monde;
	}
	
    //####################################################### Methodes #######################################################

	/**
	* Calcule un code unique (hash) basé sur le nom et le monde de l'entité.
	* @return le code de hachage
 	*/
	@Override
	public int hashCode() {
		return 119 * this.nom.hashCode() + 19 * this.monde.hashCode();
	}

    //-------------------------------------------------------------------------------------------------------------------
	
	/**
	* Permet de comparer si deux objets sont la même entité.
	* @param obj l'objet à comparer
	* @return vrai si les objets sont identiques, faux sinon
 	*/
	@Override
	public boolean equals(Object obj) {
		if (obj == null || this.getClass() != obj.getClass()) {
			return false;
		}
		Entite ent = (Entite) (obj);
		return (((this.hashCode()) == (ent.hashCode())) && this.nom.equals(ent.nom) && this.monde.equals(ent.monde));
	}

    //-----------
	
	/**
	* Renvoie une présentation simple (texte) de l'entité.
 	* @return description en texte de l'entité
 	*/
	@Override
	public String toString() {
		return String.format("Salut je suis %s\n",this.nom);
	}
}
