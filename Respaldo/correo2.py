import mysql.connector
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from reportlab.pdfgen import canvas
from datetime import datetime
import io
from reportlab.lib import colors


# Configuración de la conexión a la base de datos MySQL
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "root",
    "database": "cumpleaños"
}

# Conectarse a la base de datos
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

# Obtener la fecha actual
hoy = datetime.now()
fecha_actual = hoy.strftime("%Y-%m-%d")

# Consultar profesores cuyo cumpleaños es hoy
consulta = f"SELECT nombre, correo, fecha_nacimiento FROM profesores WHERE DATE_FORMAT(fecha_nacimiento, '%m-%d') = DATE_FORMAT('{fecha_actual}', '%m-%d')"
cursor.execute(consulta)
resultados = cursor.fetchall()

# Configuración del servidor de correo
remitente = "udgcorreos115@gmail.com"
contraseña = "mtzy zsdn vwnx jwdx"  # Recuerda no incluir contraseñas en texto claro en tu código
servidor = smtplib.SMTP('smtp.gmail.com', 587)
servidor.starttls()
servidor.login(remitente, contraseña)

# Función para crear un PDF personalizado de felicitación
def crear_pdf(nombre, fecha_nacimiento):
    packet = io.BytesIO()
    c = canvas.Canvas(packet)
    
    # Cambiar el color y tamaño de la fuente
    c.setFont("Helvetica-Bold", 16)
    c.setFillColor(colors.red)  # Puedes cambiar el color según tus preferencias

    # Agregar texto al PDF
    c.drawString(100, 750, f"¡Feliz Cumpleaños, {nombre}!")
    c.drawString(100, 730, "Esperamos que tengas un día maravilloso.")

    # Cambiar color y tamaño para el siguiente texto
    c.setFont("Helvetica", 12)
    c.setFillColor(colors.black)

    # Agregar más texto si es necesario
    # ...

    c.save()
    packet.seek(0)
    return packet

# Enviar correos de cumpleaños con PDF personalizado
for nombre, correo_destinatario, fecha_nacimiento in resultados:
    # Crear el PDF personalizado
    pdf = crear_pdf(nombre, fecha_nacimiento)

    # Adjuntar el PDF al correo
    pdf_attachment = MIMEApplication(pdf.read(), _subtype="pdf")
    pdf_attachment.add_header('Content-Disposition', f'attachment; filename=felicitacion_{nombre}.pdf')

    # Creación del correo
    correo_enviar = MIMEMultipart()
    correo_enviar['From'] = remitente
    correo_enviar['To'] = correo_destinatario
    correo_enviar['Subject'] = "¡Feliz Cumpleaños!"

    # Mensaje de felicitación
    mensaje = f"¡Feliz Cumpleaños, {nombre}! Esperamos que tengas un día maravilloso."
    correo_enviar.attach(MIMEText(mensaje, 'plain'))

    # Adjuntar el PDF
    correo_enviar.attach(pdf_attachment)

    # Convertir el correo a cadena y enviarlo directamente con sendmail
    cuerpo_correo = correo_enviar.as_string()
    servidor.sendmail(remitente, [correo_destinatario], cuerpo_correo)
    
# Cerrar la conexión con la base de datos
conn.close()

# Cerrar la conexión con el servidor de correo
servidor.quit()
