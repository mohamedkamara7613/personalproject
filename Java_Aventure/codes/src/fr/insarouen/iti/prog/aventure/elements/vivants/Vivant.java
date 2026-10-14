package fr.insarouen.iti.prog.aventure.elements.vivants;

import fr.insarouen.iti.prog.aventure.elements.structure.Piece;
import fr.insarouen.iti.prog.aventure.ITIAventureException;
import fr.insarouen.iti.prog.aventure.Monde;
import fr.insarouen.iti.prog.aventure.elements.Entite;
import fr.insarouen.iti.prog.aventure.elements.structure.Porte;
import fr.insarouen.iti.prog.aventure.elements.Etat;
import fr.insarouen.iti.prog.aventure.elements.objets.Objet;
import fr.insarouen.iti.prog.aventure.elements.Executable;
import java.util.HashMap;
import java.util.Map;
import java.util.Collection;
import java.util.ArrayList;

import fr.insarouen.iti.prog.aventure.NomDEntiteDejaUtiliseDansLeMondeException;
import fr.insarouen.iti.prog.aventure.elements.structure.ObjetAbsentDeLaPieceException;
import fr.insarouen.iti.prog.aventure.elements.structure.VivantAbsentDeLaPieceException;
import fr.insarouen.iti.prog.aventure.elements.objets.ObjetNonDeplacableException;
import fr.insarouen.iti.prog.aventure.elements.structure.PorteInexistanteDansLaPieceException;
import fr.insarouen.iti.prog.aventure.elements.structure.PorteFermeException;

/**
 * Représente un être vivant joueur ou non, qui se promène dans la carte.
 * Il a de la vie, de la force, un sac à dos pour les objets et une position
 * dans une pièce.
 */
public class Vivant extends Entite implements Executable {

	private int pointVie;
	private int pointForce;
	private Piece piece;
	private Map<String, Objet> objets = new HashMap<>();

	// ####################################################### Constructeurs
	// #######################################################

	/**
	 * Donne naissance à un Vivant avec tous ses paramètres de base.
	 * 
	 * @param nom        le nom du personnage
	 * @param monde      le monde où il pop
	 * @param pointVie   la santé / Points de vie initiaux
	 * @param pointForce la force physique du personnage
	 * @param piece      la pièce de départ
	 * @param objets     les objets de départ directement dans son sac
	 */
	public Vivant(String nom, Monde monde, int pointVie, int pointForce, Piece piece, Objet... objets)
			throws NomDEntiteDejaUtiliseDansLeMondeException {
		super(nom, monde);

		this.pointVie = pointVie;
		this.pointForce = pointForce;
		this.piece = piece;
		piece.entrer(this);

		Map<String, Objet> temp = new HashMap<>();

		for (int i = 0; i < objets.length; i++) {
			temp.put(objets[i].getNom(), objets[i]);
		}
		this.objets = temp;
	}

	// ####################################################### Getters
	// #######################################################

	/**
	 * Demande le nombre de points de vie actuels de la personne.
	 * 
	 * @return les PV du vivant
	 */
	public int getPointVie() {
		return this.pointVie;
	}

	// -------------------------------------------------------------------------------------------------------------------

	/**
	 * Demande le niveau de force brute du personnage.
	 * 
	 * @return la force
	 */
	public int getPointForce() {
		return this.pointForce;
	}

	// -------------------------------------------------------------------------------------------------------------------

	/**
	 * Sort un objet du sac à dos uniquement grâce à l'inspection de nom.
	 * 
	 * @param nomObj nom de l'objet qu'on cherche
	 * @return l'objet correspondant trouvé dans le sac
	 */
	public Objet getObjet(String nomObj) {
		return (Objet) this.objets.get(nomObj);
	}

	// -------------------------------------------------------------------------------------------------------------------

	/**
	 * Fait l'inventaire complet du sac.
	 * 
	 * @return la liste de tous les objets possédés
	 */
	public Collection<Objet> getObjets() {
		return new ArrayList(this.objets.values());
	}

	// -------------------------------------------------------------------------------------------------------------------

	/**
	 * Regarde la pièce dans laquelle le personnage se trouve actuellement.
	 * 
	 * @return la pièce actuelle
	 */
	public Piece getPiece() {
		return this.piece;
	}

	// -------------------------------------------------------------------------------------------------------------------

	/**
	 * Vérifie très basiquement si le joueur est mort (PV à 0).
	 * 
	 * @return vrai si le vivant est mort
	 */
	public boolean estMort() {
		return (this.getPointVie() == 0);
	}

	// ####################################################### Setters
	// #######################################################

	/**
	 * Modifie le niveau de santé actuel.
	 * 
	 * @param pv les nouveaux points de vie
	 */
	public void setPointVie(int pv) {
		this.pointVie = pv;
	}

	// -------------------------------------------------------------------------------------------------------------------

	/**
	 * Met à jour la force musculaire du joueur.
	 * 
	 * @param pf la nouvelle force
	 */
	public void setPointForce(int pf) {
		this.pointForce = pf;
	}

	// -------------------------------------------------------------------------------------------------------------------

	/**
	 * Téléporte le personnage de sa propre volonté d'une pièce à l'autre sans
	 * passer de porte propre.
	 * 
	 * @param piece la pièce cible de la téléportation
	 */
	public void setPiece(Piece piece) {
		if (this.piece == piece) {
			return;
		}

		Piece anciennePiece = this.piece;
		this.piece = piece;
		try {
			if (anciennePiece != null && anciennePiece.contientVivant(this)) {
				anciennePiece.sortir(this);
			}

			if (this.piece != null && !this.piece.contientVivant(this)) {
				this.piece.entrer(this);
			}
		} catch (VivantAbsentDeLaPieceException e) {
			throw new Error("Pas de sens que setPiece lève l'execption VivantAbsentDeLaPieceException");
		}
	}

	// ####################################################### Methodes
	// #######################################################

	/**
	 * Franche question : as-tu cet objet avec toi ?
	 * 
	 * @param obj objet en question
	 * @return vrai si l'objet est dans le sac
	 */
	public boolean possede(Objet obj) {
		return this.objets.containsValue(obj);
	}

	// -------------------------------------------------------------------------------------------------------------------

	/**
	 * Franche question : as-tu l'objet nommé comme tel avec toi ?
	 * 
	 * @param nomObj nom de l'objet en question
	 * @return vrai si l'objet est présent
	 */
	public boolean possede(String nomObj) {
		return this.objets.containsKey(nomObj);
	}

	// -------------------------------------------------------------------------------------------------------------------

	/**
	 * Le personnage ramasse l'objet par terre et le met dans son sac.
	 * 
	 * @param obj Objet de la pièce à ramasser
	 */
	public void prendre(Objet obj) throws ObjetNonDeplacableException, ObjetAbsentDeLaPieceException {
		this.piece.retirer(obj);
		this.objets.put(obj.getNom(), obj);
	}

	// -------------------------------------------------------------------------------------------------------------------

	/**
	 * Le personnage ramasse ce qu'il identifie par ce nom dans son environnement
	 * direct.
	 * 
	 * @param nomObj nom de l'objet à ramasser
	 */
	public void prendre(String nomObj) throws ObjetNonDeplacableException, ObjetAbsentDeLaPieceException {
		Objet obj = this.piece.retirer(nomObj);
		this.objets.put(obj.getNom(), obj);
	}

	// -------------------------------------------------------------------------------------------------------------------

	/**
	 * Le joueur s'allège en jetant l'objet par terre dans la pièce actuelle.
	 * 
	 * @param obj objet à jeter
	 */
	public void deposer(Objet obj) throws ObjetNonPossedeParLeVivantException {
		if (!this.objets.containsValue(obj)) {
			throw new ObjetNonPossedeParLeVivantException(
					String.format("Le vivant ne possède pas %s !!!!!", obj.toString()));
		}
		this.objets.remove(obj.getNom());
		this.piece.deposer(obj);
	}

	// -------------------------------------------------------------------------------------------------------------------

	/**
	 * Le joueur s'allège en jetant l'objet qu'on identifie par le nom en question.
	 * 
	 * @param nomObj nom de l'objet à jeter
	 */
	public void deposer(String nomObj) throws ObjetNonPossedeParLeVivantException {
		if (!this.objets.containsKey(nomObj)) {
			throw new ObjetNonPossedeParLeVivantException(String.format("Le vivant ne possède pas %s !!!!!!", nomObj));
		}
		this.piece.deposer((Objet) this.objets.remove(nomObj));
	}

	// -------------------------------------------------------------------------------------------------------------------

	/**
	 * Fait marcher physiquement la créature à travers la porte et donc, la change
	 * de pièce.
	 * 
	 * @param porte la porte par laquelle passer
	 */
	public void franchir(Porte porte) throws PorteInexistanteDansLaPieceException, PorteFermeException {
		// Collection<Porte> portesDeLaPiece = this.piece.getPortes();
		if (!piece.aLaPorte(porte)) {
			throw new PorteInexistanteDansLaPieceException("Cette porte n'est pas dans la piece.");
		}

		if (porte.getEtat() == Etat.FERME || porte.getEtat() == Etat.VERROUILLE) {
			throw new PorteFermeException("On ne franchit pas  une porte fermée ou verrouillee.");
		}

		Piece pieceAutrePiece = porte.getPieceAutreCote(this.getPiece());
		this.setPiece(pieceAutrePiece);
	}

	// -------------------------------------------------------------------------------------------------------------------

	/**
	 * Fait marcher la créature à travers la porte cherchée par nom.
	 * 
	 * @param nomPorte le nom de la porte en question
	 */
	public void franchir(String nomPorte) throws PorteInexistanteDansLaPieceException, PorteFermeException {
		Collection<Porte> portesDeLaPiece = this.piece.getPortes();
		Porte porte = null;
		for (Porte p : portesDeLaPiece) {
			if (p.getNom().equals(nomPorte)) {
				porte = p;
				break;
			}
		}
		if (porte == null) {
			throw new PorteInexistanteDansLaPieceException("La porte \"" + nomPorte + "\" n'est pas dans la pièce.");
		}
		this.franchir(porte);
	}

	// -------------------------------------------------------------------------------------------------------------------

	/**
	 * Affiche la feuille de personnage pour tout récapituler (Vie, Force,
	 * Equipement).
	 * 
	 * @return texte narratif qui décrit fièrement la bête
	 */
	@Override
	public String toString() {
		StringBuilder sb = new StringBuilder();

		sb.append("\n########################################\n");
		sb.append("########################################\n");
		sb.append(String.format("#   VIVANT : %-26s #\n", this.getNom()));
		sb.append("########################################\n");
		sb.append(String.format("# Monde     : %-26s #\n", monde.getNom()));
		sb.append(String.format("# Vie       : %-26d #\n", this.getPointVie()));
		sb.append(String.format("# Force     : %-26d #\n", this.getPointForce()));
		if (piece != null) {
			sb.append(String.format("# Position  : %-26s #\n", piece.getNom()));
		} else {
			sb.append(String.format("# Position  : %-26s #\n", "Dimension parallele"));
		}

		sb.append("----------------------------------------\n");
		sb.append("# Objets :\n");

		if (this.objets == null || this.objets.size() == 0) {
			sb.append("#   - aucun\n");
		} else {
			for (Objet obj : this.objets.values().toArray(new Objet[objets.size()])) {
				sb.append("#   - ").append(obj.getNom()).append("\n");
			}
		}

		sb.append("########################################\n");

		return sb.toString();
	}

	// -------------------------------------------------------------------------------------------------------------------

	/**
	 * N'a pas d'action spontanée par défaut.
	 */
	@Override
	public void executer() throws ITIAventureException {
		// Par défaut, un Vivant lambda ne fait rien
	}

}
