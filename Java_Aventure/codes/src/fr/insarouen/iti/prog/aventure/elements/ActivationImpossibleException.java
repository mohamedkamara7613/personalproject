package fr.insarouen.iti.prog.aventure.elements;


public class ActivationImpossibleException extends ActivationException {
    public ActivationImpossibleException(String message) {
		super(message);
	}
	
	public ActivationImpossibleException(String message,Throwable cause) {
		super(message,cause);
	}
}