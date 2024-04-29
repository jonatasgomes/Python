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

#https://mailtrap.io/blog/python-send-email-gmail/#:~:text=To%20send%20an%20email%20with%20Python%20via%20Gmail%20SMTP%2C%20you,Transfer%20Protocol%20(SMTP)%20server.