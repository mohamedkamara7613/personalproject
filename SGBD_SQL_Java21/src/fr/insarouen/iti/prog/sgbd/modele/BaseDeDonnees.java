package fr.insarouen.iti.prog.sgbd.modele;

import fr.insarouen.iti.prog.sgbd.exceptions.TableExistanteException;
import fr.insarouen.iti.prog.sgbd.exceptions.TableInconnueException;
import fr.insarouen.iti.prog.sgbd.exceptions.AttributInconnuException;
import fr.insarouen.iti.prog.sgbd.exceptions.BaseDeDonneesExistanteException;
import fr.insarouen.iti.prog.sgbd.exceptions.TypesIncompatibleException;
import fr.insarouen.iti.prog.sgbd.expressions.ExpressionLogique;
import fr.insarouen.iti.prog.sgbd.exceptions.BaseDeDonneesExistanteException;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.HashSet;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/**
 * Représentation de la base de données
 * Gestions de tables contenant des attributs et des tuples
 *
 * @author S.Maclean
 */
public class BaseDeDonnees implements Serializable{

    private String nom;
    private Map<String, Table> tables;
    private int compteurSerial;

    /**
     * Creation base de données vide.
     *
     * @param nom le nom de la base de données
     */
    public BaseDeDonnees(String nom)  {
       
        this.nom = nom;
        this.tables = new HashMap<>();
        this.compteurSerial = 0;
       
    }

    /**
     * Vérifie si une table existe dans la base.
     *
     * @param nom le nom de la table
     * @return true si la table existe, false sinon
     */
    public boolean tableExiste(String nom) {
        return this.tables.containsKey(nom.toLowerCase());
    }

    /**
     * Crée une nouvelle table dans la base.
     *
     * @param t la table à créer
     * @throws TableExistanteException si une table de même nom existe déjà
     */
    public void creerTable(Table t) throws TableExistanteException {
        if (this.tableExiste(t.getNom())) {
            throw new TableExistanteException(t.getNom());
        }
        this.tables.put(t.getNom().toLowerCase(), t);
    }

    /**
     * Supprime une table de la base.
     *
     * @param nom le nom de la table à supprimer
     * @throws TableInconnueException si la table n'existe pas
     */
    public void supprimerTable(String nom) throws TableInconnueException {
        if (!this.tableExiste(nom)) {
            throw new TableInconnueException(nom);
        }
        this.tables.remove(nom.toLowerCase());
    }

    /**
     * Retourne une table par son nom.
     *
     * @param nom le nom de la table
     * @return la table correspondante
     * @throws TableInconnueException si la table n'existe pas
     */
    public Table getTable(String nom) throws TableInconnueException {
        if (!this.tableExiste(nom)) {
            throw new TableInconnueException(nom);
        }
        return this.tables.get(nom.toLowerCase());
    }

    /**
     * Retourne la liste des noms de toutes les tables.
     *
     * @return liste non modifiable des noms de tables
     */
    public List<String> listerTables() {
        return Collections.unmodifiableList(new ArrayList<>(this.tables.keySet()));
    }

    /**
     * Incrémente et retourne le prochain identifiant SERIAL global.
     * Le compteur est partagé entre toutes les tables.
     *
     * @return le prochain entier SERIAL disponible
     */
    public int prochainSerial() {
        this.compteurSerial++;
        return this.compteurSerial;
    }

    /**
     * Retourne la valeur actuelle du compteur SERIAL global.
     *
     * @return la derniere valeur SERIAL utilisée
     */
    public int getCompteurSerial() {
        return this.compteurSerial;
    }

    /**
     * Restaure la valeur du compteur SERIAL global.
     * Cette methode est principalement utilisée lors du chargement
     * d'une base sauvegardée.
     *
     * @param compteurSerial la derniere valeur SERIAL deja utilisée
     */
    public void restaurerCompteurSerial(int compteurSerial) {
        if (compteurSerial < 0) {
            throw new IllegalArgumentException("Le compteur SERIAL ne peut pas etre negatif.");
        }
        this.compteurSerial = compteurSerial;
    }

    /**
     * Retourne une nouvelle table contenant uniquement les colonnes demandées,
     * dans l'ordre spécifié, avec tous les tuples de la table source.
     *
     * @param table la table source
     * @param nomsColonnes liste ordonnée des noms de colonnes à conserver
     * @return nouvelle table projetée
     * @throws AttributInconnuException si une colonne demandée est absente de la table
     */
    public Table projection(Table table, List<String> nomsColonnes) throws AttributInconnuException{ //Est ce qu'un contains ne serais pas plus pertinent 
        // On verifie que les colonnes existe avec index 
        List<Integer> indices = new ArrayList<>();
        List<Attribut> nouveauSchema = new ArrayList<>();
        List<Attribut> ancienSchema = new ArrayList<>(table.getAttributs()); 
        for (String nom : nomsColonnes){
            int idx = table.indexAttribut(nom); 
            indices.add(idx); 
            nouveauSchema.add(ancienSchema.get(idx)); 
        }
        // Nouvelle table résultat dans laquelle on va mettre les nouveaux tuples ù
        Table res = new Table(table.getNom()+"_projection", nouveauSchema); 


        //Projection de chaques tuples 
        for (Tuple ancien : table.getTuples()){
            List<Valeur> valeurs = new ArrayList<>(); 
            for(int idx : indices){
                valeurs.add(ancien.get(idx)); 
            }
            res.insererTuple(new Tuple(valeurs));
        }
        return res;
    }

    public Table produitCartesien(Table source, Table destination){
        // on crée une liste avec tous les attributs préfixés par leur nom de table
        List<Attribut> attributsFusion = new ArrayList<>();
        for (Attribut attr : source.getAttributs()) {
            String nouveauNom = attr.nom().contains(".") ? attr.nom() : source.getNom() + "." + attr.nom();
            attributsFusion.add(new Attribut(nouveauNom, attr.type()));
        }
        for (Attribut attr : destination.getAttributs()) {
            String nouveauNom = attr.nom().contains(".") ? attr.nom() : destination.getNom() + "." + attr.nom();
            attributsFusion.add(new Attribut(nouveauNom, attr.type()));
        }
        // on crée la nouvelle table
        String nomproduitcartesien = source.getNom() + "_" + destination.getNom();
        Table newtable = new Table(nomproduitcartesien , attributsFusion);
        // On parcours les tuples de la premiere table
        for (Tuple tupleSource : source.getTuples()){
            // On parcours les tuples de la deuxieme table
            for(Tuple tupledestination : destination.getTuples()){
                //on crée la liste des attributs des deux tables
                List<Valeur> valeursFusionnees = new ArrayList<>();
                // on ajoute les valeurs du premier tuple
                for (int i = 0; i < tupleSource.size(); i++) {
                    valeursFusionnees.add(tupleSource.get(i));
                }
                // on ajouter les valeurs du second tuple
                for (int i = 0; i < tupledestination.size(); i++) {
                    valeursFusionnees.add(tupledestination.get(i));
                }
                // Créer et insérer le nouveau tuple
                Tuple nouveauTuple = new Tuple(valeursFusionnees);
                newtable.insererTuple(nouveauTuple);
            }
        }
        return newtable;
    }

    /**
     * pplique une sélection sur les tuples en conservant uniquement ceux qui vérifient la condit iob
     * @param condition L'expression logique à évaluer
     * @return une nouvelle table contenant les tuples filtrés
     */
    public Table selection(Table table, ExpressionLogique condition) throws AttributInconnuException, TypesIncompatibleException {
        Table nouvelleTable = new Table(table.getNom()+"_selection", table.getAttributs());
        for (Tuple t : table.getTuples()) {
            if (condition.evaluerexpression(t, table)) {
                nouvelleTable.insererTuple(t);
            }
        }
        return nouvelleTable;
    }


    /**
     * jai ajouter cette methode pour la utiliser dans interupteur pour permeter a utilisateur de voir lea base qui a creer 
     */
    // public static void afficherBasesDeDonnees() {
    //     if (registre.isEmpty()) {
    //         System.out.println("Aucune base de données créée.");
    //         return;
    //     }
    //     System.out.println("Les bases de données créées sont :");
    //     for (String nom : registre.keySet()) { 
    //         System.out.println("  - " + nom);
    //     }
    // }

    // // pour récupérer une instance existante depuis l'Interpreteur
    // public static BaseDeDonnees getBase(String nom) {
    //     return registre.get(nom.toLowerCase());
    // }

    // // dans BaseDeDonnees.java
    // public static Map<String, BaseDeDonnees> getRegistre() {
    //     return Collections.unmodifiableMap(registre);
    // }

    /**
     * Retourne le nom de la base de données.
     *
     * @return le nom
     */
    public String getNom() {
        return this.nom;
    }


}