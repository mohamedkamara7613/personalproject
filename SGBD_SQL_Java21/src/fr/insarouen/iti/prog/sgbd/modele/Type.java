package fr.insarouen.iti.prog.sgbd.modele;

/**
 * Énumération représentant les types de données supportés par le SGBD.
 * <p>
 * Chaque constante correspond à un type SQL et est utilisée pour typer les
 * {@link Attribut attributs} d'une {@link Table table} et valider la cohérence
 * des {@link Valeur valeurs} qui y sont insérées.
 * </p>
 *
 * @see Attribut
 * @see Valeur
 */
public enum Type {

    /**
     * Type entier signé ({@code INTEGER} en SQL).
     * Correspond aux valeurs portées par {@link ValeurInt}.
     */
    INT,

    /**
     * Type chaîne de caractères de longueur variable ({@code VARCHAR} en SQL).
     * Correspond aux valeurs portées par {@link ValeurVarchar}.
     */
    VARCHAR,

    /**
     * Type entier auto-incrémenté ({@code SERIAL} en SQL / PostgreSQL).
     * Utilisé typiquement pour les clés primaires générées automatiquement et gérer l'auto-incrémentation.
     */
    SERIAL
}