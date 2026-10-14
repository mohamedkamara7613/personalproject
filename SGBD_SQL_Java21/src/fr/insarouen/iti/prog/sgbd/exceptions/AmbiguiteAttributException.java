package fr.insarouen.iti.prog.sgbd.exceptions;
import fr.insarouen.iti.prog.sgbd.exceptions.SGBDException;
/**
 *
 * @author Marwan
 */

public class AmbiguiteAttributException extends SGBDException{
    
    public AmbiguiteAttributException(){
        super();
    }

    public AmbiguiteAttributException(String msg){
        super(msg);
    }
}