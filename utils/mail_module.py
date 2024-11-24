import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Configuration mail account
mail = "zurdovendrell1998@gmail.com"
mail_password = "ttnq yhux kqsd sdhb"
addressee = "baicartg@uoc.edu"

message = MIMEMultipart("alternative")
message["Subject"] = "Resumen Semanal de estado de salud"
message["From"] = mail
message["To"] = addressee

# Content html
with open("template_mail.html", "r", encoding="utf-8") as file:
    html_content = file.read()

parte_html = MIMEText(html_content, "html")
message.attach(parte_html)

# Connection and send email
try:
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(mail, mail_password)
    server.sendmail(mail, addressee, message.as_string())
    print("Correo enviado correctamente.")
except Exception as e:
    print(f"Error al enviar el correo: {e}")
finally:
    server.quit()
