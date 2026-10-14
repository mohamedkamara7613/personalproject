
package fr.insarouen.iti.prog.aventure.elements.structure;

public class ObjetAbsentDeLaPieceException extends PieceException {

	public ObjetAbsentDeLaPieceException(String message) {
		super(message);
	}
	
	public ObjetAbsentDeLaPieceException(String message,Throwable cause) {
		super(message,cause);
	}
	
}
