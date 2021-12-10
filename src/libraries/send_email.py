import smtplib
from config.config import gmail_user, gmail_password,  host, puerto


def send_email(to, subject, message):
    email_text = f"""From: {gmail_user}
To: {", ".join([to])}
Subject: {subject}

{message}
    """

    try:
        server = smtplib.SMTP_SSL(host, puerto)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(gmail_user, to, email_text)
        server.close()
        print("email send")
        return True
    except Exception as e:
        print("error to send email")
        print(e)
        return False



#to = "wisrovi.rodriguez@gmail.com"
#subject = "correo prueba"
#message = """hola mundo"""

#send_email(to, subject, message)