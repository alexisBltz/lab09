package app;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.SQLException;

/**
 * @web https://www.jc-mouse.net/
 * @author Mouse
 */
public class JNoRollback {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {

        // Obtenemos conexion a la base de datos
        Connection connection = Database.getConnection();

        PreparedStatement stmt1 = null;
        PreparedStatement stmt2 = null;

        try {
            // AutoCommit está habilitado por defecto (true) - cada executeUpdate() se confirma automáticamente
            // No se llama connection.setAutoCommit(false) como en JRollback
            
            // Se preparan las sentencias SQL
            stmt1 = connection.prepareStatement("INSERT INTO mitabla VALUES( ?, ? );");
            stmt2 = connection.prepareStatement("INSERT INTO miotratabla VALUES( ?, ?, ? );");

            System.out.println("Primer INSERT tabla [mitabla] ");
            stmt1.setString(1, "000001");
            stmt1.setString(2, "micorreo@mail.com");
            stmt1.executeUpdate();

            System.out.println("Segundo INSERT tabla [mitabla] ");
            stmt1.setString(1, "000002");
            stmt1.setString(2, "amayuya@mail.com");
            stmt1.executeUpdate();

            System.out.println("Tercer INSERT tabla [mitabla] ");
            stmt1.setString(1, "000003");
            stmt1.setString(2, "diosdado@mail.com");
            stmt1.executeUpdate();

            System.out.println("Primer INSERT tabla [miotratabla]");
            stmt2.setString(1, "Juan");
            stmt2.setString(2, "Perez");
            // stmt2.setInt(3, 99); //Tipo de dato CORRECTO INT
            stmt2.setString(3, "Hola soy un error"); // Tipo de dato INCORRECTO
            stmt2.executeUpdate();

        } catch (SQLException ex) {
            System.err.println("ERROR: " + ex.getMessage());
        } finally {
            System.out.println("cierra conexion a la base de datos");
            try {
                if (stmt1 != null) stmt1.close();
                if (stmt2 != null) stmt2.close();
                if (connection != null) connection.close();
            } catch (SQLException ex) {
                System.err.println(ex.getMessage());
            }
        }

    } // end:main
}