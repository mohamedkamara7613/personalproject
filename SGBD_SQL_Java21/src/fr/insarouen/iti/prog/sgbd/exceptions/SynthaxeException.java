package fr.insarouen.iti.prog.sgbd.exceptions;
import fr.insarouen.iti.prog.sgbd.exceptions.SGBDException;
/**
 *
 * @author Marwan
 */

public class SynthaxeException extends SGBDException{
    
    public SynthaxeException(){
        super();
    }

    public SynthaxeException(String msg){
        super(msg);
    }
}