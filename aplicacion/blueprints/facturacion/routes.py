from flask import request, render_template, redirect, url_for, Blueprint, current_app, jsonify, g
from flask_login import login_required

facturacion = Blueprint('facturacion', __name__, template_folder='templates', static_folder="static")

@facturacion.route('/',methods = ['GET', 'POST'])
@login_required
def index():
    if request.method == 'GET':
        return render_template('facturacion/index.html')
    
    if request.method == 'POST':
        try:
            with g.db.cursor() as cur:
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
                g.db.commit()

                cur.execute('SELECT LAST_INSERT_ID()')
                idFactura = cur.fetchone()[0] 
                
                for record in productos:
                    cur.execute('INSERT INTO factura_x_producto (`idFactura`, `idProducto`, `cantidad`) VALUES (%s, %s, %s)', (idFactura, record['idProducto'], record['cantidadProducto']))
                    g.db.commit()
                return jsonify({'mensaje': 'Factura guardada'}), 200
        except Exception as e:
            if hasattr(g, 'db'):
                g.db.rollback()
            return jsonify({'error': f'Error: {e}'}), 500


@facturacion.route('/inventario',methods = ['GET', 'POST'])
@login_required
def inventario():
    if request.method == 'GET':
        try:
            with g.db.cursor() as cur:
                cur.execute('SELECT * FROM productos')
                registros = cur.fetchall()
                insertRegistros = []
                columNames = [column[0] for column in cur.description]

                for record in registros:
                    insertRegistros.append(dict(zip(columNames, record)))
                return render_template('facturacion/inventario.html', productos = insertRegistros)
        except Exception as e:
            if hasattr(g, 'db'):
                g.db.rollback()
            return f'Error: {e}'
    
    if request.method == 'POST':
        try:
            with g.db.cursor() as cur:
                nombre = request.form.get('nombre')
                precio = request.form.get('precio')
                stock = request.form.get('stock')

                cur.execute('INSERT INTO productos (`nombre`, `precio`, `stock`) VALUES (%s, %s, %s)', (nombre, precio, stock))
                g.db.commit()
                return jsonify({'mensaje': 'Producto creado satisfactoriamente'}), 200
        except Exception as e:
            if hasattr(g, 'db'):
                g.db.rollback()
            return jsonify({'error': f'Error al crear producto: {e}'}), 500

@facturacion.route('/elim_producto/<int:idProducto>', methods = ['DELETE'])
@login_required
def elim_producto(idProducto):
    try:
        with g.db.cursor() as cur:
            cur.execute('DELETE FROM productos WHERE idProducto = %s', (idProducto))
            g.db.commit()
            return jsonify({'mensaje': 'Producto eliminado'}), 200
    except Exception as e:
        if hasattr(g, 'db'):
            g.db.rollback()
        return jsonify({'error': f'Error al eliminar producto: {e}'}), 500

@facturacion.route('/buscar_producto', methods = ['GET', 'POST'])
@login_required
def buscar_producto():
    try:
        with g.db.cursor() as cur:
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
        if hasattr(g, 'db'):
            g.db.rollback()
        return f'Error: {e}'

@facturacion.route('/edit_producto/<int:idProducto>', methods = ['GET', 'PATCH'])
@login_required
def edit_producto(idProducto):
    if request.method == 'GET':
        try:
            with g.db.cursor() as cur:
                cur.execute('SELECT * FROM productos WHERE idProducto = %s', (idProducto,))
                registros = cur.fetchall()
                insertRegistros = []
                columNames = [column[0] for column in cur.description]

                for record in registros:
                    insertRegistros.append(dict(zip(columNames, record)))
                
                return render_template('facturacion/editProducto.html', producto = insertRegistros)
        except Exception as e:
            if hasattr(g, 'db'):
                g.db.rollback()
            return f'Error: {e}'
    
    if request.method == 'PATCH':
        try:
            with g.db.cursor() as cur:
                nombre = request.form.get('nombre')
                precio = request.form.get('precio')
                stock = request.form.get('stock')

                if nombre:
                    cur.execute('UPDATE productos SET nombre = %s WHERE idProducto = %s', (nombre, idProducto))
                
                if precio:
                    cur.execute('UPDATE productos SET precio = %s WHERE idProducto = %s', (precio, idProducto))
                
                if stock:
                    cur.execute('UPDATE productos SET stock = %s WHERE idProducto = %s', (stock, idProducto))
                
                g.db.commit()
                return jsonify({'mensaje': 'Producto actualizado'}), 200
        except Exception as e:
            if hasattr(g, 'db'):
                g.db.rollback()
            return jsonify({'error': f'Error: {e}'}), 500

@facturacion.route('/historial_facturas', methods = ['GET', 'POST'])
@login_required
def historial():
    if request.method == 'GET':
        try:
            with g.db.cursor() as cur:
                cur.execute('''
                    SELECT 
                        f.idFactura, 
                        f.cliente, 
                        f.telefono, 
                        f.cedula, 
                        f.direccion,
                        f.total, 
                        f.fecha,
                        p.idProducto,
                        p.nombre as producto_nombre,
                        p.precio as producto_precio,
                        fp.cantidad as producto_cantidad
                    FROM facturas f
                    LEFT JOIN factura_x_producto fp ON f.idFactura = fp.idFactura
                    LEFT JOIN productos p ON fp.idProducto = p.idProducto
                    ORDER BY f.idFactura, p.idProducto
                ''')
                registros = cur.fetchall()
                
                facturas_dict = {}
                productos_procesados_por_factura = {}  # Un set diferente por cada factura
                
                for record in registros:
                    factura_id = record[0]
                    
                    # Si es la primera vez que encontramos esta factura, crear la estructura
                    if factura_id not in facturas_dict:
                        facturas_dict[factura_id] = {
                            'idFactura': factura_id,
                            'cliente': record[1],
                            'telefono': record[2],
                            'cedula': record[3],
                            'direccion': record[4],
                            'total': float(record[5]),
                            'fecha': record[6],
                            'productos': []
                        }
                        productos_procesados_por_factura[factura_id] = set()  # Nuevo set para esta factura
                    
                    # Si hay producto asociado y no lo hemos agregado ya, agregarlo al array
                    if record[7] is not None:  # idProducto
                        producto_key = record[7]  # Solo necesitamos el idProducto ya que el set es por factura
                        
                        if producto_key not in productos_procesados_por_factura[factura_id]:
                            productos_procesados_por_factura[factura_id].add(producto_key)
                            producto = {
                                'idProducto': record[7],
                                'nombre': record[8],
                                'precio': float(record[9]),
                                'cantidad': record[10]
                            }
                            facturas_dict[factura_id]['productos'].append(producto)
                
                # Convertir el diccionario a lista para el template
                facturas_array = list(facturas_dict.values())
                print(facturas_array)
                
                return render_template('facturacion/historial.html', facturas=facturas_array)
        except Exception as e:
            if hasattr(g, 'db'):
                g.db.rollback()
            return render_template('facturacion/historial.html', facturas=[])
    
    if request.method == 'POST':
        try:
            with g.db.cursor() as cur:
                cedula = request.form.get('cedula')

                cur.execute('SELECT f.idFactura, f.cliente, f.cedula, f.direccion, p.nombre, fp.total, f.fecha FROM factura_x_producto fp JOIN facturas f ON fp.idFactura = f.idFactura JOIN productos p ON fp.idProducto = p.idProducto WHERE f.cedula = %s', (cedula,))
                registros = cur.fetchall()
                insertRegistros = []
                columNames = [column[0] for column in cur.description]

                for record in registros:
                    insertRegistros.append(dict(zip(columNames, record)))
                
                return render_template('facturacion/historial.html', facturas = insertRegistros)
        except Exception as e:
            if hasattr(g, 'db'):
                g.db.rollback()
            return f'Error: {e}'

@facturacion.route('/elim_factura/<int:id>', methods = ['DELETE'])
@login_required
def elim_factura(id):
    try:
        with g.db.cursor() as cur:
            cur.execute('DELETE FROM facturas WHERE idFactura = %s', (id,))
            g.db.commit()
            return jsonify({'mensaje': 'Factura eliminada'}), 200
    except Exception as e:
        if hasattr(g, 'db'):
            g.db.rollback()
        return jsonify({'error': f'Error: {e}'}), 500

@facturacion.route('/buscar_producto_factura', methods = ['POST'])
@login_required
def buscar_producto_factura():
    try:
        with g.db.cursor() as cur:
            nombre = request.form.get('nombre')
            cur.execute('SELECT * FROM productos WHERE nombre = %s', (nombre))
            registro = cur.fetchone()

            if not registro:
                return jsonify({'error': 'El producto no existe'}), 404
            
            columNames = [column[0] for column in cur.description]
            producto = dict(zip(columNames, registro))
            return jsonify({'producto': producto}), 200

    except Exception as e:
        if hasattr(g, 'db'):
            g.db.rollback()
        return jsonify({'error': f'Error: {e}'}), 500