package fr.insarouen.iti.prog.aventure.elements.structure;

import fr.insarouen.iti.prog.aventure.elements.objets.Objet;
import fr.insarouen.iti.prog.aventure.Monde;
import fr.insarouen.iti.prog.aventure.elements.vivants.Vivant;
import java.util.HashMap;
import java.util.Map;
import java.util.Collection;
import java.util.ArrayList;

import fr.insarouen.iti.prog.aventure.NomDEntiteDejaUtiliseDansLeMondeException;
import fr.insarouen.iti.prog.aventure.elements.objets.ObjetNonDeplacableException;

/**
 * Une pièce est un lieu du jeu qui gère la présence des objets
 * et des êtres vivants qu'elle contient.
 */
public class Piece extends ElementStructurel {

	/**
	 * tableau utilisé pour contenir les objets
	 */
	private Map<String, Objet> tabObjet = new HashMap<>();

	/**
	 * tableau utilisé pour contenir les vivants
	 */
	private Map<String, Vivant> tabVivant = new HashMap<>();

	private Map<String, Porte> tabPorte = new HashMap<>();

	//####################################################### Constructeurs #######################################################
	
	/**
	 * Crée une pièce, qui contiendra ensuite des objets, des vivants, et des portes.
	 * 
	 * @param nom   le nom de la pièce
	 * @param monde le monde auquel la pièce appartient
	 */
	public Piece(String nom, Monde monde) throws NomDEntiteDejaUtiliseDansLeMondeException {
		super(nom, monde);
		this.tabObjet = new HashMap<>();
		this.tabVivant = new HashMap<>();
		this.tabPorte = new HashMap<>();
	}

	//####################################################### Getters #######################################################

	/**
	 * Donne tous les objets présents dans la pièce.
	 * 
	 * @return la liste des objets
	 */
	public Collection<Objet> getObjets() {
		return new ArrayList(this.tabObjet.values());
	}

    //-------------------------------------------------------------------------------------------------------------------

	/**
	 * Donne tous les êtres vivants présents dans la pièce.
	 * 
	 * @return la liste des vivants
	 */
	public Collection<Vivant> getVivants() {
		return new ArrayList(this.tabVivant.values());
	}

    //-------------------------------------------------------------------------------------------------------------------

	/**
	 * Donne toutes les portes appartenant à cette pièce.
	 * 
	 * @return la liste des portes
	 */
	public Collection<Porte> getPortes() {
		return new ArrayList(this.tabPorte.values());
	}

    //-------------------------------------------------------------------------------------------------------------------

	/**
	 * Trouve une porte spécifique dans la pièce par son nom.
	 * 
	 * @return la porte, ou null si elle n'existe pas ici
	 */
	public Porte getPorte(String nomPorte) {
		return this.tabPorte.get(nomPorte);
	}

	//####################################################### Methodes #######################################################

	/**
	 * Vérifie si l'objet est posé dans cette pièce.
	 * 
	 * @param obj l'objet recherché dans la pièce
	 * @return vrai si l'objet est ici, faux sinon
	 */
	public boolean contientObjet(Objet obj) {
		return this.tabObjet.containsValue(obj);
	}

    //-------------------------------------------------------------------------------------------------------------------

	/**
	 * Vérifie si un objet avec ce nom précis est posé dans cette pièce.
	 * 
	 * @param nomObj le nom de l'objet recherché dans la pièce
	 * @return vrai si un tel objet est ici, faux sinon
	 */
	public boolean contientObjet(String nomObj) {
		return this.tabObjet.containsKey(nomObj);
	}

    //-------------------------------------------------------------------------------------------------------------------

	/**
	 * Pose un objet dans la pièce (le rajoute à la liste).
	 * 
	 * @param obj l'objet à poser
	 */
	public void deposer(Objet obj) {
		this.tabObjet.put(obj.getNom(), obj);
	}

    //-------------------------------------------------------------------------------------------------------------------

	/**
	 * Enlève physiquement un objet de la pièce.
	 * 
	 * @param obj l'objet à enlever
	 * @return l'objet qu'on a ramassé
	 */
	public Objet retirer(Objet obj) throws ObjetAbsentDeLaPieceException, ObjetNonDeplacableException {
		if (!this.contientObjet(obj)) {
			throw new ObjetAbsentDeLaPieceException("L'objet " + obj.getNom() + " n'est pas dans la pièce !!!!");
		}

		if (!obj.estDeplacable()) {
			throw new ObjetNonDeplacableException("On ne peut retirer un objet non déplaçable !!!");
		}

		return (Objet) this.tabObjet.remove(obj.getNom());
	}

    //-------------------------------------------------------------------------------------------------------------------

	/**
	 * Enlève physiquement un objet de la pièce via son nom.
	 * 
	 * @param nomObj le nom de l'objet à retirer
	 * @return l'objet qu'on a ramassé
	 */
	public Objet retirer(String nomObj) throws ObjetNonDeplacableException, ObjetAbsentDeLaPieceException {
		if (!this.contientObjet(nomObj)) {
			throw new ObjetAbsentDeLaPieceException("L'objet " + nomObj + " n'est pas dans la pièce !!!!!");
		}
		Objet obj = (Objet) this.tabObjet.get(nomObj);

		if (!obj.estDeplacable()) {
			throw new ObjetNonDeplacableException("On ne peut retirer un objet non déplaçable !!!!");
		}

		this.tabObjet.remove(nomObj);
		return obj;

	}

    //-------------------------------------------------------------------------------------------------------------------

	/**
	 * Vérifie si une personne ou une créature (Vivant) est actuellement dans la pièce.
	 * 
	 * @param vivant le Vivant recherché
	 * @return vrai s'il est ici, faux sinon
	 */
	public boolean contientVivant(Vivant vivant) {
		return this.tabVivant.containsValue(vivant);
	}

    //-------------------------------------------------------------------------------------------------------------------

	/**
	 * Vérifie si quelqu'un avec ce nom précis se trouve dans la pièce.
	 * 
	 * @param nomVivant le nom cherché
	 * @return vrai si la personne y est, faux sinon
	 */
	public boolean contientVivant(String nomVivant) {
		return this.tabVivant.containsKey(nomVivant);
	}

    //-------------------------------------------------------------------------------------------------------------------

	/**
	 * Fait physiquement sortir un vivant de la pièce.
	 * 
	 * @param vivant celui qui sort
	 */
	public Vivant sortir(Vivant vivant) throws VivantAbsentDeLaPieceException {
		if (!this.contientVivant(vivant)) {
			throw new VivantAbsentDeLaPieceException("Le vivant n'est pas dans la pièce à quitter !!!!!!!");
		}

		Vivant v = (Vivant) this.tabVivant.remove(vivant.getNom());

		if (vivant.getPiece() == this) {
			vivant.setPiece(null);
		}
		return v;
	}

    //-------------------------------------------------------------------------------------------------------------------

	/**
	 * Fait sortir un vivant par son nom.
	 * 
	 * @param nomVivant le nom de celui qui sort
	 * @return celui qui est sorti
	 */
	public Vivant sortir(String nomVivant) throws VivantAbsentDeLaPieceException {
		Vivant v = (Vivant) this.tabVivant.get(nomVivant);
		return this.sortir(v);
	}

    //-------------------------------------------------------------------------------------------------------------------

	/**
	 * Fait entrer une personne dans la pièce.
	 * 
	 * @param vivant celui qui entre
	 */
	public void entrer(Vivant vivant) {
		if (this.contientVivant(vivant)) {
			return; 
		}

		this.tabVivant.put(vivant.getNom(), vivant);

		if (vivant.getPiece() != this) {
			vivant.setPiece(this);
		}
	}

    //-------------------------------------------------------------------------------------------------------------------

	/**
	 * Attache une porte existante à cette pièce.
	 * 
	 * @param porte la porte à ajouter
	 */
	protected void addPorte(Porte porte){
		if(!this.tabPorte.containsValue(porte)){
			this.tabPorte.put(porte.getNom(), porte);
		}
	}

    //-------------------------------------------------------------------------------------------------------------------

	/**
	 * Vérifie si la pièce possède cette porte.
	 * 
	 * @param porte la porte en question
	 * @return vrai s'il y a un accès
	 */
	public boolean aLaPorte(Porte porte) {
		return this.tabPorte.containsValue(porte);
	}

    //-------------------------------------------------------------------------------------------------------------------

	/**
	 * Vérifie si la pièce possède une porte répondant à ce nom.
	 * 
	 * @param nomPorte le nom de la porte
	 * @return vrai si on a cette porte
	 */
	public boolean aLaPorte(String nomPorte) {
		return this.tabPorte.containsKey(nomPorte);
	}

    //-------------------------------------------------------------------------------------------------------------------

	/**
	 * Construit le résumé texte d'une pièce.
	 * Il contient son nom, les objets par terre et les personnes présentes.
	 * 
	 * @return la description complète de la pièce
	 */
	@Override
	public String toString() {
		StringBuilder sb = new StringBuilder();
		sb.append(this.getNom());
		sb.append("\n   -");
		sb.append(this.tabObjet.toString());
		sb.append("\n   -");
		sb.append(this.tabVivant.toString());
		sb.append("\n");
		return sb.toString();
	}
}

