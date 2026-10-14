package fr.insarouen.iti.prog.sgbd.exceptions;
import fr.insarouen.iti.prog.sgbd.exceptions.SGBDException;
/**
 *
 * @author Marwan
 */

public class TableInconnueException extends SGBDException{
    
    public TableInconnueException(){
        super();
    }

    public TableInconnueException(String msg){
        super(msg);
    }
}