package fr.insarouen.iti.prog.aventure.elements;


import fr.insarouen.iti.prog.aventure.elements.objets.Objet;


public interface Activable {

    public boolean activableAvec(Objet obj) ;

    public void activer() throws ActivationException;

    public void activerAvec(Objet obj) throws ActivationException;

}