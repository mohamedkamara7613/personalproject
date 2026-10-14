package fr.insarouen.iti.prog.sgbd.data;

import fr.insarouen.iti.prog.sgbd.modele.BaseDeDonnees; 

import java.io.IOException;
import java.util.Collection;


/**
 * Contrat pour charger l'état d'une partie (monde + conditions de fin).
 */
public interface Lecteur {
    /**
     * Renvoie la base chargé depuis la source de données.
     *
     * @return La {@link BaseDeDonnees} chargé.
     * @throws IOException            En cas d'erreur de lecture.
     * @throws ClassNotFoundException Si une classe sérialisée est introuvable.
     */
    public BaseDeDonnees lire(String chemin) throws IOException, ClassNotFoundException;



}