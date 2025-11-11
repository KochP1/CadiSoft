from datetime import datetime
import io
from os import getenv
from flask import render_template, send_file, Blueprint, current_app, jsonify, g
from flask_login import current_user, login_required
import pymysql
from dotenv import load_dotenv

load_dotenv()

acerca = Blueprint('acerca', __name__, template_folder='templates', static_folder='static')

# ACERCA DE 

tables = ['usuarios', 'profesores', 'secciones', 'registro_familiar', 'productos', 'preinscripcion', 'insc_x_seccion', 'inscripcion', 'horario_x_curso', 'horario', 'facultades', 'factura_x_producto', 'facturas', 'cursos', 'codigos_verificacion', 'calificaciones', 'periodo_materias', 'empresas', 'materias']
@acerca.route('/')
@login_required
def index():
    return render_template('acercaDe/index.html')

@acerca.route('/restaurar', methods = ['POST'])
@login_required
def restaurar():
    try:
        with g.db.cursor() as cur:
            for record in tables:
                cur.execute(f'Delete FROM {record}')
                g.db.commit()
                cur.execute(f'ALTER TABLE {record} AUTO_INCREMENT = 1')
                g.db.commit()
            return jsonify({'mensaje': 'Restauración completada'}), 200
    except Exception as e:
        if hasattr(g, 'db'):
            g.db.rollback()
        return jsonify({'error': f'Error al restaurar sistema: {e}'}), 500

@acerca.route('/manual', methods = ['GET'])
@login_required
def manual():
    return render_template('acercaDe/manual.html')

# NUEVO ENDPOINT PARA GENERAR SCRIPT DE BASE DE DATOS
@acerca.route('/generar-backup', methods = ['GET'])
@login_required
def generar_backup():
    if not current_user.rol == "administrador":
        return jsonify({'error': 'No tienes permisos suficientes para realizar esta acción'}), 401
    
    try:
        # Crear un string para almacenar el script SQL
        script_sql = f"-- Backup generado el: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        db_name = getenv('DB_NAME')

        # CREATE DATABASE IF NOT EXISTS `cadisoft` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
        #USE `cadisoft`;

        script_sql += f"CREATE DATABASE IF NOT EXISTS {db_name} DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;\n\n"
        script_sql += f"USE {db_name};\n\n"
        
        # Desactivar restricciones de claves foráneas temporalmente
        script_sql += "-- Desactivar verificación de claves foráneas\n"
        script_sql += "SET FOREIGN_KEY_CHECKS = 0;\n\n"
        
        with g.db.cursor(pymysql.cursors.DictCursor) as cur:
            # Generar script para cada tabla
            for table in tables:
                script_sql += f"-- Estructura y datos para tabla: {table}\n"

                script_sql += f"DROP TABLE IF EXISTS `{table}`;\n\n"
                
                # Obtener estructura de la tabla
                cur.execute(f"SHOW CREATE TABLE {table}")
                create_table = cur.fetchone()
                script_sql += f"{create_table['Create Table']};\n\n"
                
                # Obtener datos de la tabla
                cur.execute(f"SELECT * FROM {table}")
                rows = cur.fetchall()
                
                if rows:
                    # Obtener nombres de columnas
                    column_names = [desc[0] for desc in cur.description]
                    
                    # Generar INSERT statements
                    for row in rows:
                        values = []
                        for value in row.values():
                            if value is None:
                                values.append("NULL")
                            elif isinstance(value, (int, float)):
                                values.append(str(value))
                            elif isinstance(value, bytes):
                                # PARA BLOB: usar formato hexadecimal
                                hex_value = value.hex()
                                values.append(f"0x{hex_value}")
                            else:
                                # Escapar comillas simples
                                escaped_value = str(value).replace("'", "''")
                                values.append(f"'{escaped_value}'")
                        
                        insert_stmt = f"INSERT INTO {table} ({', '.join(column_names)}) VALUES ({', '.join(values)});"
                        script_sql += f"{insert_stmt}\n"
                
                script_sql += "\n"
        
        script_sql += "-- Reactivar verificación de claves foráneas\n"
        script_sql += "SET FOREIGN_KEY_CHECKS = 1;\n\n"
        
        # Crear respuesta para descargar el archivo
        output = io.BytesIO()
        output.write(script_sql.encode('utf-8'))
        output.seek(0)
        
        filename = f"backup_db_{datetime.now().strftime('%Y%m%d_%H%M%S')}.sql"
        
        return send_file(
            output,
            as_attachment=True,
            download_name=filename,
            mimetype='application/sql'
        )
        
    except Exception as e:
        if hasattr(g, 'db'):
            g.db.rollback()
        print(e)
        return jsonify({'error': f'Error al generar backup: {str(e)}'}), 500