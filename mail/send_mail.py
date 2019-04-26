import smtplib
import email.utils
from email.mime.text import MIMEText
import getpass
EMAIL_HOST = 'mail.strangemother.org'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'webmaster@strangemother.org'
EMAIL_HOST_PASSWORD = 'FHoCLIlke)Ft'
# Prompt the user for connection info
to_email = 'webmaster@strangemother.org'
servername = EMAIL_HOST
username =EMAIL_HOST_USER
password =EMAIL_HOST_PASSWORD
from_email= EMAIL_HOST_USER

def send():
    # Create the message
    msg = MIMEText('Test message from python script.')
    msg.set_unixfrom('author')
    msg['To'] = email.utils.formataddr(('Recipient', to_email))
    msg['From'] = email.utils.formataddr(('Author', from_email))
    msg['Subject'] = 'python send'

    server = smtplib.SMTP(servername)
    try:
        server.set_debuglevel(True)

        # identify ourselves, prompting server for supported features
        server.ehlo()

        # If we can encrypt this session, do it
        if server.has_extn('STARTTLS'):
            server.starttls()
            server.ehlo() # re-identify ourselves over TLS connection

        server.login(username, password)
        server.sendmail(from_email, [to_email], msg.as_string())
    finally:
        server.quit()
