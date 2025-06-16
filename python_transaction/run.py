"""
Script para ejecutar la aplicación web de la tienda alimenticia
Manejo simplificado de rutas y dependencias
"""

import sys
import os
from pathlib import Path

# Obtener el directorio del proyecto
PROJECT_DIR = Path(__file__).parent.absolute()
sys.path.insert(0, str(PROJECT_DIR))

# Cambiar al directorio del proyecto
os.chdir(PROJECT_DIR)

from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Importar servicios del proyecto
from src.services.transaction_service import TransactionService
from src.database import Database

# Configurar rutas de templates y static
template_dir = PROJECT_DIR / 'templates'
static_dir = PROJECT_DIR / 'static'

# Crear aplicación Flask
app = Flask(__name__, 
           template_folder=str(template_dir), 
           static_folder=str(static_dir))
app.secret_key = os.getenv('SECRET_KEY', 'clave_secreta_por_defecto')

# Inicializar servicios
transaction_service = TransactionService()
db = Database()

@app.route('/')
def index():
    """
    Página principal de la tienda
    """
    productos = transaction_service.obtener_productos()
    clientes = transaction_service.obtener_clientes()
    
    return render_template('index.html', productos=productos, clientes=clientes)

@app.route('/realizar_venta', methods=['POST'])
def realizar_venta():
    """
    Endpoint para realizar una venta con transacciones
    """
    try:
        data = request.get_json()
        cliente_id = data.get('cliente_id')
        items = data.get('items', [])
        
        if not cliente_id:
            return jsonify({"success": False, "error": "Debe seleccionar un cliente"})
        
        if not items:
            return jsonify({"success": False, "error": "Debe agregar productos a la venta"})
        
        # Realizar la venta usando transacciones
        resultado = transaction_service.realizar_venta_con_transaccion(cliente_id, items)
        
        return jsonify(resultado)
        
    except Exception as e:
        return jsonify({"success": False, "error": f"Error interno: {str(e)}"})

@app.route('/simular_error', methods=['POST'])
def simular_error():
    """
    Endpoint para simular una transacción con error (para demostrar rollback)
    """
    try:
        data = request.get_json()
        cliente_id = data.get('cliente_id', 1)
        items = data.get('items', [{"producto_id": 1, "cantidad": 1}])
        
        # Simular una venta que falla
        resultado = transaction_service.simular_venta_con_error(cliente_id, items)
        
        return jsonify(resultado)
        
    except Exception as e:
        return jsonify({"success": False, "error": f"Error interno: {str(e)}"})

@app.route('/productos')
def obtener_productos():
    """
    API para obtener la lista de productos
    """
    productos = transaction_service.obtener_productos()
    return jsonify(productos)

@app.route('/clientes')
def obtener_clientes():
    """
    API para obtener la lista de clientes
    """
    clientes = transaction_service.obtener_clientes()
    return jsonify(clientes)

@app.route('/test_db')
def test_database():
    """
    Endpoint para probar la conexión a la base de datos
    """
    if db.test_connection():
        return jsonify({"status": "success", "message": "Conexión a la base de datos exitosa"})
    else:
        return jsonify({"status": "error", "message": "Error en la conexión a la base de datos"})

@app.errorhandler(404)
def not_found(error):
    return render_template('error.html', error="Página no encontrada"), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('error.html', error="Error interno del servidor"), 500

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
    
    # Probar conexión a la base de datos
    print("🔌 Probando conexión a la base de datos...")
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
        
        # Configuración del servidor
        port = int(os.getenv('PORT', 5000))
        debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
        
        # Iniciar la aplicación Flask
        app.run(host='0.0.0.0', port=port, debug=debug)
        
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
