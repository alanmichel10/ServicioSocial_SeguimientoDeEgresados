from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import secrets
import string
import mysql.connector
import random
import hashlib


correo = None
def get_var():
     return correo

def set_var(x):
     global correo
     correo = x

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'
mysql=MySQL(app)


#FORMULARIO--------------------------------------------------------------------------

# Página de Selección
@app.route('/seleccion', methods=['GET', 'POST'])
def seleccion():
    if request.method == 'POST':
        tipo_posgrado = request.form.get('posgradoInput')
        selecciones = request.form.getlist('seleccionesPosgrado')

        session['tipo_posgrado'] = tipo_posgrado
        session['carreras_interes'] = selecciones
        return redirect(url_for('general'))

    return render_template('seleccion.html')

@app.route('/general', methods=['GET', 'POST'])
def general():
    if request.method == 'POST':
        nombre_gen = request.form['nombres']
        apellido_p = request.form['apellido_p']
        apellido_m = request.form['apellido_m']
        sexo = request.form['sexo']
        telefono = request.form['tel_contacto']
        correo = request.form['correo_alumno']
        c_postal = request.form['codigo_postal']
        pais = request.form['pais']
        estado = request.form['estado']
        ciudad = request.form['ciudad']
        colonia = request.form['colonia']
        nacionalidad = request.form['nacionalidad']
        f_nacimiento = request.form['f_nacimiento']

        # Obtener las carreras de interés de la sesión
        carreras_interes = session.get('carreras_interes', [])
        carreras_interes = [int(x) for x in carreras_interes]

        insertGeneral(nombre_gen, apellido_p, apellido_m, sexo, telefono, correo, c_postal, pais, estado, ciudad, colonia, nacionalidad, f_nacimiento)
        return redirect(url_for('estudios'))
    
    return render_template('Generales.html')

@app.route('/estudios', methods=['GET', 'POST'])
def estudios():
    if request.method == 'POST':
          uni_proce = request.form['nivel']
          carrera = request.form['carrera']
          titulado = request.form['titulado']
          ciclo = request.form['ciclo']
          ingles = request.form['ingles']
          promedio = request.form['promedio']
          insertEstudios(uni_proce, carrera, titulado, ciclo, ingles, promedio, get_var())
          return redirect(url_for('laboral'))

    return render_template('Estudios.html')


@app.route('/laboral', methods=['GET', 'POST'])
def laboral():
    if request.method == 'POST':
         siOno = request.form['trabajasiono']
         lugar= request.form['lugardetrabajo']
         horario= request.form['horariolaboral']
         puesto= request.form['puestolaboral']
         sector = request.form['sector']
         
         contrasena, correo_usuario = insertLaboral(siOno, lugar, horario, puesto, sector, get_var())

         destinatario = correo_usuario  # Usando el correo registrado
         asunto = "Confirmación de Registro"
         mensaje_base = "Gracias por registrarte. Tu información ha sido recibida con éxito."
         mensaje_extra = """
         
         Bienvenido a nuestra comunidad de egresados.

         Nos complace informarte que tu información ha sido registrada con éxito. Gracias por tu interés en nuestros programas de posgrado.

         Para obtener más información y continuar con el proceso, por favor, inicia sesión con la cuenta y contraseña que se te proporcionaron en este correo. Puedes hacerlo a través del siguiente enlace: LINK DEL LOGIN.

         Si tienes alguna pregunta o necesitas asistencia, no dudes en contactarnos.

         ¡Que tengas un excelente día!


         """

         enviar_correo(destinatario, asunto, mensaje_base, contrasena, correo_usuario, mensaje_extra)
    
         flash('Registro completo')
         return redirect(url_for('inicio'))
    
    return render_template('Laboral.html')


@app.route('/dashboard')
def dashboard():
    cursor = mysql.connection.cursor()
    
    query = """
    SELECT 
        g.nombre, g.apellidoP, g.apellidoM, g.sexo, g.celular, 
        g.Correo_Alumno, g.codigoPostal, g.Pais, g.Estado, 
        g.Ciudad, g.Colonia, g.Nacionalidad, g.fechaNacimiento, g.posgrado,
        e.centroUniversitario, e.carrera, e.titulado, e.cicloEgreso, e.nivelIngles, e.Promedio,
        l.estatus AS Trabajando, l.nombre AS Direccion_trabajo, l.Horario_Laboral, l.Puesto_Trabajo, l.Sector
    FROM 
        general g
    LEFT JOIN 
        estudios e ON g.Correo_Alumno = e.Correo_A
    LEFT JOIN 
        laboral l ON g.Correo_Alumno = l.Correo_Alu
    """
    
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    
    return render_template('dashboard.html', data=data)


@app.route('/inicio')
def inicio():
     return render_template('inicio.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form['correo']
        clave = request.form['clave']

        cursor = mysql.connection.cursor()
        # Primero, obtén el hash almacenado para este correo
        cursor.execute("SELECT clave FROM cuenta WHERE correo = %s", (correo,))
        resultado = cursor.fetchone()
        
        if resultado:
            clave_almacenada = resultado[0]
            # Ahora, has la contraseña ingresada
            clave_hasheada = hashlib.sha256(clave.encode()).hexdigest()
            
            # Compara los hashes
            if clave_hasheada == clave_almacenada:
                # Autenticación exitosa
                session['user_id'] = correo  # O el ID del usuario si lo tienes
                return redirect(url_for('dashboard'))
            else:
                flash('Credenciales incorrectas. Por favor, inténtalo de nuevo.', 'danger')
        else:
            flash('Usuario no encontrado.', 'danger')
        
        return redirect(url_for('login'))

    return render_template('login.html')


def Error404(error):
    return '<h1>Contacte a soporte tecnico</h1>'

def generar_contrasena(longitud=10):
    caracteres = string.ascii_letters + string.digits
    contrasena = ''.join(random.choice(caracteres) for i in range(longitud))
    return contrasena

def insertGeneral(nombre_gen, apellido_p, apellido_m, sexo, telefono, correo, c_postal, pais, estado, ciudad, colonia, nacionalidad, f_nacimiento, carreras_interes):
    cursor = mysql.connection.cursor()

    # Inserta los datos generales en la tabla 'general'
    cursor.execute("INSERT INTO general (nombre, apellidoP, apellidoM, sexo, celular, Correo_Alumno, codigoPostal, Pais, Estado, Ciudad, Colonia, Nacionalidad, fechaNacimiento) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);",
                   (nombre_gen, apellido_p, apellido_m, sexo, telefono, correo, c_postal, pais, estado, ciudad, colonia, nacionalidad, f_nacimiento))
    
    # Inserta la selección de posgrado en la tabla 'aspirante_carrera'
    for carrera in carreras_interes:
        cursor.execute("INSERT INTO aspirante_carrera (Correo_Alumno, idCarrera) VALUES (%s, %s);",
                       (correo, carrera))
    
    mysql.connection.commit()
    cursor.close()

def insertEstudios(uni_proce, carrera, titulado, ciclo, ingles, promedio, correo):
     cursor = mysql.connection.cursor()
     cursor.execute("INSERT INTO estudios (Correo_A, centroUniversitario, carrera, titulado, cicloEgreso, nivelIngles, Promedio) VALUES (%s, %s, %s, %s, %s, %s, %s);", 
                    (correo, uni_proce, carrera, titulado, ciclo, ingles, promedio))
     mysql.connection.commit()
     cursor.close()
     mysql.connection.close()

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


def enviar_correo(destinatario, asunto, mensaje_base, contrasena=None, correo_usuario=None, mensaje_extra=None):
    remitente = "udgcorreos115@gmail.com"
    contraseña = "mtzy zsdn vwnx jwdx"

    # Configuración del servidor de correo
    servidor = smtplib.SMTP('smtp.gmail.com', 587)
    servidor.starttls()
    servidor.login(remitente, contraseña)

    # Creación del correo
    correo = MIMEMultipart()
    correo['From'] = remitente
    correo['To'] = destinatario
    correo['Subject'] = asunto

    # Diseño mejorado del correo en HTML
    mensaje_html = f"""
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                color: #333333;
            }}
            .container {{
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
                background-color: #f9f9f9;
                border-radius: 5px;
            }}
            .header {{
                background-color: #003366;
                color: white;
                padding: 20px;
                text-align: center;
                border-radius: 5px 5px 0 0;
            }}
            .content {{
                background-color: white;
                padding: 20px;
                border-radius: 0 0 5px 5px;
            }}
            .footer {{
                text-align: center;
                margin-top: 20px;
                font-size: 0.8em;
                color: #666666;
            }}
            .highlight {{
                background-color: #fffacd;
                padding: 10px;
                border-radius: 5px;
                margin: 10px 0;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Bienvenido a Nuestra Comunidad de Egresados</h1>
            </div>
            <div class="content">
                <p>{mensaje_base}</p>
    """

    if correo_usuario and contrasena:
        mensaje_html += f"""
                <div class="highlight">
                    <p><strong>Tu correo registrado:</strong> {correo_usuario}</p>
                    <p><strong>Tu contraseña:</strong> <span style="font-size: 1.2em; background-color: #e6f2ff; padding: 5px; border-radius: 3px;">{contrasena}</span></p>
                </div>
        """
    
    if mensaje_extra:
        mensaje_html += f"<p>{mensaje_extra}</p>"

    mensaje_html += """
                <p>Si tienes alguna pregunta o necesitas asistencia, no dudes en contactarnos.</p>
                <p>¡Que tengas un excelente día!</p>
            </div>
            <div class="footer">
                <p>&copy; 2024 Universidad de Guadalajara. Todos los derechos reservados.</p>
            </div>
        </div>
    </body>
    </html>
    """

    correo.attach(MIMEText(mensaje_html, 'html'))

    # Enviar el correo
    servidor.send_message(correo)
    servidor.quit()