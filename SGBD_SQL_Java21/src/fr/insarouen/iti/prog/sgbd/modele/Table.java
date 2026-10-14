package fr.insarouen.iti.prog.sgbd.modele;

import fr.insarouen.iti.prog.sgbd.exceptions.AttributInconnuException;
import fr.insarouen.iti.prog.sgbd.exceptions.TupleInconnuException;

import fr.insarouen.iti.prog.sgbd.exceptions.TypesIncompatibleException;
import fr.insarouen.iti.prog.sgbd.expressions.ExpressionLogique;

import java.io.Serializable;
import java.lang.reflect.Array;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.HashSet;
import java.util.Collection;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Set;

/**
 * Représente une table au sein d'une base de données relationnelle.
 * Une table possède un nom unique et contient un ensemble de tuples
 * respectant une structure d'attributs définie.
 *
 * @author Elakoum
 * @version 1.0
 */
public class Table implements Serializable {
    /*
     * Le nom de la table dans une base de donne ce nom la est unique pour chaque
     * table
     */

    private String nom;
    
    private LinkedHashSet<Attribut> attributs;
    private List<Tuple> tuples;

    /**
     * Construction d'une table vide 
     * Lors de la creation dune table en fait CREATE NOM (aat1,att2,att3)
     * @param nom tab a creer
     * @param attributs contient la liste d'attributs à ajouter
     */

    public Table(String nom, Collection<Attribut> attributs) { // en se basant sur lexemple de crearion d'une table de fichier exemple du moodle
    
        this.nom = nom;
        this.attributs = new LinkedHashSet<>(attributs);
        this.tuples = new ArrayList<>();
    }

    /**
     * Permet linsertion de tuple dans une table
     * 
     * @param t Tuple qui contient des valeur d'attribut
     */
    public void insererTuple(Tuple t){ // a verifier que les valeur inserer sont bien les attribut demander 
        this.tuples.add(t);
    }

    /***
     * 
     * @param tuplesASupprimer
     * @return retourne le nb tuple qui sont supprimer
     */
    public int supprimerTuples(List<Tuple> tuplesASupprimer) throws TupleInconnuException {

        // Vérfications pour eviter de perdre de l'information

        for (Tuple t : tuplesASupprimer) {
            if (!this.tuples.contains(t)) {
                throw new TupleInconnuException(String.format("Le tuple %s n'existe pas ", t.toString()));
            }
        }
        // suppression
        int tailleAvant = this.tuples.size();
        this.tuples.removeAll(tuplesASupprimer);
        int tailleApres = this.tuples.size();

        return tailleAvant - tailleApres; // La différence nous donne le nombre de lignes supprimées
    }

    /**
     * 
     * @return retourne la liste des tuples de la tables
     * 
     */
    public List<Tuple> getTuples() {
        return Collections.unmodifiableList(this.tuples);
    }

    /**
     * @param nom
     * @return l 'attribut dont il ya le nom nom
     */
    public Attribut getAttribut(String nom) throws AttributInconnuException {// la je pene il sera mieux si en ceera uen
                                                                             // exception pour dire si l'attrinbut
                                                                             // exuste ou pas

        for (Attribut att : this.attributs) {
            if (nom.equals(att.nom())) {
                return att;
            }
        }
        throw new AttributInconnuException(nom);// ici en doit enlever
    }

    /**
     * Affiche le schéma complet d'une table
     * 
     * @return l 'attribut dont il ya le nom nom
     */

    public Set<Attribut> getAttributs() {
        return Collections.unmodifiableSet(this.attributs);
    }

    /***
     * 
     * @param nom
     * @return un boolean en indiquant si l attribut avec ce nom la existe ou pas
     */
    public boolean attributExiste(String nom) {
        for (Attribut att : this.attributs) {
            if (nom.equals(att.nom())) {
                return true;
            }
        }
        return false; // dapres la java doc cette methode retourn true si existe false si non
    }

    /***
     * Pour obtenir l'indice dun attribut pour gerer apres le auto incremente
     * 
     * @param nom
     * @return lindice de l'attribut possedent le nom nom
     */
    public int indexAttribut(String nom) throws AttributInconnuException {
        Attribut att = this.getAttribut(nom); // lève AttributInconnuException si absent

        List<Attribut> liste = new ArrayList<>(this.attributs);
        return liste.indexOf(att);
    }

    /**
     * @return le nom de la table
     */
    public String getNom() {
        return this.nom;
    }
    
    /**
     * Permet d'ajouter un attribut (unbe colonne) au schma de la table
     * 
     * @param a L'attribut à ajouter
     */
    public void addAttribut(Attribut a) {
        this.attributs.add(a);
    }

    /**
     * Méthode permettant la gestions des alias 
     * Crée une table où tous les attributs sont préfixé par l'alias
     *
     * @param prefixe le préfixe (alias ou nom de table)
     * @return la nouvelle table préfixée
     */
    public Table renommerAvecPrefixe(String prefixe){
        List<Attribut> attrPrefixe = new ArrayList<>(); 
        for (Attribut attr : this.attributs){
            attrPrefixe.add(new Attribut(prefixe+"."+attr.nom(),attr.type()));
        }
        Table res = new Table(prefixe, attrPrefixe);
        for (Tuple t : this.tuples){
            res.insererTuple(t);
        }
        return res; 
    }
}