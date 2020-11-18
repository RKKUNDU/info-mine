import smtplib
import ssl
import os
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email import encoders
import sys
sys.path.append("../../")
sys.path.append("functionalities/dept_mail/")
from usersapi.views import Users


class send_mail:
    def send_m(self,targets,subject,body,attach,sender_whatsapp_no,filepath=None,cc=[],bcc=[]):
        try:
            ret=""

            #Fetch CSE Ldap username and password from whatsapp number
            user = Users(sender_whatsapp_no)
            sender,passwd=user.getCSEMail()

            if sender is None or passwd is None:
                return "Please register department email credentials"

            #Fetch IITB username and password from whatsapp number
            user1 = Users(sender_whatsapp_no)
            username,password=user1.getLDAP()

            if username is None or password is None:
                return "Please register IITB email credentials"

            #Smtp url and port
            host = 'smtp-auth.iitb.ac.in'
            port = int(587)

            targets=str(targets)
            targets=targets.split(',')

            #Message treated as multipart
            msg = MIMEMultipart()
            msg['Subject'] = subject
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
                Body = body
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
            ret=ret+"Email sent successfully !!!"
            server.quit()

        except:
            ret=ret+"Sending failed !! Check username / password / filepath"
            os.remove("configs/dept_mail")
            os.remove("configs/dept_mail.key")
        return ret


