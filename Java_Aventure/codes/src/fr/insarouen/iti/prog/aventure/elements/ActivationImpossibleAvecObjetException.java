package fr.insarouen.iti.prog.aventure.elements;


public class ActivationImpossibleAvecObjetException extends ActivationException {
    
	public ActivationImpossibleAvecObjetException(String message) {
		super(message);
	}
	
	public ActivationImpossibleAvecObjetException(String message,Throwable cause) {
		super(message,cause);
	}
}