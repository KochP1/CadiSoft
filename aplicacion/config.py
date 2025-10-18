from datetime import date
import pymysql

class Config:
    SCHEDULER_API_ENABLED = True
    JOBS = [
        {
            'id': 'job_expirar_inscripciones',
            'func': 'aplicacion.app:Config.expirar_inscripciones',
            'trigger': 'cron',
            'hour': 0,
            'minute': 1
        }
    ]
    _db_pool_factory = None
    
    @classmethod
    def set_db_pool(cls, pool_factory):
        """Establecer la función factory del pool de conexiones"""
        cls._db_pool_factory = pool_factory
    
    @classmethod
    def _get_db_connection(cls):
        """Obtener una conexión del pool (uso interno)"""
        if not cls._db_pool_factory:
            print("Error: No se ha configurado el pool de conexiones")
            return None
        
        try:
            return cls._db_pool_factory()
        except Exception as e:
            print(f"Error obteniendo conexión del pool: {e}")
            return None
    
    @classmethod
    def expirar_inscripciones(cls):
        """Tarea programada para expirar inscripciones"""
        db_connection = None
        try:
            # Obtener conexión temporal del pool
            db_connection = cls._get_db_connection()
            if not db_connection:
                print("No hay conexión a la base de datos")
                return
                
            with db_connection.cursor() as cur:
                sql = """
                    UPDATE inscripcion
                    SET es_activa = FALSE
                    WHERE (fecha_expiracion < %s AND es_activa = TRUE) 
                       OR (fecha_expiracion = %s AND es_activa = TRUE)
                """
                hoy = date.today()
                print(f"Ejecutando expiración de inscripciones para: {hoy}")
                cur.execute(sql, (hoy, hoy))
                filas_afectadas = cur.rowcount
                db_connection.commit()
                print(f"Inscripciones expiradas: {filas_afectadas}")
                
        except pymysql.Error as e:
            print(f"Error de base de datos al expirar inscripciones: {e}")
            if db_connection:
                db_connection.rollback()
        except Exception as e:
            print(f"Error inesperado al expirar inscripciones: {e}")
        finally:
            # CERRAR SIEMPRE la conexión temporal
            if db_connection:
                try:
                    db_connection.close()
                except Exception as e:
                    print(f"Error cerrando conexión en expirar_inscripciones: {e}")
    
    # MÉTODO DE COMPATIBILIDAD (opcional - para código existente)
    @classmethod
    def set_db(cls, db_connection):
        """Método legacy para compatibilidad - usar set_db_pool en su lugar"""
        print("ADVERTENCIA: set_db() está obsoleto. Usa set_db_pool() en su lugar.")
        # Crear un factory simple que siempre devuelva la misma conexión
        # NO RECOMENDADO para producción, solo para transición
        cls._db_pool_factory = lambda: db_connection