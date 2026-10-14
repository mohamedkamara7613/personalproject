package fr.insarouen.iti.prog.sgbd.data;

import fr.insarouen.iti.prog.sgbd.modele.BaseDeDonnees;

import java.io.IOException;
import java.util.Collection;

/**
 * Contrat pour persister l'état d'une partie (monde + conditions de fin).
 */
public interface Enregistreur{

    /**
     * Sauvegarde le monde et les conditions de fin.
     *
     * @param bd La base de données
     * @throws IOException En cas d'erreur d'écriture.
     */
    public abstract void enregistrer(BaseDeDonnees bd, String chemin) throws IOException;
}