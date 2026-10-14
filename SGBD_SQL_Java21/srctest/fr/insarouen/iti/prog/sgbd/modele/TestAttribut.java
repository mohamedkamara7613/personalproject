package fr.insarouen.iti.prog.sgbd.modele;

import org.junit.Before;
import org.junit.Test;
 
import static org.hamcrest.CoreMatchers.equalTo;
import static org.hamcrest.CoreMatchers.not;
import static org.hamcrest.MatcherAssert.assertThat;

public class TestAttribut {
    private Attribut attributInt;
    private Attribut attributVarchar;
    private Attribut attributSerial;
    
    @Before
    public void avantTest(){
        this.attributInt = new Attribut("heure",Type.INT);
        this.attributVarchar = new Attribut("nom",Type.VARCHAR);
        this.attributSerial = new Attribut("id",Type.SERIAL);
    }

    @Test
    public void test_Attribut_nom_INT(){
        assertThat(this.attributInt.nom(), equalTo("heure"));
    }

    @Test
    public void test_Attribut_nom_VARCHAR(){
        assertThat(this.attributVarchar.nom(), equalTo("nom"));
    }

    @Test
    public void test_Attribut_nom_SERIAL(){
        assertThat(this.attributSerial.nom(), equalTo("id"));
    }

    @Test
    public void test_Attribut_type_INT() {
        assertThat(this.attributInt.type(), equalTo(Type.INT));
    }
 
    @Test
    public void test_Attribut_type_VARCHAR() {
        assertThat(this.attributVarchar.type(), equalTo(Type.VARCHAR));
    }
 
    @Test
    public void test_Attribut_type_SERIAL() {
        assertThat(this.attributSerial.type(), equalTo(Type.SERIAL));
    }
    @Test
    public void test_Attribut_toString_INT() {
        assertThat(this.attributInt.toString(), equalTo("heure INT"));
    }

     @Test
    public void test_Attribut_toString_VARCHAR(){
        assertThat(this.attributVarchar.toString(), equalTo("nom VARCHAR"));
    }

     @Test
    public void test_Attribut_toString_SERIAL(){
        assertThat(this.attributSerial.toString(), equalTo("id SERIAL"));
    }


    @Test
    public void test_Attribut_equals_identiques() {
        Attribut autre = new Attribut("heure", Type.INT);
        assertThat(this.attributInt, equalTo(autre));
    }
 
    @Test
    public void test_Attribut_equals_nomsDifferents() {
        Attribut autre = new Attribut("poids", Type.INT);
        assertThat(this.attributInt, not(equalTo(autre)));
    }
 
    @Test
    public void test_Attribut_equals_typesDifferents() {
        Attribut autre = new Attribut("heure", Type.VARCHAR);
        assertThat(this.attributInt, not(equalTo(autre)));
    }
 
    @Test
    public void test_Attribut_equals_nomEtTypesDifferents() {
        assertThat(this.attributInt, not(equalTo(this.attributVarchar)));
    }
}
