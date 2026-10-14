package fr.insarouen.iti.prog.sgbd.exceptions;
import fr.insarouen.iti.prog.sgbd.exceptions.SGBDException;
/**
 *
 * @author Marwan
 */

public class TupleInconnuException extends SGBDException{
    
    public TupleInconnuException(){
        super();
    }

    public TupleInconnuException(String msg){
        super(msg);
    }
}