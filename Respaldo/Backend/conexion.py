import mysql.connector # se debe descargar la libreria "pip install mysql-connector-python
import json
conexion = mysql.connector.connect(
    host = "127.0.0.1",
    user = "root",
    password = "1234",
    db = "seg_egresados",
)

cursor = conexion.cursor()

def addUsuario(correo, contra):
    with open("registro.json") as archivo:
        datos = json.load(archivo)

        correo = datos["correo"]
        contra = datos["contra"]

    cursor.execute("insert into usuarios (correo, contraseña) values ('" + correo + "' ,'" + contra + "')")
    conexion.commit()
    cursor.close()
    conexion.close()

def datosGen(curp, nombre, apeP, apeM, correo, fNacimiento, codigoEstudiante, lugarNacimiento, estadoCivil, sexo, nCelular):
    with open ("datos.json") as archivo:
        datos = json.load(archivo)

        curp = datos["curp"]
        nombre = datos["nombre"]
        apeP = datos["apellidoPaterno"]
        apeM = datos["apellidoMaterno"]
        correo = datos["correo"]


#cursor.execute("select * from usuarios")
#for bd in cursor:  # type: ignore
#    print(bd)
