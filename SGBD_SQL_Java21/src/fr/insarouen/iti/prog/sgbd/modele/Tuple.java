package fr.insarouen.iti.prog.sgbd.modele;

import java.io.Serializable;
import java.util.AbstractList;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Objects;
import java.util.stream.Collectors;


/**
 * Représente un tuple (une ligne de données) dans une table.
 * Implément la liste de Valeur via AbstractList pour un accès direct
 * aux valeurs avec toutes les opérations de liste standard. 
 * Sans avoir à tout redéfinir
 * 
 * * @author Elakoum 
 * @version 2.0
 */


public class Tuple extends AbstractList<Valeur> implements Serializable {
    private final List<Valeur> values;// Un tuple ne change pas 

    public Tuple(List<Valeur> values){
        this.values=new ArrayList<>(values); 

    }

    /**
     * 
     * @param index indice de l'attribut dans la table 
     * @return la valeur associer a cette attribut
     */
    @Override
    public Valeur get(int index) {
        return this.values.get(index);
    }


    /**
     * Retourne le nombre de valeurs dans ce tuple.
     *
     */
    @Override
    public int size() {
        return this.values.size();
    }

    
     /**
     * @return contenu d'un tuple (déboggage)
     */
    public String toString() {
        return this.values.stream()
        .map(v -> v.getDonnee().toString())
        .collect(Collectors.joining(", ", "[", "]"));
    }
    /**
     * @return si deux tuples sont identiques
     */
    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof Tuple)) return false;
        Tuple autre = (Tuple) o;
        return this.values.equals(autre.values); // délègue au equals de Valeur
    }
    /**
     * @return le hashcode d'un tuple
     */
    @Override
    public int hashCode() {
        return Objects.hash(this.values);
    }
}