from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from os import environ
from sys import stderr

load_dotenv()

def send_email(email, language):
    if language:
        assunto = 'Thank you'
        corpo = """<html>
  <body>
    <p>Hi,</p>
    <p>Thank you so much for getting in touch through my portfolio. I truly appreciate the time you took to share your message and contact details. I'm very happy about your interest!</p>
    <p>I’ll carefully review what you sent and will get back to you as soon as possible.</p>
    <p>Talk soon, and thanks again!</p>
    <p>Best regards, Alexandre.</p>
    <br>
    <p style="color:gray; font-size:small;">This is an automatic message. Please do not reply to this email.</p>
  </body>
</html>"""
    else:
        assunto = 'Obrigado por contactar'
        corpo = """<html>
  <body>
    <p>Olá,</p>
    <p>Muito obrigado por entrar em contacto através do meu portfólio. Fico muito feliz com o seu interesse!</p>
    <p>Vou analisar com atenção o que me enviou e entrarei em contacto o mais brevemente possível.</p>
    <p>Atenciosamente, Alexandre.</p>
    <br>
    <p style="color:gray; font-size:small;">Esta é uma mensagem automática. Por favor, não responda a este e-mail.</p>
  </body>
</html>"""

    msg = MIMEMultipart()
    msg['From'] = environ.get('EMAIL')
    msg['To'] = email
    msg['Subject'] = assunto

    html = MIMEText(corpo, 'html')
    msg.attach(html)

    try:
        with SMTP('smtp.gmail.com', 587) as servidor:
            servidor.starttls()
            servidor.login(environ.get('EMAIL'), environ.get('EMAIL_KEY'))
            servidor.sendmail(environ.get('EMAIL'), email, msg.as_string())
            servidor.quit()
    except Exception as e:
        print("Error to send email for " + environ.get('EMAIL') + " " + str(e), file=stderr)
        pass