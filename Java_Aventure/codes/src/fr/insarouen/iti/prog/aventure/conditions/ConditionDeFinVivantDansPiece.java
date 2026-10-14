package fr.insarouen.iti.prog.aventure.conditions;

import fr.insarouen.iti.prog.aventure.elements.vivants.Vivant;
import fr.insarouen.iti.prog.aventure.elements.structure.Piece;



public class ConditionDeFinVivantDansPiece extends ConditionDeFin {
    private Vivant vivant;
    private Piece piece ; 

    public ConditionDeFinVivantDansPiece(EtatDuJeu etat, Vivant vivant, Piece piece){
        super(etat);
        this.vivant = vivant;
        this.piece = piece;
    }

    @Override
    public EtatDuJeu verifierCondition(){
        if(this.vivant.getPiece().equals(this.piece)){
            return this.getEtatSiConditonVerifiee();
        }
        return EtatDuJeu.ENCOURS;
    }
}