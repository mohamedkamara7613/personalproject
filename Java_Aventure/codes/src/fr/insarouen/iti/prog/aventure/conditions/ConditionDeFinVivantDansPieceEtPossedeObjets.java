package fr.insarouen.iti.prog.aventure.conditions;


import java.util.ArrayList;
import java.util.Iterator;
import java.util.Collections;
import fr.insarouen.iti.prog.aventure.elements.vivants.Vivant;
import fr.insarouen.iti.prog.aventure.elements.objets.Objet;
import fr.insarouen.iti.prog.aventure.elements.structure.Piece;


public class ConditionDeFinVivantDansPieceEtPossedeObjets extends ConditionDeFin {
    private ArrayList<Objet> objets = new ArrayList<>();
    private Vivant vivant;
    private Piece piece ;
    
    public ConditionDeFinVivantDansPieceEtPossedeObjets(EtatDuJeu etat, Vivant vivant, Piece piece, Objet... objets){
        super(etat);
        this.vivant = vivant;
        this.piece = piece;
        Collections.addAll(this.objets, objets);
    }

    @Override
    public EtatDuJeu verifierCondition() {
        boolean oui = true;

        Iterator<Objet> it = this.objets.iterator();

        while( it.hasNext()){
            if(!this.vivant.possede(it.next())){
                oui = false;
            }
        }

        if(oui && this.vivant.getPiece().equals(this.piece)){
            return this.getEtatSiConditonVerifiee();
        }

        return EtatDuJeu.ENCOURS;
    }
}