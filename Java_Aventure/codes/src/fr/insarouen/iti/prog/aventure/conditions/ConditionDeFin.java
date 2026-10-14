package fr.insarouen.iti.prog.aventure.conditions;

import java.io.Serializable;



public abstract class ConditionDeFin extends Object implements Serializable {

    private EtatDuJeu etat;

    public ConditionDeFin(EtatDuJeu etat) {
        this.etat = etat;
    }

    public  EtatDuJeu getEtatSiConditonVerifiee() {
        return this.etat;
    };

    public abstract EtatDuJeu verifierCondition();

}