package fr.insarouen.iti.prog.sgbd.expressions;


/**
 * Ce sont les 3 valeurs possibles de operateur enum. 
 * Entre parenthèses je passe le symbole 
 *  c'est comme appeler un constructeur
 */
public enum Operateur { // ici jutilise enum pour creer une liste fixe de operateur car les operateur sont fixe 

    EGAL("="),
    SUP(">"),
    INF("<");

    private String symbole;

    Operateur(String symbole) {
        this.symbole = symbole;
    }

    /**
     * 
     * @return retourne simplement l'operateur exemple "="
     */
     public String getSymbole() {
        return this.symbole;
    }


    /**
     * 
     * @param s il prend en paramtre le symbole par exmple "=" 
     * @return il verifie si il existe dans notre enum et il retourne l enum associe EGAL 
     */
    public static Operateur fromString(String s) {
    for (Operateur op : Operateur.values()) { // retourne la liste de toutes les valeurs de l'enum [EGAL, SUP, INF]
        if (op.symbole.equals(s)) { 
            return op;
        }
    }
    throw new IllegalArgumentException("Opérateur inconnu : " + s);
    }
}