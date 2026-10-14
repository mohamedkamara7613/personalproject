package fr.insarouen.iti.prog.sgbd.exceptions;
import fr.insarouen.iti.prog.sgbd.exceptions.SGBDException;
/**
 *
 * @author Marwan
 */

public class TableExistanteException extends SGBDException{
    
    public TableExistanteException(){
        super();
    }

    public TableExistanteException(String msg){
        super(msg);
    }
}