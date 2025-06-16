"""
Servicio para manejar transacciones de ventas en la tienda alimenticia
Demuestra el uso de transacciones ACID en bases de datos

TRANSACCIONES:
Una transacción es una unidad de trabajo que se ejecuta de forma atómica,
es decir, todas las operaciones se ejecutan correctamente o ninguna se ejecuta.

Propiedades ACID:
- Atomicidad: Todo o nada se ejecuta
- Consistencia: Los datos quedan en un estado válido
- Aislamiento: Las transacciones no se interfieren entre sí
- Durabilidad: Los cambios persisten después del commit
"""

import mysql.connector
from mysql.connector import Error
from src.database import Database
from src.models import Producto, Cliente, Venta, DetalleVenta
from decimal import Decimal

class TransactionService:
    """
    Servicio para manejar transacciones de ventas
    Implementa operaciones CRUD con control de transacciones
    """
    
    def __init__(self):
        self.db = Database()
    
    def realizar_venta_con_transaccion(self, cliente_id, items_venta):
        """
        Realiza una venta completa usando transacciones para garantizar consistencia
        
        Esta función demuestra:
        1. Inicio de transacción (BEGIN)
        2. Validación de stock
        3. Actualización de inventario
        4. Registro de venta
        5. Commit si todo sale bien
        6. Rollback si hay algún error
        
        Args:
            cliente_id (int): ID del cliente
            items_venta (list): Lista de diccionarios con producto_id y cantidad
            
        Returns:
            dict: Resultado de la operación con éxito o error
        """
        
        connection = None
        cursor = None
        
        try:
            # Obtener conexión a la base de datos
            connection = self.db.get_connection()
            if not connection:
                return {"success": False, "error": "No se pudo conectar a la base de datos"}
            
            # INICIO DE TRANSACCIÓN
            # Crear cursor y deshabilitar autocommit para manejar transacciones manualmente
            cursor = connection.cursor()
            connection.start_transaction()  # Equivale a BEGIN en SQL
            
            print("🚀 INICIANDO TRANSACCIÓN DE VENTA")
            print(f"👤 Cliente ID: {cliente_id}")
            print(f"🛒 Items a vender: {items_venta}")
            
            # 1. VALIDAR QUE EL CLIENTE EXISTE
            cursor.execute("SELECT id, nombre FROM clientes WHERE id = %s", (cliente_id,))
            cliente = cursor.fetchone()
            if not cliente:
                raise Exception(f"Cliente con ID {cliente_id} no existe")
            
            print(f"✅ Cliente validado: {cliente[1]}")
            
            # 2. VALIDAR STOCK Y CALCULAR TOTAL
            total_venta = Decimal('0.00')
            productos_validados = []
            
            for item in items_venta:
                producto_id = item['producto_id']
                cantidad_solicitada = item['cantidad']
                
                # Verificar que el producto existe y tiene stock suficiente
                cursor.execute(
                    "SELECT id, nombre, precio, stock FROM productos WHERE id = %s",
                    (producto_id,)
                )
                producto = cursor.fetchone()
                
                if not producto:
                    raise Exception(f"Producto con ID {producto_id} no existe")
                
                stock_actual = producto[3]
                if stock_actual < cantidad_solicitada:
                    raise Exception(
                        f"Stock insuficiente para '{producto[1]}'. "
                        f"Stock actual: {stock_actual}, Solicitado: {cantidad_solicitada}"
                    )
                
                precio_unitario = producto[2]
                subtotal = precio_unitario * cantidad_solicitada
                total_venta += subtotal
                
                productos_validados.append({
                    'producto_id': producto_id,
                    'nombre': producto[1],
                    'cantidad': cantidad_solicitada,
                    'precio_unitario': precio_unitario,
                    'subtotal': subtotal,
                    'stock_actual': stock_actual
                })
                
                print(f"✅ Producto validado: {producto[1]} - Cantidad: {cantidad_solicitada} - Subtotal: ${subtotal}")
            
            print(f"💰 Total de la venta: ${total_venta}")
            
            # 3. REGISTRAR LA VENTA (CABECERA)
            cursor.execute(
                """INSERT INTO ventas (cliente_id, total, estado) 
                   VALUES (%s, %s, 'completada')""",
                (cliente_id, total_venta)
            )
            
            venta_id = cursor.lastrowid
            print(f"📋 Venta registrada con ID: {venta_id}")
            
            # 4. REGISTRAR DETALLES DE VENTA Y ACTUALIZAR STOCK
            for producto in productos_validados:
                # Insertar detalle de venta
                cursor.execute(
                    """INSERT INTO detalle_ventas 
                       (venta_id, producto_id, cantidad, precio_unitario, subtotal)
                       VALUES (%s, %s, %s, %s, %s)""",
                    (venta_id, producto['producto_id'], producto['cantidad'],
                     producto['precio_unitario'], producto['subtotal'])
                )
                
                # Actualizar stock del producto (OPERACIÓN CRÍTICA)
                nuevo_stock = producto['stock_actual'] - producto['cantidad']
                cursor.execute(
                    "UPDATE productos SET stock = %s WHERE id = %s",
                    (nuevo_stock, producto['producto_id'])
                )
                
                print(f"📦 Stock actualizado para '{producto['nombre']}': {producto['stock_actual']} → {nuevo_stock}")
            
            # 5. COMMIT DE LA TRANSACCIÓN
            # Si llegamos aquí, todo salió bien, confirmamos los cambios
            connection.commit()
            print("✅ TRANSACCIÓN COMPLETADA EXITOSAMENTE - COMMIT REALIZADO")
            
            return {
                "success": True,
                "venta_id": venta_id,
                "total": float(total_venta),
                "mensaje": f"Venta realizada exitosamente. ID: {venta_id}, Total: ${total_venta}",
                "productos": productos_validados
            }
            
        except Error as e:
            # Error de base de datos
            error_msg = f"Error de base de datos: {str(e)}"
            print(f"❌ {error_msg}")
            if connection:
                connection.rollback()
                print("🔄 ROLLBACK REALIZADO - Transacción deshecha")
            return {"success": False, "error": error_msg}
            
        except Exception as e:
            # Error de lógica de negocio
            error_msg = f"Error en la validación: {str(e)}"
            print(f"❌ {error_msg}")
            if connection:
                connection.rollback()
                print("🔄 ROLLBACK REALIZADO - Transacción deshecha")
            return {"success": False, "error": error_msg}
            
        finally:
            # Limpiar recursos
            if cursor:
                cursor.close()
            print("🧹 Recursos liberados")
    
    def simular_venta_con_error(self, cliente_id, items_venta):
        """
        Simula una venta que falla a propósito para demostrar el rollback
        
        Esta función demuestra qué pasa cuando una transacción falla:
        - Se deshacen todos los cambios realizados
        - La base de datos vuelve al estado anterior
        """
        
        connection = None
        cursor = None
        
        try:
            connection = self.db.get_connection()
            if not connection:
                return {"success": False, "error": "No se pudo conectar a la base de datos"}
            
            cursor = connection.cursor()
            connection.start_transaction()
            
            print("🚀 INICIANDO TRANSACCIÓN CON ERROR SIMULADO")
            print("⚠️  Esta transacción fallará intencionalmente para demostrar rollback")
            
            # Registrar una venta
            cursor.execute(
                "INSERT INTO ventas (cliente_id, total, estado) VALUES (%s, %s, 'pendiente')",
                (cliente_id, 999.99)
            )
            venta_id = cursor.lastrowid
            print(f"📋 Venta temporal registrada con ID: {venta_id}")
            
            # Simular un error forzado
            print("💥 SIMULANDO ERROR...")
            raise Exception("Error simulado para demostrar rollback")
            
        except Exception as e:
            error_msg = f"Error simulado: {str(e)}"
            print(f"❌ {error_msg}")
            if connection:
                connection.rollback()
                print("🔄 ROLLBACK REALIZADO - Todos los cambios fueron deshecho")
            return {"success": False, "error": error_msg}
            
        finally:
            if cursor:
                cursor.close()
    
    def obtener_productos(self):
        """
        Obtiene la lista de productos disponibles
        """
        try:
            connection = self.db.get_connection()
            cursor = connection.cursor()
            
            cursor.execute("SELECT id, nombre, categoria, precio, stock FROM productos WHERE stock > 0")
            productos = cursor.fetchall()
            
            return [
                {
                    'id': p[0],
                    'nombre': p[1], 
                    'categoria': p[2],
                    'precio': float(p[3]),
                    'stock': p[4]
                } 
                for p in productos
            ]
            
        except Error as e:
            print(f"Error al obtener productos: {e}")
            return []
        finally:
            if cursor:
                cursor.close()
    
    def obtener_clientes(self):
        """
        Obtiene la lista de clientes
        """
        try:
            connection = self.db.get_connection()
            cursor = connection.cursor()
            
            cursor.execute("SELECT id, nombre, email FROM clientes")
            clientes = cursor.fetchall()
            
            return [
                {
                    'id': c[0],
                    'nombre': c[1],
                    'email': c[2]
                }
                for c in clientes
            ]
            
        except Error as e:
            print(f"Error al obtener clientes: {e}")
            return []
        finally:
            if cursor:
                cursor.close()
    
    def verificar_rollback_real(self, cliente_id):
        """
        Función educativa para DEMOSTRAR que el rollback SÍ afecta la BD real
        
        Esta función:
        1. Cuenta las ventas antes de la transacción
        2. Inicia una transacción y agrega una venta
        3. Muestra que la venta SÍ se agregó temporalmente
        4. Fuerza un error para activar rollback
        5. Muestra que la venta fue ELIMINADA por el rollback
        """
        
        connection = None
        cursor = None
        
        try:
            connection = self.db.get_connection()
            if not connection:
                return {"success": False, "error": "No se pudo conectar a la base de datos"}
            
            cursor = connection.cursor()
            
            # 1. CONTAR VENTAS ANTES DE LA TRANSACCIÓN
            cursor.execute("SELECT COUNT(*) FROM ventas")
            ventas_antes = cursor.fetchone()[0]
            print(f"📊 ANTES: {ventas_antes} ventas en la base de datos")
            
            # 2. INICIAR TRANSACCIÓN
            connection.start_transaction()
            print("🚀 INICIANDO TRANSACCIÓN...")
            
            # 3. AGREGAR UNA VENTA REAL
            cursor.execute(
                "INSERT INTO ventas (cliente_id, total, estado) VALUES (%s, %s, 'temporal')",
                (cliente_id, 888.88)
            )
            venta_id = cursor.lastrowid
            
            # 4. VERIFICAR QUE LA VENTA SÍ SE AGREGÓ (dentro de la transacción)
            cursor.execute("SELECT COUNT(*) FROM ventas")
            ventas_durante = cursor.fetchone()[0]
            print(f"📊 DURANTE TRANSACCIÓN: {ventas_durante} ventas (SE AGREGÓ REALMENTE)")
            print(f"📋 Venta ID {venta_id} EXISTE temporalmente en la BD")
            
            # 5. FORZAR ERROR PARA ACTIVAR ROLLBACK
            print("💥 FORZANDO ERROR PARA DEMOSTRAR ROLLBACK...")
            raise Exception("Error intencional para activar rollback")
            
        except Exception as e:
            print(f"❌ {str(e)}")
            if connection:
                # 6. EL ROLLBACK ELIMINA LA VENTA QUE SÍ EXISTÍA
                connection.rollback()
                print("🔄 ROLLBACK EJECUTADO")
                
                # 7. VERIFICAR QUE LA VENTA FUE ELIMINADA
                cursor.execute("SELECT COUNT(*) FROM ventas")
                ventas_despues = cursor.fetchone()[0]
                print(f"📊 DESPUÉS DEL ROLLBACK: {ventas_despues} ventas")
                
                if ventas_despues == ventas_antes:
                    print("✅ DEMOSTRACIÓN EXITOSA: El rollback SÍ deshizo cambios reales")
                else:
                    print("⚠️  Algo inesperado ocurrió")
                    
            return {
                "success": False, 
                "error": "Demostración completada - El rollback SÍ afecta la BD real",
                "ventas_antes": ventas_antes,
                "ventas_despues": ventas_despues if 'ventas_despues' in locals() else "N/A"
            }
            
        finally:
            if cursor:
                cursor.close()
