package fr.insarouen.iti.prog.sgbd.expressions;

import fr.insarouen.iti.prog.sgbd.modele.*;
import fr.insarouen.iti.prog.sgbd.exceptions.*;

/**
 * Représente un opérande dans une condition SQL (ex. : {@code age > 18}).
 *
 * Un opérande peut être :
 * <ul>
 *   <li>un nom de colonne ({@code COLONNE}),</li>
 *   <li>un entier littéral ({@code NOMBRE}),</li>
 *   <li>une chaîne littérale ({@code CHAINE}).</li>
 * </ul>
 */
public class Operande {

    /** Nature de l'opérande. */
    public enum TypeOperande {
        /** Référence à une colonne de la table courante. */
        COLONNE,
        /** Valeur entière constante. */
        NOMBRE,
        /** Valeur chaîne constante. */
        CHAINE
    }

    private TypeOperande type;
    private String nomColonne;
    private ValeurInt valeurNombre;
    private ValeurVarchar valeurChaine;

    /**
     * Crée un opérande de type colonne.
     *
     * @param nomColonne nom de la colonne référencée
     */
    public Operande(String nomColonne) {
        this.type = TypeOperande.COLONNE;
        this.nomColonne = nomColonne;
    }

    /**
     * Crée un opérande de type entier littéral.
     *
     * @param valeur valeur entière constante
     */
    public Operande(ValeurInt valeur) {
        this.type = TypeOperande.NOMBRE;
        this.valeurNombre = valeur;
    }

    /**
     * Crée un opérande de type chaîne littérale.
     *
     * @param valeur valeur chaîne constante
     */
    public Operande(ValeurVarchar valeur) {
        this.type = TypeOperande.CHAINE;
        this.valeurChaine = valeur;
    }

    /**
     * Retourne la nature de cet opérande.
     *
     * @return le {@link TypeOperande} associé
     */
    public TypeOperande getType() {
        return type;
    }

    /**
     * Retourne le nom de la colonne référencée.
     * Valide uniquement si {@link #getType()} == {@link TypeOperande#COLONNE}.
     *
     * @return le nom de la colonne
     */
    public String getNomColonne() {
        return nomColonne;
    }

    /**
     * Évalue cet opérande dans le contexte d'un tuple donné.
     *
     * <ul>
     *   <li>{@code COLONNE} — résout l'index de la colonne dans le schéma et retourne la valeur du tuple.</li>
     *   <li>{@code NOMBRE} / {@code CHAINE} — retourne directement la valeur constante.</li>
     * </ul>
     *
     * @param tuple le tuple en cours d'évaluation
     * @param table la table dont le schéma sert à résoudre les noms de colonnes
     * @return la {@link Valeur} résultante
     * @throws AttributInconnuException si le nom de colonne n'existe pas dans le schéma de la table
     */
    public Valeur evaluer(Tuple tuple, Table table) throws AttributInconnuException {
        switch (type) {
            case COLONNE:
                int index = table.indexAttribut(nomColonne);
                return tuple.get(index);
            case NOMBRE:
                return valeurNombre;
            case CHAINE:
                return valeurChaine;
            default:
                throw new IllegalStateException("Type d'opérande inconnu : " + type);
        }
    }
}
