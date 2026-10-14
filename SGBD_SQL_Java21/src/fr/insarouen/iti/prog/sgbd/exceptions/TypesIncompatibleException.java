package fr.insarouen.iti.prog.sgbd.exceptions;
import fr.insarouen.iti.prog.sgbd.exceptions.SGBDException;
/**
 *
 * @author Marwan
 */

public class TypesIncompatibleException extends SGBDException{
    
    public TypesIncompatibleException(){
        super();
    }

    public TypesIncompatibleException(String msg){
        super(msg);
    }
}