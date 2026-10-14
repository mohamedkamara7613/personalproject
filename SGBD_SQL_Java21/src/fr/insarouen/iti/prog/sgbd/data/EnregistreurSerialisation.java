package fr.insarouen.iti.prog.sgbd.data;
import fr.insarouen.iti.prog.sgbd.modele.BaseDeDonnees;

import java.io.FileOutputStream;
import java.io.IOException;
import java.io.ObjectOutputStream;
import java.util.Collection;


/**
 * Implémentation de {@link Enregistreur} par sérialisation Java.
 * <p>
 * Écrit la {@link BaseDeDonnees} puis les conditions de fin dans un
 * {@link ObjectOutputStream}.
 * </p>
 */
public class EnregistreurSerialisation  implements Enregistreur{

    /**
     * Sérialise la BD dans le chemin.
     * La méthode employé ferme automatiquement le fichier 
     *
     * @param bd          La base de donnée à sauvegarder.
     * @param chemin  Le chemin où stocker les données.
     * @throws IOException En cas d'erreur d'écriture.
     */
    @Override
    public void enregistrer(BaseDeDonnees bd, String chemin) throws IOException {
        try (ObjectOutputStream oos = new ObjectOutputStream(new FileOutputStream(chemin))) {
            oos.writeObject(bd);
        } catch (IOException e) {
            System.err.println("Erreur le fichier n'a pas pu être ouvert: " + e.getMessage());
            e.printStackTrace();
        } 
    }

}
