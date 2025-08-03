from flask import request, render_template, redirect, url_for, Blueprint, current_app, jsonify

facturacion = Blueprint('facturacion', __name__, template_folder='templates', static_folder="static")

@facturacion.route('/',methods = ['GET', 'POST'])
def index():
    db = current_app.config['db']
    if request.method == 'GET':
        return render_template('facturacion/index.html')
    
    if request.method == 'POST':
        with db.cursor() as cur:
            try:
                data = request.get_json()

                if not data or 'cliente' not in data or 'telefono' not in data or 'cedula' not in data or 'direccion' not in data or 'total' not in data or 'productos' not in data:
                    return jsonify({'error': 'Datos incompletos'}), 400
                
                cliente = data['cliente']
                cedula = data['cedula']
                telefono = data['telefono']
                direccion = data['direccion']
                total = data['total']
                productos = data['productos']
                
                cur.execute('INSERT INTO facturas (`cliente`, `telefono`, `cedula`, `direccion`, `total`) VALUES (%s, %s, %s, %s, %s)', (cliente, telefono, cedula, direccion, total))
                db.commit()

                cur.execute('SELECT idFactura FROM facturas WHERE cedula = %s', (cedula,))
                idFactura = cur.fetchone()

                for record in productos:
                    print(record['idProducto'])
                    print(record['cantidadProducto'])
                
                for record in productos:
                    cur.execute('INSERT INTO factura_x_producto (`idFactura`, `idProducto`, `cantidad`) VALUES (%s, %s, %s)', (idFactura, record['idProducto'], record['cantidadProducto']))
                    db.commit()
                return jsonify({'mensaje': 'Factura guardada'}), 200
            except Exception as e:
                db.rollback()
                print(e)
                return jsonify({'error': f'Error: {e}'}), 500


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
            cur.execute('SELECT f.idFactura, f.cliente, f.telefono, f.cedula, f.direccion, p.nombre, f.total, f.fecha FROM factura_x_producto fp JOIN facturas f ON fp.idFactura = f.idFactura JOIN productos p ON fp.idProducto = p.idProducto')
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

@facturacion.route('/elim_factura/<int:id>', methods = ['DELETE'])
def elim_factura(id):
    db = current_app.config['db']

    with db.cursor() as cur:
        try:
            cur.execute('DELETE FROM facturas WHERE idFactura = %s', (id,))
            db.commit()
            return jsonify({'mensaje': 'Factura eliminada'}), 200
        except Exception as e:
            db.rollback()
            print(e)
            return jsonify({'error': f'Error: {e}'}), 500

@facturacion.route('/buscar_producto_factura', methods = ['POST'])
def buscar_producto_factura():
    db = current_app.config['db']

    with db.cursor() as cur:
        try:
            nombre = request.form.get('nombre')
            cur.execute('SELECT * FROM productos WHERE nombre = %s', (nombre))
            registro = cur.fetchone()

            if not registro:
                return jsonify({'error': 'El producto no existe'}), 404
            
            columNames = [column[0] for column in cur.description]
            producto = dict(zip(columNames, registro))
            return jsonify({'producto': producto}), 200

        except Exception as e:
            db.rollback()
            print(e)
            return jsonify({'error': f'Error: {e}'}), 500