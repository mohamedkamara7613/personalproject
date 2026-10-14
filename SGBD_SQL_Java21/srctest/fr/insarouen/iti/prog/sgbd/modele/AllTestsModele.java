package fr.insarouen.iti.prog.sgbd.modele;
import org.junit.runner.RunWith;
import org.junit.runners.Suite;
import org.junit.runners.Suite.SuiteClasses;
import fr.insarouen.iti.prog.sgbd.modele.TestValeur;
import fr.insarouen.iti.prog.sgbd.modele.TestTuple;
import fr.insarouen.iti.prog.sgbd.modele.TestAttribut;
import fr.insarouen.iti.prog.sgbd.modele.TestTable;

@RunWith(Suite.class)
@SuiteClasses({
    TestValeur.class,
    TestTuple.class,
    TestAttribut.class,
    TestTable.class,
})

public class AllTestsModele {}
