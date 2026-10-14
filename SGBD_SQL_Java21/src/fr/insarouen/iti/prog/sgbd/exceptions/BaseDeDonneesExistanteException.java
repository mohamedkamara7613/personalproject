package fr.insarouen.iti.prog.sgbd.exceptions;

public class BaseDeDonneesExistanteException extends SGBDException {

    public BaseDeDonneesExistanteException() {
        super();
    }

    public BaseDeDonneesExistanteException(String nom) {
        super("La base de données '" + nom + "' existe déjà.");
    }
}