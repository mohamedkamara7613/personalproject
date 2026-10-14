package fr.insarouen.iti.prog.aventure.data;

import fr.insarouen.iti.prog.aventure.Monde;
import java.util.Collection;
import fr.insarouen.iti.prog.aventure.conditions.ConditionDeFin;


public interface Enregistreur {

    public void enregistrer(Monde monde,  Collection<ConditionDeFin> conditionsDeFin) throws Throwable;

}