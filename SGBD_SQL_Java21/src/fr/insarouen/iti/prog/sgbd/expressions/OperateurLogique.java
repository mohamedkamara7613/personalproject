package fr.insarouen.iti.prog.sgbd.expressions;

/**
 * Opérateurs logiques binaires utilisés pour combiner des {@link ConditionSimple}
 * au sein d'une {@link ExpressionLogique}.
 *
 * <p>La conversion depuis une chaîne SQL est assurée par
 * {@link Enum#valueOf(Class, String)} (insensible à la casse côté parseur) :</p>
 * <pre>
 *   OperateurLogique op = OperateurLogique.valueOf("AND"); // → AND
 * </pre>
 */
public enum OperateurLogique {
    AND,
    OR;
}