package fr.insarouen.iti.prog.sgbd.modele;

import fr.insarouen.iti.prog.sgbd.modele.Type;

import java.io.Serializable;

import fr.insarouen.iti.prog.sgbd.exceptions.TypesIncompatibleException;


public abstract class Valeur implements Serializable{
    
    private Type type; 

    public Valeur(Type type){
        this.type = type; 

    }

    public Type getType(){
        return type;
    }

    public abstract Object getDonnee();
    public abstract int compareTo(Valeur autre) throws TypesIncompatibleException;
    public abstract boolean estCompatible(Type t);
    
}