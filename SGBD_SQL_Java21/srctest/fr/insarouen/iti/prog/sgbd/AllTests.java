package fr.insarouen.iti.prog.sgbd;
import org.junit.runner.RunWith;
import org.junit.runners.Suite;
import org.junit.runners.Suite.SuiteClasses;
import fr.insarouen.iti.prog.sgbd.modele.AllTestsModele;
import fr.insarouen.iti.prog.sgbd.parseur.AllTestsParseur;
import fr.insarouen.iti.prog.sgbd.expressions.AllTestsExpressions;
import fr.insarouen.iti.prog.sgbd.data.AllTestsData;

@RunWith(Suite.class)
@SuiteClasses({
   AllTestsModele.class,
   AllTestsParseur.class,
   AllTestsExpressions.class,
   AllTestsData.class
})

public class AllTests {}
