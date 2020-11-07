
import smtplib
import ssl
from email.mime.text import MIMEText

f = open("key.txt", "r")
username=str(f.readlines(1))
username=username[2:-4]
password=str(f.readlines(2))
password=password[2:-2]

host = 'smtp-auth.iitb.ac.in'
port = int(587)

sender = '203050098@iitb.ac.in'
targets = ['203050030@iitb.ac.in','pranshuchourasia786@gmail.com']

msg = MIMEText('Hi, i am pranshu ?')
msg['Subject'] = 'Hello'
msg['From'] = sender
msg['To'] = ', '.join(targets)


server = smtplib.SMTP(host, port)
server.starttls(context=ssl.create_default_context())
server.login(username, password)
server.sendmail(sender, targets, msg.as_string())
server.quit()