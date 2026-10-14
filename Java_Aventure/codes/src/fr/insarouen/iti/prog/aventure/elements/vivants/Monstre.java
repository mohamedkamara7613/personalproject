package fr.insarouen.iti.prog.aventure.elements.vivants;


import fr.insarouen.iti.prog.aventure.elements.structure.Piece;
import fr.insarouen.iti.prog.aventure.Monde;
import fr.insarouen.iti.prog.aventure.elements.structure.Porte;
import fr.insarouen.iti.prog.aventure.elements.objets.Objet;
import fr.insarouen.iti.prog.aventure.elements.Etat;
import java.util.Optional;
import java.util.Collection;



import fr.insarouen.iti.prog.aventure.ITIAventureException;
import fr.insarouen.iti.prog.aventure.NomDEntiteDejaUtiliseDansLeMondeException;

/**
 * Créature errante, elle perd de la vie petit à petit et se promène au hasard dans le monde.
 */
public class Monstre extends Vivant{

    //####################################################### Constructeurs #######################################################

    /**
     * Invoque un monstre avec ses stats et la pièce où on le place au début.
     * 
     * @param nom le nom de la bête
     * @param monde le monde du monstre
     * @param pointVie sa santé de départ
     * @param pointForce sa force brute
     * @param piece l'endroit de départ
     */
    public Monstre(String nom, Monde monde, int pointVie, int pointForce, Piece piece) throws NomDEntiteDejaUtiliseDansLeMondeException{
        super(nom, monde, pointVie, pointForce, piece);
    }

    //####################################################### Methodes #######################################################

    /**
     * Cycle de vie par défaut du monstre.
     * À chaque tour il perd un PV, cherche une porte praticable, la franchit si possible
     * et s'amuse à vider son sac pour tout échanger avec les objets présents par terre dans la nouvelle pièce.
     */
    public void executer() throws ITIAventureException{
        
        /*S’il est vivant :
        — perd 1 point de vie
        — cherche une porte ouverte ou fermée (OUVERT/FERME)
        Utilisez les stream pour rechercher la porte
        — franchit la porte en l’ouvrant si nécessaire
        — s’il arrive à changer de pièce alors il échange les objets de son inven-
        taire avec ceux de la pièce */

        if(!this.estMort()){
            // perd 1 point de vie
            this.setPointVie(this.getPointVie()-1);

            // cherche une porte ouverte ou ferme
            Optional<Porte> porteTrouve = this.getPiece().getPortes().stream()      
            .filter(p -> p.getEtat() == Etat.OUVERT || p.getEtat() == Etat.FERME) 
            .findFirst(); 
            
            // L'Optional est une "boîte", on doit vérifier si elle est pleine, puis en extraire la porte
            if (porteTrouve.isPresent()) {
                Porte porte = porteTrouve.get();

                // si la porte est ferme, on essaie de l'ouvrir
                if(porte.getEtat() == Etat.FERME){
                    try {
                        porte.activer();
                    } catch(Exception e) {
                        return;
                    }
                }

                //  piece precedente
                Piece piecePrec = this.getPiece();

                // franchir la porte
                try {
                    this.franchir(porte);
                } catch(Exception e) {
                    return;
                }

                // verifier si on a changé de piece
                if(!piecePrec.equals(this.getPiece())){
                    Collection<Objet> objetsPiece = this.getPiece().getObjets();
                    Collection<Objet> objetsInventaire = this.getObjets();

                    // déposer
                    for(Objet obj : objetsInventaire){
                        try { 
                            this.deposer(obj); 
                        } catch(Exception e) {}
                    }
                    // prendre
                    for(Objet obj : objetsPiece){
                        try { 
                            this.prendre(obj); 
                        } catch(Exception e) {}
                    }
                }
            }
        }
    }

    //-------------------------------------------------------------------------------------------------------------------

    /**
     * Résume la bête en affichant l'intégralité des informations de type Vivant, adaptées pour signaler qu'il s'agit d'un monstre.
     * 
     * @return fiche signalétique du monstre
     */
    @Override
    public String toString() {
        return super.toString().replace("VIVANT", "MONSTRE");
    }
}

