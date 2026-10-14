package fr.insarouen.iti.prog.aventure.elements.objets;
import fr.insarouen.iti.prog.aventure.ITIAventureException;

public class ObjetException extends ITIAventureException {

	public ObjetException(String message) {
		super(message);
	}
	
	public ObjetException(String message,Throwable cause) {
		super(message,cause);
	}
	
}
