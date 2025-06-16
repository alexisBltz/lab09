"""
Ejemplo básico de transacciones en Python - Versión consola
Demuestra los conceptos fundamentales de transacciones ACID

CONCEPTOS CLAVE:
- TRANSACCIÓN: Unidad de trabajo que se ejecuta completamente o no se ejecuta
- ACID: Atomicidad, Consistencia, Aislamiento, Durabilidad
- COMMIT: Confirma los cambios permanentemente
- ROLLBACK: Deshace todos los cambios de la transacción
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.services.transaction_service import TransactionService
from src.database import Database

def demostrar_transaccion_exitosa():
    """
    Demuestra una transacción que se ejecuta correctamente
    """
    print("\n" + "="*60)
    print("🚀 DEMOSTRACIÓN: TRANSACCIÓN EXITOSA")
    print("="*60)
    
    service = TransactionService()
    
    # Datos de ejemplo para una venta
    cliente_id = 1  # Juan Pérez
    items_venta = [
        {"producto_id": 1, "cantidad": 2},  # 2kg de Arroz
        {"producto_id": 3, "cantidad": 1},  # 1L de Aceite
    ]
    
    print("📋 Datos de la venta:")
    print(f"   Cliente ID: {cliente_id}")
    print(f"   Items: {items_venta}")
    print()
    
    # Realizar la venta
    resultado = service.realizar_venta_con_transaccion(cliente_id, items_venta)
    
    print("\n📊 RESULTADO:")
    if resultado["success"]:
        print("   ✅ TRANSACCIÓN EXITOSA")
        print(f"   💰 Total: ${resultado['total']}")
        print(f"   🆔 ID de venta: {resultado['venta_id']}")
    else:
        print("   ❌ TRANSACCIÓN FALLIDA")
        print(f"   🚫 Error: {resultado['error']}")

def demostrar_transaccion_con_rollback():
    """
    Demuestra una transacción que falla y se deshace automáticamente
    """
    print("\n" + "="*60)
    print("🔄 DEMOSTRACIÓN: TRANSACCIÓN CON ROLLBACK")
    print("="*60)
    
    service = TransactionService()
    
    cliente_id = 1
    items_venta = [{"producto_id": 1, "cantidad": 1}]
    
    print("📋 Esta transacción fallará intencionalmente")
    print("🎯 Objetivo: Demostrar cómo funciona el ROLLBACK")
    print()
    
    # Simular una venta que falla
    resultado = service.simular_venta_con_error(cliente_id, items_venta)
    
    print("\n📊 RESULTADO:")
    print("   ❌ TRANSACCIÓN FALLIDA (como se esperaba)")
    print(f"   🔄 Rollback ejecutado: {resultado['error']}")
    print("   ✅ Base de datos restaurada al estado anterior")

def demostrar_validacion_stock():
    """
    Demuestra la validación de stock que previene ventas incorrectas
    """
    print("\n" + "="*60)
    print("📦 DEMOSTRACIÓN: VALIDACIÓN DE STOCK")
    print("="*60)
    
    service = TransactionService()
    
    # Intentar vender más stock del disponible
    cliente_id = 1
    items_venta = [
        {"producto_id": 1, "cantidad": 999},  # Cantidad excesiva
    ]
    
    print("📋 Intentando vender 999 unidades de arroz")
    print("🎯 Objetivo: Demostrar validación de stock")
    print()
    
    resultado = service.realizar_venta_con_transaccion(cliente_id, items_venta)
    
    print("\n📊 RESULTADO:")
    if not resultado["success"]:
        print("   ✅ VALIDACIÓN CORRECTA")
        print(f"   🚫 Error detectado: {resultado['error']}")
        print("   🔄 Rollback automático ejecutado")
    else:
        print("   ⚠️  Esto no debería haber pasado")

def mostrar_info_transacciones():
    """
    Muestra información educativa sobre transacciones
    """
    print("\n" + "="*80)
    print("📚 INFORMACIÓN SOBRE TRANSACCIONES DE BASE DE DATOS")
    print("="*80)
    
    print("""
🎯 ¿QUÉ ES UNA TRANSACCIÓN?
   Una transacción es una secuencia de operaciones de base de datos que se
   ejecutan como una unidad única e indivisible.

🔤 PROPIEDADES ACID:

   🅰️  ATOMICIDAD (Atomicity)
       • Todas las operaciones se ejecutan completamente o ninguna
       • No hay estados intermedios
       • Ejemplo: Transferencia bancaria (débito + crédito)

   🅱️  CONSISTENCIA (Consistency)  
       • Los datos quedan en un estado válido después de la transacción
       • Se respetan todas las reglas de integridad
       • Ejemplo: Stock nunca puede ser negativo

   🅲️  AISLAMIENTO (Isolation)
       • Las transacciones concurrentes no se interfieren
       • Cada transacción ve un estado consistente
       • Ejemplo: Dos usuarios comprando el último producto

   🅳️  DURABILIDAD (Durability)
       • Los cambios persisten incluso si hay fallas del sistema
       • Se guardan permanentemente en el disco
       • Ejemplo: Venta confirmada sobrevive a un reinicio

🔧 COMANDOS CLAVE:
   • BEGIN/START TRANSACTION: Inicia una transacción
   • COMMIT: Confirma todos los cambios permanentemente  
   • ROLLBACK: Deshace todos los cambios de la transacción
   • SAVEPOINT: Crea puntos de restauración dentro de una transacción

🏪 EJEMPLO EN NUESTRA TIENDA:
   1. BEGIN TRANSACTION
   2. Validar stock del producto
   3. Insertar registro de venta
   4. Insertar detalles de venta
   5. Actualizar stock de productos
   6. COMMIT (si todo sale bien) o ROLLBACK (si hay error)

⚠️  SIN TRANSACCIONES:
   • Datos inconsistentes
   • Ventas sin actualizar stock
   • Stock negativo
   • Pérdida de información en caso de errores
""")

def main():
    """
    Función principal del ejemplo
    """
    print("🏪 SISTEMA DE TRANSACCIONES - TIENDA ALIMENTICIA")
    print("🐍 Implementación en Python con MySQL")
    
    # Verificar conexión
    db = Database()
    if not db.test_connection():
        print("\n❌ Error: No se puede conectar a la base de datos")
        print("🔧 Asegúrese de:")
        print("   1. MySQL esté ejecutándose")
        print("   2. La base de datos esté creada (ejecute database_schema.sql)")
        print("   3. Las credenciales en .env sean correctas")
        return
    
    # Mostrar información educativa
    mostrar_info_transacciones()
    
    # Demostraciones prácticas
    demostrar_transaccion_exitosa()
    demostrar_validacion_stock()
    demostrar_transaccion_con_rollback()
    
    print("\n" + "="*60)
    print("✅ DEMOSTRACIONES COMPLETADAS")
    print("="*60)
    print("🌐 Para ver la interfaz web, ejecute: python main.py")
    print("📖 Para más información, revise el código fuente comentado")

if __name__ == "__main__":
    main()
