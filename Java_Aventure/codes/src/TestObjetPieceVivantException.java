import fr.insarouen.iti.prog.aventure.Monde;
import fr.insarouen.iti.prog.aventure.ITIAventureException;
import fr.insarouen.iti.prog.aventure.elements.objets.Coffre;
import fr.insarouen.iti.prog.aventure.elements.objets.ObjetNonDeplacableException;
import fr.insarouen.iti.prog.aventure.elements.objets.PiedDeBiche;
import fr.insarouen.iti.prog.aventure.elements.structure.ObjetAbsentDeLaPieceException;
import fr.insarouen.iti.prog.aventure.elements.structure.Piece;
import fr.insarouen.iti.prog.aventure.elements.structure.VivantAbsentDeLaPieceException;
import fr.insarouen.iti.prog.aventure.elements.vivants.Vivant;
import fr.insarouen.iti.prog.aventure.elements.vivants.ObjetNonPossedeParLeVivantException;

public class TestObjetPieceVivantException {
    public static void main(String[] args) throws ITIAventureException {
	Monde m = new Monde("Le monde impitoyable d'ITI");
	Piece p = new Piece("Piece1", m);
	Vivant v = new Vivant("Vivant1", m, 10, 10, p, new PiedDeBiche("pieddecerf",m), new PiedDeBiche("pieddefaon", m));

	PiedDeBiche pdb = new PiedDeBiche("pdb", m);
	Coffre cfr = new Coffre("cfr", m);

	// ***** Test des exceptions liées aux Objets dans les pièces *****

	p.deposer(pdb);
	p.deposer(cfr);
	System.out.println(p);

	System.out.println("--- Test Piece Objet Déplaçable et dans la Pièce ---");
	p.retirer("pdb");
	System.out.println(p);

	System.out.println("--- Test Piece ObjetAbsentDeLaPieceException ---");
	try {
	    p.retirer("nexistepas");
	} catch(ObjetAbsentDeLaPieceException ex) {
	    ex.printStackTrace();
	}
	System.out.println(p);

	System.out.println("--- Test Piece ObjetNonDeplacableException ---");
	try {
	    p.retirer("cfr");
	} catch(ObjetNonDeplacableException ex) {
	    ex.printStackTrace();
	}
	System.out.println(p);

	// ***** Test des exceptions liées aux Objets dans les vivants *****

	System.out.println("--- Test Vivant ObjetAbsentDeLaPieceException ---");
	try {
	    v.prendre("nexistepas");
	} catch(ObjetAbsentDeLaPieceException ex) {
	    ex.printStackTrace();
	}
	System.out.println(p);

	System.out.println("--- Test Vivant ObjetNonDeplacableException ---");
	try {
	    v.prendre("cfr");
	} catch(ObjetNonDeplacableException ex) {
	    ex.printStackTrace();
	}
	System.out.println(p);

	System.out.println("--- Test Vivant ObjetNonPossedeParLeVivantException ---");
	try {
	    v.deposer("nexistepas");
	} catch(ObjetNonPossedeParLeVivantException ex) {
	    ex.printStackTrace();
	}
	System.out.println(p);

	System.out.println("--- Test Vivant déposer un objet ---");
	v.deposer("pieddecerf");

	System.out.println(p);

	System.out.println("--- Test Vivant prendre un objet ---");
	v.prendre("pieddecerf");

	System.out.println(p);

	Piece p2 = new Piece("Piece2", m);
	
	System.out.println("--- Test Vivant changement de pièce avec entrer ---");
	p2.entrer(v);
	System.out.println(p);
	System.out.println(p2);

	System.out.println("--- Test Vivant changement de pièce avec setPiece ---");
	v.setPiece(p);
	System.out.println(p);
	System.out.println(p2);

	System.out.println("--- Test Vivant sortie de pièce ---");
	p.sortir(v);
	System.out.println(p);
	System.out.println(v);

	System.out.println("--- Test Vivant changement de pièce avec entrer ---");
	p2.entrer(v);
	System.out.println(p);
	System.out.println(p2);

	System.out.println("--- Test Vivant sortie de pièce ---");
	p2.sortir(v);
	System.out.println(p2);
	System.out.println(v);

	System.out.println("--- Test Vivant changement de pièce avec setPiece ---");
	v.setPiece(p);
	System.out.println(p);
	System.out.println(v);

	System.out.println("--- Test de sortie d'un vivant d'une piece ou il n'est pas ---");
	try {
	    p2.sortir(v);
	} catch(VivantAbsentDeLaPieceException ex) {
	    ex.printStackTrace();
	}

	System.out.println("--- Tests terminés ---");
    }
}

