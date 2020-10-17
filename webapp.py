# Importamos framework Flask
from flask import Flask
# importamos modulo de mysql
import pymysql

# Inicializamos la app y el servidor
app = Flask(__name__)

# Establecemos la conexion a la BD
con=pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="empresa")
db=con.cursor()

# Configuracion
app.secret_key = "mysecretkey"

# Importamos el controlador que contiene las rutas de la aplicacion
from Controlador import *

# Iniciamos la app
if __name__ == "__main__":
    app.run(port=3000, debug=True)
