package fr.insarouen.iti.prog.sgbd.exceptions;
/**
 * 
 * @author Marwan
 */

public class SGBDException extends Exception{
    
    public SGBDException(){
        super();
    }

    public SGBDException(String msg){
        super(msg);
    }
}