package fr.insarouen.iti.prog.sgbd.data;
import fr.insarouen.iti.prog.sgbd.modele.BaseDeDonnees;
import java.io.*;

public class GestionnaireStockage {

    private final Lecteur lecteur;
    private final Enregistreur enregistreur;

    public GestionnaireStockage(Lecteur lecteur, Enregistreur enregistreur) {
        this.lecteur = lecteur;
        this.enregistreur = enregistreur;
    }
    /**
     * Fonction qui permert de sauvegarder notre {@link BaseDeDonnees}
     * dans un fichier et d'afficher dans la sortie standart l'emplacemeent du fichier
     * 
     * @param chemin
     *
     */
    public void sauvegarder(BaseDeDonnees db, String chemin) throws IOException {
        this.enregistreur.enregistrer(db, chemin);
        System.out.println(String.format("La base est sauvegardé de %s :", chemin));;
    }

     /**
     * Fonction qui permert de récupéré la base de donnée
     * depuis un fichier 
     * 
     * @param chemin
     * @return @{@link BaseDeDonnees}
     */
    public BaseDeDonnees charger(String chemin) throws IOException, ClassNotFoundException {
        BaseDeDonnees db = this.lecteur.lire(chemin);
        System.out.println(String.format("La base est chargé de %s :", chemin));
        return db;
    }

    /**
     * Petite méthode utilitaire pour vérifier l'existence d'une base 
     * 
     * @param chemin
     * @return File
     */
    public static boolean baseExiste(String chemin) {
        return new File(chemin).exists();
    }
}