package fr.insarouen.iti.prog.aventure.conditions;


import java.util.ArrayList;
import java.util.Iterator;
import java.util.Collections;
import fr.insarouen.iti.prog.aventure.elements.vivants.Vivant;
import fr.insarouen.iti.prog.aventure.elements.objets.Objet;


public class ConditionDeFinVivantPossedeObjets extends ConditionDeFin {
    
    private ArrayList<Objet> objets = new ArrayList<>();
    private Vivant vivant ;
    public ConditionDeFinVivantPossedeObjets(EtatDuJeu etat, Vivant vivant, Objet... objets) {
        super(etat);
        this.vivant = vivant;
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

        if(oui){
            return this.getEtatSiConditonVerifiee();
        }

        return EtatDuJeu.ENCOURS;
    }
}