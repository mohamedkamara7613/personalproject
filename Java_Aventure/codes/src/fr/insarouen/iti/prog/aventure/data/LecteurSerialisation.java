package fr.insarouen.iti.prog.aventure.data;

import java.io.ObjectInputStream;
import java.lang.ClassNotFoundException;
import fr.insarouen.iti.prog.aventure.Monde;
import java.util.ArrayList;
import java.util.Collection;
import fr.insarouen.iti.prog.aventure.conditions.ConditionDeFin;

import java.io.IOException;

public class LecteurSerialisation extends Object implements Lecteur {
    private ObjectInputStream ois;
    private Monde monde;
    private Collection<ConditionDeFin> list_ConditonsDeFin = new ArrayList<>();
    public LecteurSerialisation(ObjectInputStream ois) throws ClassNotFoundException, IOException {
        this.ois = ois;
        this.monde = (Monde)this.ois.readObject();
        this.list_ConditonsDeFin = (Collection<ConditionDeFin>)this.ois.readObject();
    }

    @Override
    public Monde getMonde(){
        return this.monde;
    }

    public Collection<ConditionDeFin> getConditionsDeFin(){
        return list_ConditonsDeFin;
    }
}