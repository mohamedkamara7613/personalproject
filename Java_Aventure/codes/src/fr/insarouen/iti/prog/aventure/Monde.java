package fr.insarouen.iti.prog.aventure;

import fr.insarouen.iti.prog.aventure.elements.Entite;
import java.util.HashMap;
import java.util.Map;
import java.util.Collection;
import java.util.ArrayList;
import java.io.Serializable;

/**
 * Représente le monde du jeu vidéo qui contient toutes les entités
 */
public final class Monde implements Serializable {
	/**
	 * Nom du Monde
	 */
	private String nom;

	/**
	 * Entités composant le monde
	 */
	private Map<String, Entite> entites = new HashMap<>();

	//####################################################### Constructeurs #######################################################

	/**
	 * Initialise un nouveau Monde avec le nom donné.
	 * 
	 * @param nom Le nom du monde
	 */
	public Monde(String nom) {
		this.nom = nom;
	}

	//####################################################### Getters #######################################################

	/**
	 * Renvoie la liste de toutes les entités présentes dans ce monde.
	 * 
	 * @return les entités du monde
	 */
	public Collection<Entite> getEntites() {
		return new ArrayList(this.entites.values());
	}

    //-------------------------------------------------------------------------------------------------------------------

	/**
	 * Renvoie le nom de ce monde.
	 * 
	 * @return le nom du monde
	 */
	public String getNom() {
		return this.nom;
	}

    //-------------------------------------------------------------------------------------------------------------------

	/**
	 * Cherche et renvoie une entité par son nom précis.
	 * 
	 * @param nom le nom de l'entité à rechercher
	 * @return l'entité correspondante, ou null si introuvable
	 */
	public Entite getEntite(String nom) {
		Map<String, Entite> me = this.entites;
		Entite result = null;

		for (String n : me.keySet()) {
			if (n.equals(nom)) {
				result = me.get(n);
			}
		}

		return result;
	}

	//####################################################### Methodes #######################################################

	/**
	 * Enregistre une nouvelle entité dans le monde.
	 * 
	 * @param ent l'entité à insérer
	 * @throws EntiteDejaDansUnAutreMondeException       si l'entité est déjà assignée à un autre monde
	 * @throws NomDEntiteDejaUtiliseDansLeMondeException si une entité de même nom existe déjà
	 */
	public void ajouter(Entite ent)
			throws EntiteDejaDansUnAutreMondeException, NomDEntiteDejaUtiliseDansLeMondeException {
		if (ent.getMonde() != null && ent.getMonde() != this) {
			throw new EntiteDejaDansUnAutreMondeException("L'entité a déjà un monde !");
		}
		if (this.getEntite(ent.getNom()) != null) {
			throw new NomDEntiteDejaUtiliseDansLeMondeException("Une entité de même nom appartient déjà au monde !!");
		}

		this.entites.put(ent.getNom(), ent);
	}

    //-------------------------------------------------------------------------------------------------------------------

	/**
	 * Génère un nom unique (au hasard) pour une nouvelle entité.
	 * 
	 * @param prefixe le début du nom (ex: "Porte_")
	 * @return le nom unique généré
	 */
	public String genererNom(String prefixe) {
		String nom = null;
		do {
			nom = prefixe + (int) (Math.random() * Integer.MAX_VALUE);
		} while (this.getEntite(nom) != null);
		return nom;
	}

    //-----------

	/**
	 * Fournit une description en texte regroupant toutes les entités de ce monde.
	 * 
	 * @return La liste du monde et de ses entités en texte
	 */
	@Override
	public String toString() {
		StringBuilder s = new StringBuilder();
		s.append(this.nom);

		if (this.entites != null) {
			s.append(" : [");
			for (String n : entites.keySet()) {
				s.append(n);
				s.append(",");

			}
			s.append("]");
		}
		return s.toString();
	}
}
