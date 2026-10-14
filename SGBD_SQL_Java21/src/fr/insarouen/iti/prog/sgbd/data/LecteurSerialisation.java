package fr.insarouen.iti.prog.sgbd.data;

import fr.insarouen.iti.prog.sgbd.modele.BaseDeDonnees;

import java.io.FileInputStream;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.util.Collection;


public class LecteurSerialisation implements Lecteur {

    /**
     * Renvoie la base chargé depuis la source de données.
     *
     * @return La {@link BaseDeDonnees} chargé.
     * @throws IOException            En cas d'erreur de lecture.
     * @throws ClassNotFoundException Si une classe sérialisée est introuvable.
     * @return null                   Dans le cas ou le fichier n'a pas été trouvé
     */
    @Override
    public BaseDeDonnees lire(String chemin) throws IOException, ClassNotFoundException{
        try(ObjectInputStream ois = new ObjectInputStream(new FileInputStream(chemin))){
            return (BaseDeDonnees) ois.readObject();
        }catch(IOException|ClassNotFoundException e){
            System.err.println("Erreur le fichier n'a pas pu être ouvert: " + e.getMessage());
            e.printStackTrace();
        };
        return null; 
    };



}