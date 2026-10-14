package fr.insarouen.iti.prog.aventure.elements;

import fr.insarouen.iti.prog.aventure.ITIAventureException;



public class ActivationException extends ITIAventureException {
    public ActivationException(String message) {
		super(message);
	}
	
	public ActivationException(String message,Throwable cause) {
		super(message,cause);
	}
}