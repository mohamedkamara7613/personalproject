package fr.insarouen.iti.prog.aventure.data;

import java.io.Reader;
import java.io.FileReader ;


public class testeur{
    public static void main(String[] args){
        try{Reader reader = new FileReader("exemplesimulation1.aa");
        Lecteur lecteur = new LecteurDescription(reader);
        //Monde monde = lecteur.getMonde();
        // faites les affichages n´ecessaires pour v´erifier votre travail
    }
    catch (Exception ex){
        ex.printStackTrace();
    }}
}