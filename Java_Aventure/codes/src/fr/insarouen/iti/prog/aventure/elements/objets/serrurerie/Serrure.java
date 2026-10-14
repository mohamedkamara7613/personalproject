package fr.insarouen.iti.prog.aventure.elements.objets.serrurerie;

import fr.insarouen.iti.prog.aventure.elements.objets.Objet;
import fr.insarouen.iti.prog.aventure.Monde;
import fr.insarouen.iti.prog.aventure.elements.Activable;
import fr.insarouen.iti.prog.aventure.elements.Etat;

import fr.insarouen.iti.prog.aventure.NomDEntiteDejaUtiliseDansLeMondeException;
import fr.insarouen.iti.prog.aventure.elements.ActivationException;
import fr.insarouen.iti.prog.aventure.elements.ActivationImpossibleException;
import fr.insarouen.iti.prog.aventure.elements.ActivationImpossibleAvecObjetException;

/**
 * Objet représentant une serrure qu'on peut verrouiller ou déverrouiller avec une clé.
 */
public class Serrure extends Objet implements Activable {

    private Etat etat;
    private Cle cle = null;

    //####################################################### Constructeurs #######################################################

    /**
     * Crée une serrure avec un nom généré automatiquement.
     * @param monde le monde où placer la serrure
     */
    public Serrure(Monde monde) throws NomDEntiteDejaUtiliseDansLeMondeException{
        this(monde.genererNom("Serrure_"), monde);
    }

    //-------------------------------------------------------------------------------------------------------------------

    /**
     * Crée une serrure avec un nom précis. Elle est verrouillée par défaut.
     * @param nom le nom de la serrure
     * @param monde le monde où placer la serrure
     */
    public Serrure(String nom, Monde monde) throws NomDEntiteDejaUtiliseDansLeMondeException{
        super(nom, monde);
        etat = Etat.VERROUILLE;
    }

    //####################################################### Getters #######################################################

    /**
     * Renvoie l'état actuel de la serrure (VERROUILLE ou DEVERROUILLE).
     * @return l'état de la serrure
     */
    public Etat getEtat(){
        return this.etat;
    }

    //-------------------------------------------------------------------------------------------------------------------

    /**
     * Vérifie si la serrure peut être déplacée.
     * @return toujours faux, on ne trimballe pas une serrure
     */
    @Override
	public boolean estDeplacable() {
        return false;
    }

    //####################################################### Methodes #######################################################
    
    /**
     * Vérifie si l'objet présenté est la bonne clé pour cette serrure.
     * @param obj l'objet qu'on essaie d'utiliser
     * @return vrai si c'est la bonne clé, faux sinon
     */
    public boolean activableAvec(Objet obj) {
        if (this.cle == null) { 
            return false;
        }
        else {
            return this.cle.equals(obj);
        }
    }

    //-------------------------------------------------------------------------------------------------------------------

    /**
     * Tente d'activer la serrure sans rien. C'est impossible.
     */
    public void activer() throws ActivationImpossibleException {
        throw new ActivationImpossibleException("Serrure non activable sans rien");
    }

    //-------------------------------------------------------------------------------------------------------------------

    /**
     * Tente d'activer la serrure avec un objet précis (ex: sa clé).
     * @param obj l'objet essayé
     */
    public void activerAvec(Objet obj) throws ActivationImpossibleAvecObjetException { 
        if(!this.activableAvec(obj)){
            throw new ActivationImpossibleAvecObjetException("Non activable avec cet objet.") ;
        }
        else{
            if(this.getEtat().equals(Etat.VERROUILLE)){
                this.etat = Etat.DEVERROUILLE;
            }
            else if(this.getEtat().equals(Etat.DEVERROUILLE)){
                this.etat = Etat.VERROUILLE;
            }
        }
    }

    //-------------------------------------------------------------------------------------------------------------------

    /**
     * Forge la toute première clé qui correspondra à cette serrure exacte.
     * Ne marche qu'une fois.
     * @return la nouvelle clé créée, ou null si elle a déjà été créée
     */
    public Cle creerCle() throws NomDEntiteDejaUtiliseDansLeMondeException {
        if(this.cle != null){
            return null;
        }
        else {
            this.cle = new Cle(this.getMonde().genererNom("Cle_"), this.getMonde());
            return this.cle;
        }
    }

    //-------------------------------------------------------------------------------------------------------------------

    /**
     * Fournit un résumé texte de la serrure (nom, état, et sa clé).
     * @return la description de la serrure
     */
    public String toString(){
        String s;
        s = "\n" + "#------------------" + " Serrure ------------------#" + "\n";
        s += "Nom : " +  this.getNom() + "\n";
        s += "Etat: " + this.getEtat() + "\n";
        s += "Cle: " + this.cle.toString() + "\n";
        s += "#------------------------------------------------------#";
        return s;
    }
}
