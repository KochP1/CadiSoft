from flask import request, render_template, redirect, url_for, Blueprint, current_app, jsonify
from flask_login import login_user, logout_user, current_user
from flask_bcrypt import Bcrypt, generate_password_hash

facturacion = Blueprint('facturacion', __name__, template_folder='templates', static_folder="static")
bcrypt = Bcrypt()

@facturacion.route('/',methods = ['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('facturacion/index.html')

@facturacion.route('/inventario',methods = ['GET', 'POST'])
def inventario():
    db = current_app.config['db']
    if request.method == 'GET':
        with db.cursor() as cur:
            try:
                cur.execute('SELECT * FROM productos')
                registros = cur.fetchall()
                insertRegistros = []
                columNames = [column[0] for column in cur.description]

                for record in registros:
                    insertRegistros.append(dict(zip(columNames, record)))
                return render_template('facturacion/inventario.html', productos = insertRegistros)
            except Exception as e:
                print(e)
                return f'Error: {e}'
    
    if request.method == 'POST':
        with db.cursor() as cur:
            try:
                nombre = request.form.get('nombre')
                precio = request.form.get('precio')
                stock = request.form.get('stock')

                cur.execute('INSERT INTO productos (`nombre`, `precio`, `stock`) VALUES (%s, %s, %s)', (nombre, precio, stock))
                db.commit()
                return jsonify({'mensaje': 'Producto creado satisfactoriamente'}), 200
            except Exception as e:
                db.rollback()
                print(e)
                return jsonify({'error': f'Error al crear producto: {e}'}), 500

@facturacion.route('/elim_producto/<int:idProducto>', methods = ['DELETE'])
def elim_producto(idProducto):
    db = current_app.config['db']

    with db.cursor() as cur:
        try:
            cur.execute('DELETE FROM productos WHERE idProducto = %s', (idProducto))
            db.commit()
            return jsonify({'mensaje': 'Producto eliminado'}), 200
        except Exception as e:
            print(e)
            return jsonify({'error': f'Error al eliminar producto: {e}'}), 500

@facturacion.route('/buscar_producto', methods = ['GET', 'POST'])
def buscar_producto():
    db = current_app.config['db']
    with db.cursor() as cur:
        try:
            nombre = request.form.get('nombre')

            if not nombre:
                return redirect(url_for('facturacion.inventario'))
            
            cur.execute('SELECT * FROM productos WHERE nombre = %s',(nombre,))
            registros = cur.fetchall()
            insertRegistros = []
            columNames = [column[0] for column in cur.description]

            for record in registros:
                insertRegistros.append(dict(zip(columNames, record)))
            return render_template('facturacion/inventario.html', productos = insertRegistros)
        except Exception as e:
            print(e)
            return f'Error: {e}'

@facturacion.route('/edit_producto/<int:idProducto>', methods = ['GET', 'PATCH'])
def edit_producto(idProducto):
    db = current_app.config['db']
    
    if request.method == 'GET':
        with db.cursor() as cur:
            try:
                cur.execute('SELECT * FROM productos WHERE idProducto = %s', (idProducto,))
                registros = cur.fetchall()
                insertRegistros = []
                columNames = [column[0] for column in cur.description]

                for record in registros:
                    insertRegistros.append(dict(zip(columNames, record)))
                
                return render_template('facturacion/editProducto.html', producto = insertRegistros)
            except Exception as e:
                return f'Error: {e}'
    
    if request.method == 'PATCH':
        with db.cursor() as cur:
            try:
                nombre = request.form.get('nombre')
                precio = request.form.get('precio')
                stock = request.form.get('stock')

                if nombre:
                    cur.execute('UPDATE productos SET nombre = %s WHERE idProducto = %s', (nombre, idProducto))
                
                if precio:
                    cur.execute('UPDATE productos SET precio = %s WHERE idProducto = %s', (precio, idProducto))
                
                if stock:
                    cur.execute('UPDATE productos SET stock = %s WHERE idProducto = %s', (stock, idProducto))
                
                db.commit()
                return jsonify({'mensaje': 'Producto actualizado'}), 200
            except Exception as e:
                db.rollback()
                print(e)
                return jsonify({'error': f'Error: {e}'}), 500

@facturacion.route('/historial_facturas', methods = ['GET', 'POST'])
def historial():
    db = current_app.config['db']

    if request.method == 'GET':
        with db.cursor() as cur:
            cur.execute('SELECT f.idFactura, f.cliente, f.cedula, f.direccion, p.nombre, fp.total, f.fecha FROM factura_x_producto fp JOIN facturas f ON fp.idFactura = f.idFactura JOIN productos p ON fp.idProducto = p.idProducto')
            registros = cur.fetchall()
            insertRegistros = []
            columNames = [column[0] for column in cur.description]

            for record in registros:
                insertRegistros.append(dict(zip(columNames, record)))
            
            print(insertRegistros)
            return render_template('facturacion/historial.html', facturas = insertRegistros)
    
    if request.method == 'POST':
        with db.cursor() as cur:
            try:
                cedula = request.form.get('cedula')

                cur.execute('SELECT f.idFactura, f.cliente, f.cedula, f.direccion, p.nombre, fp.total, f.fecha FROM factura_x_producto fp JOIN facturas f ON fp.idFactura = f.idFactura JOIN productos p ON fp.idProducto = p.idProducto WHERE f.cedula = %s', (cedula,))
                registros = cur.fetchall()
                insertRegistros = []
                columNames = [column[0] for column in cur.description]

                for record in registros:
                    insertRegistros.append(dict(zip(columNames, record)))
                
                print(insertRegistros)
                return render_template('facturacion/historial.html', facturas = insertRegistros)
            except Exception as e:
                db.rollback()
                print(e)
                return f'Error: {e}'