package fr.insarouen.iti.prog.aventure.elements.structure;

import fr.insarouen.iti.prog.aventure.Monde;
import fr.insarouen.iti.prog.aventure.elements.Activable;
import fr.insarouen.iti.prog.aventure.elements.Etat;
import fr.insarouen.iti.prog.aventure.elements.objets.Objet;
import fr.insarouen.iti.prog.aventure.elements.objets.serrurerie.Serrure;
import fr.insarouen.iti.prog.aventure.elements.objets.PiedDeBiche;

import fr.insarouen.iti.prog.aventure.NomDEntiteDejaUtiliseDansLeMondeException;
import fr.insarouen.iti.prog.aventure.elements.ActivationImpossibleException;
import fr.insarouen.iti.prog.aventure.elements.ActivationImpossibleAvecObjetException;

/**
 * Représente une porte qui relie deux pièces du jeu.
 * Elle peut être ouverte, fermée, ou verrouillée avec une serrure.
 */
public class Porte extends ElementStructurel implements Activable {
    private Etat etat;
    private Piece pieceA;
    private Piece pieceB;
    private Serrure serrure = null;

    //####################################################### Constructeurs #######################################################

    /**
     * Crée une porte standard (fermée mais sans serrure) entre deux pièces.
     * 
     * @param nom le nom de la porte
     * @param monde le monde
     * @param pieceA la première pièce
     * @param pieceB la deuxième pièce
     */
    public Porte(String nom, Monde monde, Piece pieceA, Piece pieceB) throws NomDEntiteDejaUtiliseDansLeMondeException{
        super(nom, monde);
        this.etat = Etat.FERME;
        this.pieceA = pieceA;
        this.pieceB = pieceB;
        this.pieceA.addPorte(this);
        this.pieceB.addPorte(this);
    }

    //-------------------------------------------------------------------------------------------------------------------

    /**
     * Crée une porte munie d'une serrure entre deux pièces.
     * Elle est verrouillée dès le départ.
     * 
     * @param nom le nom de la porte
     * @param monde le monde
     * @param serrure la serrure attachée à la porte
     * @param pieceA la première pièce
     * @param pieceB la deuxième pièce
     */
    public Porte(String nom, Monde monde, Serrure serrure, Piece pieceA, Piece pieceB) throws NomDEntiteDejaUtiliseDansLeMondeException{
        this(nom, monde, pieceA, pieceB);
        this.serrure = serrure;
        this.etat = Etat.VERROUILLE;
    }

    //####################################################### Getters #######################################################

    /**
     * Donne l'état actuel de la porte (Ouverte, Fermée ou Verrouillée).
     * 
     * @return l'état de la porte
     */
    public Etat getEtat(){
        if (this.serrure != null && this.serrure.getEtat() == Etat.VERROUILLE) {
            return Etat.VERROUILLE;
        }
        return this.etat;
    }

    //-------------------------------------------------------------------------------------------------------------------

    /**
     * Récupère la serrure installée sur cette porte.
     * 
     * @return la serrure de la porte, ou null s'il n'y en a pas
     */
    public Serrure getSerrure(){
        return this.serrure;
    }

    //-------------------------------------------------------------------------------------------------------------------

    /**
     * Indique la pièce située de l'autre côté de la porte.
     * 
     * @param piece la pièce où on se trouve
     * @return la pièce de l'autre côté
     */
    public Piece getPieceAutreCote(Piece piece){
        if (piece.equals(pieceA)){
            return pieceB;
        }
        else{
            return pieceA;
        }
    }

    //####################################################### Methodes #######################################################

    /**
     * Indique si on peut interagir avec la porte en utilisant cet objet (comme un Pied de Biche ou une clé).
     * 
     * @param obj l'objet qu'on tient en main
     * @return vrai si l'objet est utile ici, faux sinon
     */
    public boolean activableAvec(Objet obj){
        if(this.serrure == null){
            return false;
        }
        else if (obj instanceof PiedDeBiche) {
            return true;
        }
        else {
            return this.serrure.activableAvec(obj);
        }
    }

    //-------------------------------------------------------------------------------------------------------------------

    /**
     * Permet d'ouvrir ou de fermer la porte à mains nues.
     * Impossible si la porte est verrouillée à clé.
     */
    public void activer() throws ActivationImpossibleException {
        if(this.serrure != null && this.serrure.getEtat().equals(Etat.VERROUILLE)){
            throw new ActivationImpossibleException("Utilisez la bonne clé");
        }
        else{  
            if(this.etat == Etat.FERME || this.etat == Etat.VERROUILLE){
                this.etat = Etat.OUVERT;
            }
            else if(this.etat == Etat.OUVERT){
                this.etat = Etat.FERME;
            }
        }
    }

    //-------------------------------------------------------------------------------------------------------------------

    /**
     * Permet d'ouvrir la porte en forçant avec un objet ou en utilisant la bonne clé.
     * 
     * @param obj l'objet utilisé sur la porte
     */
    public void activerAvec(Objet obj) throws ActivationImpossibleAvecObjetException, ActivationImpossibleException{
        if (!this.activableAvec(obj)){
            throw new ActivationImpossibleAvecObjetException(String.format("Porte non activable avec %s !!!", obj.toString()));
        }
        else if(obj instanceof PiedDeBiche) {
            this.serrure = null;
            this.etat = Etat.OUVERT;
        }
        else{
            this.serrure.activerAvec(obj);
            if (this.serrure.getEtat() == Etat.DEVERROUILLE) {
                this.etat = Etat.OUVERT;
            } else {
                this.etat = Etat.VERROUILLE;
            }
        }
    }

    //-------------------------------------------------------------------------------------------------------------------

    /**
     * Résume la porte en texte avec son état et les pièces qu'elle relie.
     * 
     * @return description de la porte
     */
    @Override
    public String toString(){
        StringBuilder sb = new StringBuilder();
		sb.append(this.getNom());
		sb.append("\n   -");
        sb.append(this.getMonde().getNom());
		sb.append("\n   -");
		sb.append(this.etat.toString());
		sb.append("\n   -");
		sb.append(this.pieceA.toString());
		sb.append("\n   -");
		sb.append(this.pieceB.toString());
		sb.append("\n");
		return sb.toString();
    } 
}