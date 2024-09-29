from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

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