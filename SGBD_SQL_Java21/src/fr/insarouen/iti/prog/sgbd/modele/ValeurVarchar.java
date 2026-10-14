package fr.insarouen.iti.prog.sgbd.modele;
import fr.insarouen.iti.prog.sgbd.modele.Type;
import fr.insarouen.iti.prog.sgbd.modele.Valeur;
import fr.insarouen.iti.prog.sgbd.exceptions.TypesIncompatibleException;
/**
 * Valeur de type chaîne de caractères ({@link Type#VARCHAR}) stockée dans le SGBD.
 * <p>
 * Encapsule une {@link String} et fournit les opérations définies par
 * {@link Valeur} : accès à la donnée, comparaison avec une autre valeur et
 * vérification de compatibilité de type.
 * </p>
 *
 * @see Type#VARCHAR
 * @see Valeur
 */
public class ValeurVarchar extends Valeur {

    private String valeur;

    /**
     * Construit une valeur chaîne de caractères.
     *
     * @param valeur la chaîne à stocker
     */
    public ValeurVarchar(String valeur) {
        super(Type.VARCHAR);
        this.valeur = valeur;
    }

    /**
     * Retourne la chaîne de caractères encapsulée.
     *
     * @return la valeur sous forme de {@link String}
     */
    @Override
    public String getDonnee() {
        return this.valeur;
    }

    /**
     * Compare cette valeur à une autre valeur du SGBD selon l'ordre lexicographique.
     *
     * @param autre la valeur à comparer
     * @return un entier négatif, zéro ou positif selon que cette chaîne est
     *         lexicographiquement inférieure, égale ou supérieure à {@code autre}
     * @throws TypesIncompatibleException si {@code autre} n'est pas un {@link ValeurVarchar}
     */
    public int compareTo(Valeur autre) throws TypesIncompatibleException {
        if (!(autre instanceof ValeurVarchar)) {
            throw new TypesIncompatibleException(String.format("Le type attendu : VAECHAR, type reçu : %s", autre.getType() == Type.INT ? "INT" : "SERIAL" ));
        }
        ValeurVarchar autreVarchar = (ValeurVarchar) autre;
        return this.valeur.compareTo(autreVarchar.getDonnee());
    }

    /**
     * Indique si cette valeur est compatible avec le type donné.
     *
     * @param t le type à vérifier
     * @return {@code true} uniquement si {@code t} est {@link Type#VARCHAR}
     */
    public boolean estCompatible(Type t) {
        return t == Type.VARCHAR;
    }

    @Override
    public boolean equals(Object obj) {
        if (this == obj) return true;
        if (obj == null || !(obj instanceof ValeurVarchar)) return false;
        ValeurVarchar other = (ValeurVarchar) obj;
        return this.valeur.equals(other.valeur);
    }

    @Override
    public int hashCode() {
        return this.valeur.hashCode();
    }

    @Override
    public String toString() {
        return this.valeur;
    }
}