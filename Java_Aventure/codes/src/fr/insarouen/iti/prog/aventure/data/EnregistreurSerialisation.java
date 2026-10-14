package fr.insarouen.iti.prog.aventure.data;

import java.io.ObjectOutputStream;
import fr.insarouen.iti.prog.aventure.Monde;
import java.util.Collection;
import fr.insarouen.iti.prog.aventure.conditions.ConditionDeFin;


import java.io.IOException;

public class EnregistreurSerialisation extends Object implements Enregistreur {
    private ObjectOutputStream oos;

    public EnregistreurSerialisation(ObjectOutputStream oos) {
        this.oos = oos;
    }

    @Override
    public void enregistrer(Monde monde,  Collection<ConditionDeFin> conditionsDeFin) throws IOException {
        this.oos.writeObject(monde);
        this.oos.writeObject(conditionsDeFin);
    }
}