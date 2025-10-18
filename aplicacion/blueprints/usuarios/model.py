from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, nombre, segundoNombre, apellido, segundoApellido, cedula, email, contraseña, rol, imagen):
        self.idusuarios = id
        self.nombre = nombre
        self.segundoNombre = segundoNombre
        self.cedula = cedula
        self.apellido = apellido
        self.segundoApellido = segundoApellido
        self.email = email
        self.contraseña = contraseña
        self.rol = rol
        self.imagen = imagen

    @staticmethod
    def get_by_id(db_connection, user_id):
        """Usar conexión proporcionada en lugar de conexión global"""
        try:
            with db_connection.cursor() as cur:
                cur.execute('SELECT * FROM usuarios WHERE idusuarios = %s', (user_id,))
                user_data = cur.fetchone()
                
                if user_data:
                    return User(
                        id=user_data['idusuarios'],
                        nombre=user_data['nombre'],
                        segundoNombre=user_data['segundoNombre'],
                        apellido=user_data['apellido'],
                        segundoApellido=user_data['segundoApellido'],
                        cedula=user_data['cedula'],
                        email=user_data['email'],
                        contraseña=user_data['contraseña'],
                        rol=user_data['rol'],
                        imagen=user_data['imagen']
                    )
                return None
        except Exception as e:
            print(f"Error en get_by_id: {e}")
            return None
    
    def get_id(self):
        return str(self.idusuarios) 
    
    @staticmethod
    def get_by_cedula(db_connection, cedula):
        """Usar conexión proporcionada en lugar de conexión global"""
        try:
            with db_connection.cursor() as cur:
                cur.execute('SELECT * FROM usuarios WHERE cedula = %s', (cedula,))
                user_data = cur.fetchone()
                
                if user_data:
                    return User(
                        id=user_data['idusuarios'],
                        nombre=user_data['nombre'],
                        segundoNombre=user_data['segundoNombre'],
                        apellido=user_data['apellido'],
                        segundoApellido=user_data['segundoApellido'],
                        cedula=user_data['cedula'],
                        email=user_data['email'],
                        contraseña=user_data['contraseña'],
                        rol=user_data['rol'],
                        imagen=user_data['imagen']
                    )
                return None
        except Exception as e:
            print(f"Error en get_by_cedula: {e}")
            return None