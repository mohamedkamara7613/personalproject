
package fr.insarouen.iti.prog.sgbd.expressions;

import java.util.*;

import fr.insarouen.iti.prog.sgbd.exceptions.AttributInconnuException;
import fr.insarouen.iti.prog.sgbd.exceptions.TypesIncompatibleException;
import fr.insarouen.iti.prog.sgbd.modele.Table;
import fr.insarouen.iti.prog.sgbd.modele.Tuple;

public class ExpressionLogique {
    /***
     * Une expression Logique est compser de conditon simple 
     * qui sont relier par des operateur logique 
     
     */
    private List<ConditionSimple> conditions;
    private List<OperateurLogique> operateurs;

    public ExpressionLogique(){
        this.conditions=new ArrayList<>();
        this.operateurs=new ArrayList<>();
     
    }

    /**
     * Pour l ajout de conditon simples dans la list 
     * des conditons simple de LexpressionSimple
     * @param c cest just la conditon simple 
     */
    public void ajouterCondition(ConditionSimple c){

        this.conditions.add(c);

    }


    /**
     * Dans le cas ou notre requet et compose de deux condition ou plus
     * @param op operateur logique
     * @param c conditon simple
     */
    public void ajouterOperateurEtCondition(OperateurLogique op, ConditionSimple c){
        this.operateurs.add(op);
        this.ajouterCondition(c);

    }
    /**
     * 
     * @param t tuple
     * @param table Table
     * @return Retourne le resultat de lexpression logique
     * @throws AttributInconnuException pour evaluerCondition
     * @throws TypesIncompatibleException pour evaluer condition 
     */

    public boolean evaluerexpression(Tuple t,Table table) throws AttributInconnuException, TypesIncompatibleException {

        boolean res = this.conditions.get(0).evaluerCondition(t, table);// la je recupere le resultat de la premiere conditon et jai decder de le faire la car comme ca si il ya pas doperateur logique le res soit retourner

        ConditionSimple cond;
        OperateurLogique opera;
        
        for (int i = 0; i < this.operateurs.size(); i++) {// pour parcourir tous les operateurs logique

            cond= this.conditions.get(i+1);
            opera=this.operateurs.get(i);

            if(opera.equals(OperateurLogique.AND) ){

                res = res && cond.evaluerCondition(t, table); // apre recuperer une condition simple a index i en la compare avec i+1 qui est recuperer avant 
            }else if(opera.equals(OperateurLogique.OR)){

              res = res || cond.evaluerCondition(t, table);

            }

        
          }
          
        return res;
    }






    
}