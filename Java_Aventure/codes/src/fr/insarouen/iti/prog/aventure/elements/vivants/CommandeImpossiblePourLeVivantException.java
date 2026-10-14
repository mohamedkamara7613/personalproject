package fr.insarouen.iti.prog.aventure.elements.vivants;

public class CommandeImpossiblePourLeVivantException extends VivantException {
    
    public CommandeImpossiblePourLeVivantException(String message) {
        super(message);
    }
    
    public CommandeImpossiblePourLeVivantException(String message, Throwable cause) {
        super(message, cause);
    }
}
