package fr.insarouen.iti.prog.sgbd.exceptions;
import fr.insarouen.iti.prog.sgbd.exceptions.SGBDException;
/**
 *
 * @author Marwan
 */

public class AttributExistantException extends SGBDException{
    
    public AttributExistantException(){
        super();
    }

    public AttributExistantException(String msg){
        super(msg);
    }
}