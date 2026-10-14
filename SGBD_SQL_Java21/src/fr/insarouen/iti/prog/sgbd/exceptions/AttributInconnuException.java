package fr.insarouen.iti.prog.sgbd.exceptions;
import fr.insarouen.iti.prog.sgbd.exceptions.SGBDException;
/**
 *
 * @author Marwan
 */

public class AttributInconnuException extends SGBDException{
    
    public AttributInconnuException(){
        super();
    }

    public AttributInconnuException(String msg){
        super(msg);
    }
}