# importamos los modulos a usar en las rutas
from flask import render_template, redirect, url_for, request, flash, session
from werkzeug.security import check_password_hash, generate_password_hash
# Importamos db y app para formar las rutas de la aplicacion
from webapp import db, app, con

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
            return render_template('home.html',user=session['username'])
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
      return render_template("home.html")

@app.route('/principal')
def Index():
    con.connect()
    db=con.cursor()
    db.execute('SELECT * FROM empresa.empleado')
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
        db.execute('SELECT * FROM empresa.departamento')
        data2 = db.fetchall()
        db.close()
    if data2:
        con.connect()
        db=con.cursor()
        db.execute('''select idEmpleado as Id, nombre as Nombre, apellido as Apellido, email as Email, telefono as Telefono,sueldo as Sueldo, cargo.descripcion as Cargo, sector.descripcion as Sector FROM empresa.empleado, empresa.cargo,empresa.sector 
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
    return render_template('index.html', user=user, empleado=data, cargos=data1, depto=data2, empleados=data3, sector=data4)

@app.route('/add_contact', methods=['POST'])
def add_contact():
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
        db.execute("INSERT INTO empresa.empleado (nombre, apellido, email, telefono, sueldo, Cargo_idCargo, Sector_idSector) VALUES (%s,%s,%s,%s,%s,%s,%s)", (name, lastname, email, phone, sueldo, cargo, sector ))
        con.commit()
        flash('Empleado Added successfully')
        return redirect(url_for('Index'))

@app.route('/edit/<id>', methods = ['POST', 'GET'])
def get_contact(id):
    con.connect()
    db=con.cursor()
    db.execute('''SELECT idEmpleado, nombre, apellido, email, telefono,sueldo, cargo.descripcion, sector.descripcion 
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
    con.connect()
    db=con.cursor()
    db.execute('DELETE FROM empresa.empleado WHERE idEmpleado = {0}'.format(id))
    con.commit()
    flash('Empleado eliminado satisfactoriamente')
    return redirect(url_for('Index'))

# Vista visualizar departamentos
@app.route('/visualizar-departamentos')
def VisualizarDepartamentos():
    con.connect()
    db=con.cursor()
    db.execute('''select idEmpleado as Id, nombre as Nombre, apellido as Apellido,sueldo as Sueldo, cargo.descripcion as Cargo, departamento.descripcion as Departamento, sector.descripcion as Sector FROM empresa.empleado, empresa.cargo, empresa.departamento, empresa.sector 
    where cargo.idCargo = empleado.Cargo_idCargo and sector.idSector = empleado.Sector_idSector and sector.Departamento_idDepartamento = departamento.idDepartamento;''')
    data = db.fetchall()
    db.close()
    user = session['username']
    return render_template('departamentos.html', user=user, empleados=data)
