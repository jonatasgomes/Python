import smtplib
from email.mime.text import MIMEText
import env

def send_email(subject, body, recipients):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = env.email
    msg['To'] = ', '.join(recipients)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
        smtp_server.login(env.email, env.password)
        smtp_server.sendmail(env.email, recipients, msg.as_string())
    print("Message sent!")

send_email("Email Subject", "This is the body of the text message", ['jonatasgomes@gmail.com'])
