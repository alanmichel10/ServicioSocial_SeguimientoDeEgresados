from flask import Flask, flash, jsonify, request
from flask_mysqldb import MySQL
import mysql.connector
import logging

app = Flask(__name__)
mysql = MySQL(app)

# Configurar logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@app.route('/verificar_correo', methods=['POST'])
def verificar_correo():
    logger.debug("Recibida petición de verificación de correo")
    try:
        data = request.get_json()
        logger.debug(f"Datos recibidos: {data}")

        if not data:
            logger.error("No se recibieron datos JSON")
            return jsonify({'error': 'No se recibieron datos'}), 400

        correo = data.get('correo')
        logger.debug(f"Correo a verificar: {correo}")

        if not correo:
            logger.error("Correo no proporcionado en la petición")
            return jsonify({'error': 'Correo no proporcionado'}), 400

        existe = check_email_exists(correo)
        logger.debug(f"Resultado de verificación: {existe}")

        return jsonify({'existe': existe})

    except Exception as e:
        logger.error(f"Error en verificar_correo: {str(e)}")
        return jsonify({'error': str(e)}), 500

# Modificar la función check_email_exists para manejar mejor los errores
def check_email_exists(correo):
    logger.debug(f"Verificando existencia del correo: {correo}")
    cursor = mysql.connection.cursor()
    try:
        query = "SELECT Correo_Alumno FROM general WHERE Correo_Alumno = %s"
        logger.debug(f"Ejecutando query: {query} con parámetro: {correo}")

        cursor.execute(query, (correo,))
        result = cursor.fetchone()

        exists = result is not None
        logger.debug(f"Resultado de la consulta: {exists}")

        return exists

    except Exception as e:
        logger.error(f"Error en check_email_exists: {str(e)}")
        return False
    finally:
        cursor.close()


def insertGeneral(nombre_gen, apellido_p, apellido_m, sexo, telefono, correo,
                  c_postal, pais, estado, ciudad, colonia, nacionalidad,
                  f_nacimiento, carreras_interes, tipo_posgrado):
    """
    Inserta los datos generales del aspirante y sus carreras de interés
    """
    # Verificamos si el correo ya existe
    if check_email_exists(correo):
        raise ValueError("Este correo electrónico ya está registrado. Por favor, utiliza otro correo.")

    cursor = mysql.connection.cursor()
    try:
        # Inserta los datos generales en la tabla 'general'
        insert_general_query = """
            INSERT INTO general (
                nombre, apellidoP, apellidoM, sexo, celular,
                Correo_Alumno, codigoPostal, Pais, Estado,
                Ciudad, Colonia, Nacionalidad, fechaNacimiento
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_general_query, (
            nombre_gen, apellido_p, apellido_m, sexo, telefono,
            correo, c_postal, pais, estado, ciudad, colonia,
            nacionalidad, f_nacimiento
        ))

        # Inserta la selección de posgrado en la tabla 'aspirante_carrera'
        insert_carrera_query = """
            INSERT INTO aspirante_carrera (correo_alumno, idCarrera)
            VALUES (%s, %s)
        """
        for carrera in carreras_interes:
            if carrera:  # Verifica que el valor no esté vacío
                cursor.execute(insert_carrera_query, (correo, carrera))

        # Commit de las transacciones
        mysql.connection.commit()
        return True

    except mysql.connector.Error as err:
        mysql.connection.rollback()
        logger.error(f"MySQL Error: {err}")
        if err.errno == 1062:  # Código de error para entrada duplicada
            raise ValueError("Este correo electrónico ya está registrado. Por favor, utiliza otro correo.")
        else:
            raise ValueError(f"Error al insertar datos: {str(err)}")
    except Exception as e:
        mysql.connection.rollback()
        logger.error(f"Error general: {e}")
        raise ValueError(f"Error inesperado al insertar datos: {str(e)}")
    finally:
        cursor.close()


