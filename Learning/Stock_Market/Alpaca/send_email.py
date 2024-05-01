import smtplib
from email.mime.text import MIMEText
import env

def send_email(recipients, subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = env.EMAIL_USERNAME
    msg['To'] = ', '.join(recipients)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
        smtp_server.login(env.EMAIL_USERNAME, env.EMAIL_PASSWORD)
        smtp_server.sendmail(env.EMAIL_USERNAME, recipients, msg.as_string())
    return None
