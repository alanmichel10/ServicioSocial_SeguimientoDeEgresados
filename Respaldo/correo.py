import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def enviar_correo(destinatario, asunto, mensaje):
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

    # Agregar el mensaje al correo
    correo.attach(MIMEText(mensaje, 'plain'))

    # Enviar el correo
    servidor.send_message(correo)
    servidor.quit()

# Uso de la función
enviar_correo("alan.jimenez1350@alumnos.udg.mx", "PRUEBA", "HOLA ESTO ES UNA PINSHI PRUEBA")
