package fr.insarouen.iti.prog.sgbd.expressions;

import fr.insarouen.iti.prog.sgbd.modele.Table;
import fr.insarouen.iti.prog.sgbd.modele.Tuple;
import fr.insarouen.iti.prog.sgbd.modele.Valeur;
import fr.insarouen.iti.prog.sgbd.exceptions.*;
public class ConditionSimple {
    private Operande operandegauche;
    private Operande operandedroite;
    private Operateur op;

    public ConditionSimple(Operande gauche, Operateur op, Operande droite) {
        this.operandegauche = gauche;
        this.operandedroite = droite;
        this.op = op;
    }

    /**
     * Évalue la condition simple sur un tuple donné.
     * @param t le tuple sur lequel on évalue la condition
     * @param table la table contenant les métadonnées des colonnes
     * @return true si la condition est satisfaite, false sinon
     * @throws AttributInconnuException si une colonne n'existe pas dans la table
     */
    public boolean evaluerCondition(Tuple t, Table table) throws AttributInconnuException,TypesIncompatibleException {
        Valeur valG = this.operandegauche.evaluer(t, table);
        Valeur valD = this.operandedroite.evaluer(t, table);
        int cmp = valG.compareTo(valD);
        switch (this.op) {
            case EGAL:
                 return cmp == 0;
            case SUP: 
             return cmp > 0;
            case INF:
                return cmp < 0;
            default: 
            throw new IllegalStateException("Opérateur inconnu");
        }
    }


    
}