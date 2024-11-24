import smtplib
import pandas as pd
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


# Configuración de credenciales y destinatario
mi_correo = "jorge@gmail.com"          # tu correo de Gmail
mi_contraseña = ".........."           # tu contraseña de Gmail o la contraseña de aplicación
destinatario = "paciente@gmail.com"  # destinatario del correo

# Crear el mensaje con formato MIME
mensaje = MIMEMultipart("alternative")
mensaje["Subject"] = "Resumen Semanal de estado de salud"
mensaje["From"] = mi_correo
mensaje["To"] = destinatario

# Contenido del correo en formato HTML
html = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
       
    </head>
    <body>
    </body>
    </html>
"""

# Adjuntar el contenido HTML al mensaje
parte_html = MIMEText(html, "html")
mensaje.attach(parte_html)

# Enviar el correo usando smtplib
try:
    # Conectarse al servidor SMTP de Gmail
    servidor = smtplib.SMTP("smtp.gmail.com", 587)
    servidor.starttls()  # Protocolo seguro
    servidor.login(mi_correo, mi_contraseña)
    servidor.sendmail(mi_correo, destinatario, mensaje.as_string())
    print("Correo enviado correctamente.")
except Exception as e:
    print(f"Error al enviar el correo: {e}")
finally:
    servidor.quit()  # Cerrar la conexión
