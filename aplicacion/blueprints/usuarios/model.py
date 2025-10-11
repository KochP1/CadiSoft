from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, nombre, segundoNombre, apellido, segundoApellido, cedula, email, contraseña, rol, imagen):
        self.id = id
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
    def get_by_id(db, user_id):
        cur = db.cursor()
        cur.execute('SELECT * FROM usuarios WHERE idusuarios = %s', (user_id,))
        user_data = cur.fetchone()
        cur.close()
        if user_data:
                return User(
                    id=user_data[0],
                    nombre=user_data[1],
                    segundoNombre=user_data[2],
                    apellido=user_data[3],
                    segundoApellido=user_data[4],
                    cedula=user_data[5],
                    email=user_data[6],
                    contraseña = user_data[7],
                    rol = user_data[8],
                    imagen = user_data[9]
                )
        return None
    
    def get_id(self):
        return str(self.id) 
    
    @staticmethod
    def get_by_cedula(db, cedula):
        cur = db.cursor()
        cur.execute('SELECT * FROM usuarios WHERE cedula = %s', (cedula,))
        user_data = cur.fetchone()
        cur.close()
        if user_data:
                return User(
                    id=user_data[0],
                    nombre=user_data[1],
                    segundoNombre=user_data[2],
                    apellido=user_data[3],
                    segundoApellido=user_data[4],
                    cedula=user_data[5],
                    email=user_data[6],
                    contraseña = user_data[7],
                    rol = user_data[8],
                    imagen = user_data[9]
                )
        return None