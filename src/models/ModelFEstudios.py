from flask import Flask
from flask_mysqldb import MySQL
import mysql.connector

app = Flask(__name__)
mysql=MySQL(app)

def insertEstudios(uni_proce, carrera, titulado, ciclo, ingles, promedio, correo):
     cursor = mysql.connection.cursor()
     cursor.execute("INSERT INTO estudios (Correo_A, centroUniversitario, carrera, titulado, cicloEgreso, nivelIngles, Promedio) VALUES (%s, %s, %s, %s, %s, %s, %s);", 
                    (correo, uni_proce, carrera, titulado, ciclo, ingles, promedio))
     mysql.connection.commit()
     cursor.close()
     mysql.connection.close()