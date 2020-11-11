# importamos los modulos a usar en las rutas
from flask import render_template, redirect, url_for, request, flash, session, json, make_response
from werkzeug.security import check_password_hash, generate_password_hash
# Importamos db y app para formar las rutas de la aplicacion
from webapp import db, app, con
import pdfkit
from jinja2 import Environment, FileSystemLoader

# Rutas de la aplicacion
@app.route('/')
def login():
    return render_template('login/login.html')

@app.route('/acceso', methods=['POST'])
def acceso():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        #clave = generate_password_hash(password)
        db = con.connect()
        db = con.cursor()
        sql = "Select * from empresa.empleado where nombre='{}' and clave='{}'".format(name, password)
        db.execute(sql)
        user = db.fetchone()
        if user:
            session['username'] = name
            session['id'] = user[0]
            # al  acceder exitosamente traemos la informacion de los contactos
            db.execute('SELECT * FROM empresa.empleado')
            db.close()
            con.close()
            #return redirect(url_for('Index'))
            user = session['username']
            return render_template('home.html',user=user)
        else:
            flash('Error. Usuario y/o contraseña incorrectos.')
            return redirect(url_for('login'))

@app.route('/logout')
def Logout():
    if 'username' in session:
        session.clear()
        return redirect(url_for('login'))

@app.route('/home')
def Home():
    if 'username' in session:
        user = session['username']
        return render_template("home.html", user=user)

@app.route('/principal')
def Index():
    if 'username' in session:
        con.connect()
        db=con.cursor()
        db.execute('''select idEmpleado as Id, nombre, apellido FROM empresa.empleado where
                    idEmpleado<6;''')
        data = db.fetchall()
        db.close()
        if data:
            con.connect()
            db=con.cursor()
            db.execute('SELECT * FROM empresa.cargo')
            data1 = db.fetchall()
            db.close()
        if data1:
            con.connect()
            db=con.cursor()
            db.execute('SELECT * FROM empresa.empleado')
            data2 = db.fetchall()
            db.close()
        if data2:
            con.connect()
            db=con.cursor()
            db.execute('''select idEmpleado as Id, nombre as Nombre, apellido as Apellido, email as Email, telefono as Telefono,sueldo as Sueldo, cargo.descripcion as Cargo, sector.descripcion as Sector
            FROM empresa.empleado, empresa.cargo,empresa.sector 
            where cargo.idCargo = empleado.Cargo_idCargo and sector.idSector = empleado.Sector_idSector''')
            data3 = db.fetchall()
            db.close()
        if data3:
            con.connect()
            db=con.cursor()
            db.execute('SELECT * FROM empresa.sector')
            data4 = db.fetchall()
            db.close()
        user = session['username']
        return render_template('index.html', user=user, supervisor=data, cargos=data1, empleado=data2[0], empleados=data3, sector=data4)

# ABM
@app.route('/add_contact', methods=['POST'])
def add_contact():
    if 'username' in session:
        if request.method == 'POST':
            name = request.form['name']
            lastname = request.form['lastname']
            email = request.form['email']
            phone = request.form['phone']
            sueldo = request.form['sueldo']
            cargo = request.form['cargo']
            sector = request.form['sector']
            supervisor = request.form['supervisor']
            con.connect()
            db=con.cursor()
            db.execute('''SELECT idEmpleado FROM empresa.empleado where nombre = %s''', (supervisor))
            data = db.fetchall()
            db.close()
            print(data)
            if data:
                con.connect()
                db=con.cursor()
                db.execute("INSERT INTO empresa.empleado (nombre, apellido, email, telefono, sueldo, codigoSupervisor, Cargo_idCargo, Sector_idSector) VALUES (%s,%s,%s,%s,%s,%s, %s,%s)", (name, lastname, email, phone, sueldo, data, cargo, sector ))
                con.commit()
                flash('Empleado Added successfully')
                return redirect(url_for('Index'))

@app.route('/edit/<id>', methods = ['POST', 'GET'])
def get_contact(id):
    if 'username' in session:
        con.connect()
        db=con.cursor()
        db.execute('''SELECT idEmpleado, nombre, apellido, email, telefono,sueldo, cargo.idCargo, cargo.descripcion, sector.idSector, sector.descripcion 
        FROM empresa.empleado, empresa.cargo, empresa.sector 
        WHERE cargo.idCargo = empleado.Cargo_idCargo and sector.idSector = empleado.Sector_idSector and idEmpleado = %s''', (id))
        data = db.fetchall()
        db.close()
        if data:
            con.connect()
            db=con.cursor()
            db.execute('SELECT * FROM empresa.cargo')
            data1 = db.fetchall()
            db.close()
        if data1:
            con.connect()
            db=con.cursor()
            db.execute('SELECT * FROM empresa.sector')
            data2 = db.fetchall()
            db.close()
        user = session['username']
        return render_template('edit-contact.html', user=user, empleados= data[0], cargos=data1, sector=data2)

@app.route('/update/<id>', methods=['POST'])
def update_contact(id):
    if 'username' in session:
        if request.method == 'POST':
            name = request.form['name']
            lastname = request.form['lastname']
            email = request.form['email']
            phone = request.form['phone']
            sueldo = request.form['sueldo']
            cargo = request.form['cargo']
            sector = request.form['sector']
            con.connect()
            db=con.cursor()
            db.execute("""
                UPDATE empresa.empleado
                SET nombre = %s,
                    apellido = %s,
                    email = %s,
                    telefono = %s,
                    sueldo = %s,
                    Cargo_idCargo = %s,
                    Sector_idSector = %s
                WHERE idEmpleado = %s
            """, (name, lastname, email, phone, sueldo, cargo, sector, id))
            flash('Empleado actualizado satisfactoriamente')
            con.commit()
            return redirect(url_for('Index'))

@app.route('/delete/<string:id>', methods = ['POST','GET'])
def delete_contact(id):
    if 'username' in session:
        con.connect()
        db=con.cursor()
        db.execute('DELETE FROM empresa.empleado WHERE idEmpleado = {0}'.format(id))
        con.commit()
        flash('Empleado eliminado satisfactoriamente')
        return redirect(url_for('Index'))

# Vista visualizar departamentos
@app.route('/visualizar-departamentos')
def VisualizarDepartamentos():
    if 'username' in session:
        con.connect()
        db=con.cursor()
        db.execute('''select idEmpleado as Id, nombre as Nombre, apellido as Apellido,sueldo as Sueldo, cargo.descripcion as Cargo, departamento.descripcion as Departamento, sector.descripcion as Sector, codigoSupervisor
        FROM empresa.empleado, empresa.cargo, empresa.departamento, empresa.sector 
        where cargo.idCargo = empleado.Cargo_idCargo and sector.idSector
        = empleado.Sector_idSector and sector.Departamento_idDepartamento
        = departamento.idDepartamento and idEmpleado >5;''')
        data = db.fetchall()
        db.close()
        if data:
            con.connect()
            db=con.cursor()
            db.execute('''select idEmpleado as Id, nombre, apellido FROM empresa.empleado where
                    idEmpleado<6;''')
            data1 = db.fetchall()
            db.close()
        user = session['username']
        return render_template('departamentos.html', user=user, empleados=data, sup=data1)

@app.route('/getSector/<string:id>', methods = ['POST','GET'])
def getSector(id):
    if 'username' in session:
        print(id)
        con.connect()
        db=con.cursor()
        db.execute('''select nombre from empresa.empleado, empresa.sector
        where idEmpleado<6 and sector.idSector = %s''',(id))
        sector = db.fetchall()
        con.commit()
        print(sector)
        sec = json.dumps(sector)
        return sec

# Generar reportes
@app.route('/generarReporte/')
def GenerarReporte():

    user = session['username']
    return render_template('generar-reporte.html', user=user)

@app.route('/getReporte/', methods=['POST', 'GET'])
def getReporte():
    if 'username' in session:
        con.connect()
        db=con.cursor()
        db.execute('''select idEmpleado as Id, nombre as Nombre, apellido as Apellido,sueldo as Sueldo, cargo.descripcion as Cargo, departamento.descripcion as Departamento, sector.descripcion as Sector, codigoSupervisor
        FROM empresa.empleado, empresa.cargo, empresa.departamento, empresa.sector 
        where cargo.idCargo = empleado.Cargo_idCargo and sector.idSector
        = empleado.Sector_idSector and sector.Departamento_idDepartamento
        = departamento.idDepartamento and idEmpleado >5;''')
        data = db.fetchall()
        db.close()
        if data:
            con.connect()
            db=con.cursor()
            db.execute('''select idEmpleado as Id, nombre, apellido FROM empresa.empleado where
                    idEmpleado<6;''')
            data1 = db.fetchall()
            db.close()
            if data1:
                con.connect()
                db=con.cursor()
                db.execute('''select sueldo as Sueldo FROM empresa.empleado where
                        idEmpleado>5;''')
                data2 = db.fetchall()
                db.close()
                sueldo = 0
                for suel in data2:
                    sueldo = sueldo + suel[0]
                print(sueldo)
        env = Environment(loader=FileSystemLoader('templates'))
        template = env.get_template('pdf_template.html')

        html = template.render(empleados=data, sup=data1, sueldo=sueldo)
        pdfkit.from_string(html, 'Reporte.pdf')
        return redirect(url_for('Home'))
    return redirect(url_for('VisualizarDepartamentos'))

# Errores
@app.errorhandler(404)
def error_404(e):
    return render_template('error/404.html'), 404

@app.errorhandler(500)
def error_500(e):
    return render_template('error/500.html'), 500

# Busqueda
@app.route('/buscar/', methods=['POST'])
def Buscar():
    if 'username' in session:
        con.connect()
        db = con.cursor()
        if request.method == 'POST':
            busqueda = request.form['busqueda']
            sql = f"select idEmpleado as Id, nombre as Nombre, apellido as Apellido,sueldo as Sueldo, cargo.descripcion as Cargo, departamento.descripcion as Departamento, sector.descripcion as Sector, codigoSupervisor from empresa.empleado, empresa.cargo, empresa.departamento, empresa.sector where cargo.idCargo = empleado.Cargo_idCargo and sector.idSector = empleado.Sector_idSector and sector.Departamento_idDepartamento = departamento.idDepartamento and idEmpleado >5 and (nombre LIKE '%{busqueda}%' or cargo.descripcion LIKE '%{busqueda}%' or sector.descripcion LIKE '%{busqueda}%' or apellido LIKE '%{busqueda}%' or departamento.descripcion LIKE '%{busqueda}%');"
            db.execute(sql)
            user = db.fetchall()
            db.close()
            con.close()
            data = []
            if user:
                for usu in user:
                    datos={'id':usu[0],
                        'nombre':usu[1],
                        'apellido':usu[2],
                        'sueldo':usu[3],
                        'cargo':usu[4],
                        'departamento':usu[5],
                        'sector':usu[6],
                        'supervisor':usu[7]
                        }
                    data.append(datos)
                users = json.dumps(data)
                return users


