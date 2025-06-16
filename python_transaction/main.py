"""
Archivo principal para ejecutar la aplicación de demostración de transacciones
Tienda Alimenticia - Sistema de ventas con transacciones ACID
"""

import sys
import os

# Agregar el directorio actual al path para importaciones
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

# Cambiar al directorio del proyecto para rutas relativas
os.chdir(current_dir)

from src.web.app import app
from src.database import Database

def main():
    """
    Función principal para iniciar la aplicación
    """
    print("=" * 60)
    print("🏪 TIENDA ALIMENTICIA - SISTEMA DE TRANSACCIONES")
    print("=" * 60)
    print()
    print("📋 DESCRIPCIÓN:")
    print("   Sistema de demostración de transacciones ACID en Python")
    print("   usando MySQL y Flask para la interfaz web.")
    print()
    print("🎯 FUNCIONALIDADES:")
    print("   ✅ Ventas con transacciones atómicas")
    print("   ✅ Validación de stock en tiempo real")
    print("   ✅ Rollback automático en caso de errores")
    print("   ✅ Interfaz web intuitiva")
    print("   ✅ Simulación de errores para demostrar rollback")
    print()
    print("🔧 TRANSACCIONES IMPLEMENTADAS:")
    print("   • BEGIN TRANSACTION")
    print("   • COMMIT (cuando todo sale bien)")
    print("   • ROLLBACK (cuando hay errores)")
    print("   • Control de concurrencia")
    print("   • Validación de integridad referencial")
    print()
    
    # Probar conexión a la base de datos
    print("🔌 Probando conexión a la base de datos...")
    db = Database()
    if db.test_connection():
        print("✅ Conexión exitosa!")
        print()
        print("🌐 Iniciando servidor web...")
        print("🔗 Abra su navegador en: http://localhost:5000")
        print()
        print("📖 INSTRUCCIONES:")
        print("   1. Seleccione un cliente")
        print("   2. Agregue productos al carrito")
        print("   3. Use 'Realizar Venta' para una transacción exitosa")
        print("   4. Use 'Simular Error' para ver el rollback en acción")
        print()
        print("⚠️  Para detener el servidor: Ctrl+C")
        print("=" * 60)
        
        # Iniciar la aplicación Flask
        app.run(host='0.0.0.0', port=5000, debug=True)
        
    else:
        print("❌ Error de conexión a la base de datos!")
        print()
        print("🔧 PASOS PARA SOLUCIONAR:")
        print("   1. Asegúrese de que MySQL esté ejecutándose")
        print("   2. Verifique las credenciales en el archivo .env")
        print("   3. Ejecute el script database_schema.sql para crear la base de datos")
        print("   4. Instale las dependencias: pip install -r requirements.txt")
        print()
        print("📄 Configuración actual (.env):")
        print(f"   DB_HOST: {os.getenv('DB_HOST', 'localhost')}")
        print(f"   DB_PORT: {os.getenv('DB_PORT', '3306')}")
        print(f"   DB_NAME: {os.getenv('DB_NAME', 'tienda_alimenticia')}")
        print(f"   DB_USER: {os.getenv('DB_USER', 'root')}")
        

if __name__ == "__main__":
    main()
