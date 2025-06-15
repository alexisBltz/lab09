package app;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

/**
 * Clase para manejar la conexión a la base de datos
 */
public class Database {
    
    private static final String URL = "jdbc:mysql://localhost:3306/laboratorio_rollback";
    private static final String USERNAME = "root";
    private static final String PASSWORD = "12345";
    
    /**
     * Obtiene una conexión a la base de datos
     * @return Connection objeto de conexión
     */
    public static Connection getConnection() {
        Connection connection = null;
        try {
            // Cargar el driver de MySQL
            Class.forName("com.mysql.cj.jdbc.Driver");
            
            // Establecer la conexión
            connection = DriverManager.getConnection(URL, USERNAME, PASSWORD);
            System.out.println("Conexión establecida exitosamente");
            
        } catch (ClassNotFoundException ex) {
            System.err.println("Error: Driver MySQL no encontrado - " + ex.getMessage());
        } catch (SQLException ex) {
            System.err.println("Error de conexión a la base de datos - " + ex.getMessage());
        }
        
        return connection;
    }
}