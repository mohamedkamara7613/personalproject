package fr.insarouen.iti.prog.aventure.data;

import java.io.Reader;
import java.lang.Object;
import java.util.Scanner;
import java.util.ArrayList;
import java.lang.Integer;
import java.util.Collection;

import fr.insarouen.iti.prog.aventure.Monde;
import fr.insarouen.iti.prog.aventure.conditions.EtatDuJeu;
import fr.insarouen.iti.prog.aventure.elements.structure.Piece;
import fr.insarouen.iti.prog.aventure.elements.structure.Porte;
import fr.insarouen.iti.prog.aventure.elements.objets.serrurerie.Serrure;
import fr.insarouen.iti.prog.aventure.elements.vivants.JoueurHumain;
import fr.insarouen.iti.prog.aventure.elements.objets.Objet;
import fr.insarouen.iti.prog.aventure.elements.Entite;
import fr.insarouen.iti.prog.aventure.conditions.ConditionDeFinVivantDansPiece;
import fr.insarouen.iti.prog.aventure.conditions.ConditionDeFin;






import java.io.IOException;
import fr.insarouen.iti.prog.aventure.NomDEntiteDejaUtiliseDansLeMondeException;
import fr.insarouen.iti.prog.aventure.ITIAventureException;



public class LecteurDescription extends Object implements Lecteur {
    private Monde monde;
    private Collection<ConditionDeFin> list_ConditonsDeFin = new ArrayList<>();

    public LecteurDescription(Reader reader) throws IOException, NomDEntiteDejaUtiliseDansLeMondeException{
        super();
        

        try (Scanner scanner = new Scanner(reader)) {
            while (scanner.hasNextLine()) {
                Scanner line = new Scanner(scanner.nextLine());
                line.useDelimiter(" ");
                //System.out.println(String.format("%s, %s",line.next("Monde"), line.next()));

                ArrayList<String> list_mot = new ArrayList<>();
                while (line.hasNext()) {
                    list_mot.add(line.next());
                }
                
                switch (list_mot.get(0)){
                    case "Monde":
                        String nom = list_mot.get(1);
                        //System.out.println(String.format("Un monde de nom : %s", nom));
                        this.monde = new Monde(nom);
                        break;
                    case "Piece":
                        String nom_piece = list_mot.get(1);
                        //System.out.println(String.format("Une piece de nom : %s", nom_piece));
                        this.createPiece(nom_piece);
                        break;
                    case "PorteSerrure":
                        this.createPorteSerrure(list_mot.get(1), list_mot.get(2), list_mot.get(3));
                        break;
                    case "Porte":
                        this.createPorte(list_mot.get(1), list_mot.get(2), list_mot.get(3));
                        break;
                    case "Cle":
                        this.placeCle(list_mot.get(1), list_mot.get(2));
                        break;
                    case "JoueurHumain":
                        this.createJoueurHumain(list_mot.get(1), list_mot.get(2), list_mot.get(3), list_mot.get(4));
                        break;
                    case "ConditionDeFinVivantDansPiece":
                        this.createConditionDeFinVivantDansPiece(list_mot.get(1), list_mot.get(2), list_mot.get(3));
                        break;
                    default:
                        break;
                }

                // System.out.println(String.format("Une ligne -------------------------"));

                // for(String m: list_mot){
                //     System.out.println(String.format("Un mot %s", m));

                // }
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public Monde getMonde() {
        return this.monde;
    }

    public Collection<ConditionDeFin> getConditionsDeFin(){
        return this.list_ConditonsDeFin; // il serait mieux de faire une copie
    }

    private Piece createPiece(String nom_piece)throws ITIAventureException{
        Piece piece = new Piece(nom_piece, this.monde);
        return piece;
    }

    private Porte createPorteSerrure(String nom_porte, String nom_pieceA, String nom_pieceB) throws ITIAventureException{
        //if(this.getMonde() != null){
            // Piece pieceA = new Piece(nom_pieceA, this.getMonde());
            // Piece pieceB = new Piece(nom_pieceB, this.getMonde());
            Serrure serrure = new Serrure(this.getMonde());
            Porte porte_serrure = new Porte(nom_porte, this.getMonde(), serrure, (Piece)this.getMonde().getEntite(nom_pieceA), (Piece)this.getMonde().getEntite(nom_pieceB));
            return porte_serrure;
        //}
    }

    private Porte createPorte(String nom_porte, String nom_pieceA, String nom_pieceB) throws ITIAventureException{
        //if(this.getMonde() != null){
            // Piece pieceA = new Piece(nom_pieceA, this.getMonde());
            // Piece pieceB = new Piece(nom_pieceB, this.getMonde());
            Porte porte = new Porte(nom_porte, this.getMonde(), (Piece)this.getMonde().getEntite(nom_pieceA), (Piece)this.getMonde().getEntite(nom_pieceB));
            return porte;
        //}
    }

    private JoueurHumain createJoueurHumain(String nom, String pointVie, String pointForce, String nom_piece) throws ITIAventureException{
        // Piece piece = new Piece(nom_piece, this.getMonde());
        JoueurHumain player = new JoueurHumain(nom, this.getMonde(), Integer.parseInt(pointVie), Integer.parseInt(pointForce), (Piece)this.getMonde().getEntite(nom_piece));
        return player;
    }

    private void placeCle(String nom_porte, String nom_piece) throws ITIAventureException {
        //Entite ne peut etre convertit en Porte ou piece.
        Porte porte = (Porte)this.getMonde().getEntite(nom_porte);
        Objet cle = porte.getSerrure().creerCle();
        Piece piece = (Piece)this.getMonde().getEntite(nom_piece);
        piece.deposer(cle);
    } 

    private void createConditionDeFinVivantDansPiece(String nom_etat, String nom_joueur, String nom_piece) throws ITIAventureException {
        Piece piece = (Piece)this.getMonde().getEntite(nom_piece);
        JoueurHumain joueur = (JoueurHumain)this.getMonde().getEntite(nom_joueur);
        this.list_ConditonsDeFin.add(new ConditionDeFinVivantDansPiece(EtatDuJeu.valueOf(nom_etat), joueur, piece));
    }
}