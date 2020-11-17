import smtplib
import ssl
import os
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
from email import encoders
from security.dept_credentials import dept_credentials
from security.insti_credentials import insti_credentials
class send_mail:
    def send_m(self,targets,subject,body,attach,filepath=None,cc=[],bcc=[]):
        try:
            Cred=dept_credentials()
            sender = str(Cred.get_stored_username())
        

            cd=insti_credentials()
            username = str(cd.get_stored_username())
            password = str(cd.get_stored_password())



            host = 'smtp-auth.iitb.ac.in'
            port = int(587)

            targets=str(targets)
            targets=targets.split(',')

            msg = MIMEMultipart()
            
            msg['Subject'] = subject
            msg['From'] = sender
            msg['To'] = ', '.join(targets)

            if cc is not None:
                cc=str(cc)
                cc=cc.split(',')
                msg['CC'] = ', '.join(cc)
                targets=targets+cc
            if bcc is not None :
                bcc=str(bcc)
                bcc=bcc.split(',')
                msg['BCC'] = ', '.join(bcc)
                targets=targets+bcc
            if body is not None:
                Body = body
                txt = MIMEText(Body)
                msg.attach(txt)
            if attach == True:
                type_file = filepath.split('.')[-1]
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
            print("Sending failed !! Check username / password / filepath")
            os.remove("configs/dept_mail")
            os.remove("configs/dept_mail.key")


