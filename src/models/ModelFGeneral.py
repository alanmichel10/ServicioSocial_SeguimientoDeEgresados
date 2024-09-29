from flask import Flask
from flask_mysqldb import MySQL
import mysql.connector

app = Flask(__name__)
mysql=MySQL(app)

def insertGeneral(nombre_gen, apellido_p, apellido_m, sexo, telefono, correo, c_postal, pais, estado, ciudad, colonia, nacionalidad, f_nacimiento, carreras_interes, tipo_posgrado):
    cursor = mysql.connection.cursor()

    # Inserta los datos generales en la tabla 'general'
    cursor.execute("INSERT INTO general (nombre, apellidoP, apellidoM, sexo, celular, Correo_Alumno, codigoPostal, Pais, Estado, Ciudad, Colonia, Nacionalidad, fechaNacimiento) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);",
                   (nombre_gen, apellido_p, apellido_m, sexo, telefono, correo, c_postal, pais, estado, ciudad, colonia, nacionalidad, f_nacimiento))
    
    
    # Inserta la selección de posgrado en la tabla 'aspirante_carrera'
    for carrera in carreras_interes:
        if carrera:  # Verifica que el valor no esté vacío
            print("Insertando carrera:", carrera)
            cursor.execute("INSERT INTO aspirante_carrera (correo_alumno, idCarrera) VALUES (%s, %s);", (correo, carrera))
    
    mysql.connection.commit()
    cursor.close()