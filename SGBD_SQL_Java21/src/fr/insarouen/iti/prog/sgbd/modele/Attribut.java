package fr.insarouen.iti.prog.sgbd.modele;

import java.io.Serializable;
import java.util.Objects;

public record Attribut(String nom, Type type)  implements Serializable{
        /**
         * Chaque attribut est caracterise par un nom et un type.
         * Ces élements de l'attributs ne peuvent être vide ou null
         * 
         * @param nom
         * @param type
         */

     public Attribut {
        if (nom == null || nom.isBlank())
            throw new IllegalArgumentException("Le nom d'un attribut ne peut pas être vide");
        if (type == null)
            throw new IllegalArgumentException("Le type d'un attribut ne peut pas être null");
    }

    /**
     * 
     * @return retourne la représentation textuelle de l'attribut 
     */
    public String toString() {
        return String.format("%s %s",this.nom, this.type);
    }
}
    
