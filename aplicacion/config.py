from datetime import date

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
    _db = None
    
    @classmethod
    def set_db(cls, db_connection):
        cls._db = db_connection
    
    @classmethod
    def expirar_inscripciones(cls):
        if not cls._db:
            print("o hay conexión a la base de datos")
            return
            
        try:
            with cls._db.cursor() as cur:
                sql = """
                    UPDATE inscripcion
                    SET es_activa = FALSE
                    WHERE (fecha_expiracion < %s AND es_activa = TRUE) OR (fecha_expiracion = %s AND es_activa = TRUE)
                """
                hoy = date.today()
                print(hoy)
                cur.execute(sql, (hoy, hoy))
                cls._db.commit()
        except Exception as e:
            print(f"Error al expirar inscripciones: {e}")