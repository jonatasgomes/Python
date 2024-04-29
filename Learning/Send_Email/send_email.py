import smtplib
from email.message import EmailMessage
import env

# Create the email message
msg = EmailMessage()
msg.set_content("Hello, this is the body of the email!")
msg['Subject'] = "Test Email from Python"
msg['From'] = env.username
msg['To'] = "jalves@cargojet.com"

# Set up the SMTP server
server = smtplib.SMTP_SSL(env.host, env.port)  # SMTP server address and port
server.login(env.username, env.password)  # Your email account and password
server.sendmail(sender, recipients)
server.quit()
