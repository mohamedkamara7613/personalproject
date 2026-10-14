package fr.insarouen.iti.prog.aventure.elements.objets.serrurerie;

import fr.insarouen.iti.prog.aventure.Monde;
import fr.insarouen.iti.prog.aventure.elements.objets.Objet;
import fr.insarouen.iti.prog.aventure.NomDEntiteDejaUtiliseDansLeMondeException;

/**
 * Représente une clé qui permet d'utiliser une serrure correspondante.
 */
public class Cle extends Objet {

    //####################################################### Constructeurs #######################################################

    /**
     * Forge une nouvelle clé dans le monde spécifié.
     * @param nom le nom de la clé
     * @param monde le monde de la clé
     */
    public Cle(String nom, Monde monde) throws NomDEntiteDejaUtiliseDansLeMondeException {
        super(nom, monde);
    }

    //####################################################### Getters #######################################################

    /**
     * Vérifie si la clé peut être transportée par quelqu'un.
     * @return toujours vrai (une clé se met dans la poche)
     */
    @Override
    public boolean estDeplacable(){
        return true;
    }

    //####################################################### Methodes #######################################################
    
    /**
     * Renvoie le nom de la clé simplement.
     * @return le nom de la clé sous forme de texte
     */
    @Override
    public String toString(){
        String s;
        s = this.getNom();
        return s;
    }
}