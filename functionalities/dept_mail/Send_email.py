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
            #Generate sender username and password
            Cred=dept_credentials()
            sender = str(Cred.get_stored_username())
            cd=insti_credentials()
            username = str(cd.get_stored_username())
            password = str(cd.get_stored_password())

            #Smtp url and port
            host = 'smtp-auth.iitb.ac.in'
            port = int(587)

            targets=str(targets)
            targets=targets.split(',')

            #Message treated as multipart
            msg = MIMEMultipart()
            s=""
            msg['Subject'] = s.join(subject)
            msg['From'] = sender
            msg['To'] = ', '.join(targets)

            #If mail contains cc
            if cc is not None:
                cc=str(cc)
                cc=cc.split(',')
                msg['CC'] = ', '.join(cc)
                targets=targets+cc

            #If mail contains bcc
            if bcc is not None :
                bcc=str(bcc)
                bcc=bcc.split(',')
                msg['BCC'] = ', '.join(bcc)
                targets=targets+bcc

            #If mail contains body
            if body is not None:
                b=""
                Body = b.join(body)
                txt = MIMEText(Body)
                msg.attach(txt)

            #If mail contains attachments
            if attach == True:
                filepath=str(filepath)
                #Split for multiple attachments
                path=filepath.split(',')
                for pt in path:
                    
                    type_file = pt.split('.')[-1]
                    #Txt type attachment
                    if type_file == 'txt':
                        with open(pt, "rb") as f:
                            file1 = MIMEApplication(f.read(),_subtype='octet-stream', _encoder=encoders.encode_base64,)
                            file1.add_header('Content-Disposition','attachment',filename=os.path.basename(pt))
                            msg.attach(file1)

                    #Image type attachment
                    elif type_file == 'jpg' or type_file == 'png':
                        with open(pt, 'rb') as f:
                            file1 = MIMEImage(f.read())
                            file1.add_header('Content-Disposition','attachment',filename=os.path.basename(pt))
                            msg.attach(file1)

                    #All other types of attachment
                    else :
                        with open(pt, "rb") as f:
                            file1 = MIMEApplication(f.read(),_subtype=type_file)
                            file1.add_header('Content-Disposition','attachment',filename=os.path.basename(pt))
                            msg.attach(file1)

            #Establishing smtp connection using STARTTLS
            server = smtplib.SMTP(host, port)
            server.starttls(context=ssl.create_default_context())

            #Authentication using username and password
            server.login(username, password)
            server.sendmail(sender, targets, msg.as_string())
            #Connection close
            print("Email sent successfully !!!")
            server.quit()
            
        except:
            print("Sending failed !! Check username / password / filepath")
            os.remove("configs/dept_mail")
            os.remove("configs/dept_mail.key")
            os.remove("configs/insti_mail")
            os.remove("configs/insti_mail.key")


