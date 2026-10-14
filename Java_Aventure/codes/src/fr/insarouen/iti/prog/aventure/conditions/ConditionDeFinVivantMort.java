package fr.insarouen.iti.prog.aventure.conditions;

import fr.insarouen.iti.prog.aventure.elements.vivants.Vivant;




public class ConditionDeFinVivantMort extends ConditionDeFin {

    private Vivant vivant;

    public ConditionDeFinVivantMort(EtatDuJeu etat, Vivant vivant){
        super(etat);
        this.vivant = vivant;
    }

    //public EtatDuJeu getEtatSiConditonVerifiee();

    @Override
    public EtatDuJeu verifierCondition(){
        if(this.vivant.estMort()) {
            return this.getEtatSiConditonVerifiee();
        }
        return EtatDuJeu.ENCOURS;
    }

}