from flask import Flask
from flask_mysqldb import MySQL
import mysql.connector

from models.ModelContraseña import generar_contrasena

app = Flask(__name__)
mysql=MySQL(app)




def insertLaboral(siOno, lugar, horario, puesto, sector, correo):
    contrasena = generar_contrasena()  # Generar una contraseña aleatoria

    cursor = mysql.connection.cursor()

    cursor.execute("INSERT INTO laboral (estatus, nombre, Horario_Laboral, Puesto_Trabajo, Sector, Correo_Alu) VALUES (%s, %s, %s, %s, %s, %s);", 
                   (siOno, lugar, horario, puesto, sector, correo))
    mysql.connection.commit()

    # Insertar la cuenta y contraseña en la base de datos
    cursor.execute("INSERT INTO cuenta (correo, clave) VALUES (%s, %s);", (correo, contrasena))
    mysql.connection.commit()

    cursor.close()
    mysql.connection.close()

    return contrasena, correo  # Retornar la contraseña generada
