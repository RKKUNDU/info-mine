
import smtplib
import ssl
import os
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
from email import encoders
from dept_credentials import dept_credentials
try:
    Cred=dept_credentials()
    username = str(Cred.get_stored_username())
    password=str(Cred.get_stored_password())

    host = 'smtp-auth.iitb.ac.in'
    port = int(587)

    sender = username
    targets=[]
    N=int(input('Please Enter number of people you want to send your E-mail : '))
    for i in range(0,N):
        temp = input('Enter E-mail : ' )
        targets.append(temp)

    msg = MIMEMultipart()
    Sub = input('Please Enter Subject : ')
    msg['Subject'] = Sub
    msg['From'] = sender
    msg['To'] = ', '.join(targets)
    # msg['CC'] = ', '.join(CC)
    # msg['BCC'] = ', '.join(BCC)
    Body = input('Please Enter body : ')
    txt = MIMEText(Body)
    msg.attach(txt)

    choice = str(input('Do you have attachment y/n : ')).lower()
    if choice == 'y':
        filepath = input('Enter full path of file : ')
    
        type_file = filepath.split('.')[-1]
        print(type_file)
        if type_file == 'txt':
            with open(filepath, "rb") as f:
                file1 = MIMEApplication(f.read(),_subtype='octet-stream', _encoder=encoders.encode_base64,)
                file1.add_header('Content-Disposition','attachment',filename=os.path.basename(filepath))
                msg.attach(file1)

        elif type_file == 'jpg' or type_file == 'png':
            with open(filepath, 'rb') as f:
                file1 = MIMEImage(f.read())
                file1.add_header('Content-Disposition','attachment',filename=os.path.basename(filepath))
                msg.attach(file1)

        else :
            with open(filepath, "rb") as f:
                file1 = MIMEApplication(f.read(),_subtype=type_file)
                file1.add_header('Content-Disposition','attachment',filename=os.path.basename(filepath))
                msg.attach(file1)

    server = smtplib.SMTP(host, port)
    server.starttls(context=ssl.create_default_context())
    server.login(username, password)
    server.sendmail(sender, targets, msg.as_string())
    print("Email sent successfully !!!")
    server.quit()
except:
    print("Sending failed !! Check username / password ")
    os.remove("configs/dept_mail")
    os.remove("configs/dept_mail.key")


