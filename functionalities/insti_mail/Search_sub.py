import imaplib
import email
from email.header import decode_header
import webbrowser
import os
import sys
from security.insti_credentials import insti_credentials

class search_sub:
    def subject(self,sub,limit=5):
        try:
            s= str(sub)
            Cred=insti_credentials()
            username = str(Cred.get_stored_username())
            password=str(Cred.get_stored_password())
            imap_url = 'imap.iitb.ac.in'
            incoming_port = int(993)

            connection = imaplib.IMAP4_SSL(imap_url,incoming_port)
            # authenticate
            connection.login(username, password)
            # number of top emails to fetch
            status, messages = connection.select("INBOX")
            # total number of emails
            messages = int(messages[0])
            j=0
            try:
                for i in range(messages, 0, -1):
                    
                    # fetch the email message by ID
                    res, msg = connection.fetch(str(i), "(RFC822)")
                    for response in msg:
                        if isinstance(response, tuple):
                            # parse a bytes email into a message object
                            msg = email.message_from_bytes(response[1])
                            # decode the email subject
                            subject = decode_header(msg["Subject"])[0][0]
                            if isinstance(subject, bytes):
                                # if it's a bytes, decode to str
                                subject = subject.decode()
                            # email sender
                            from_ = msg.get("From")
                            dt=msg.get("Date")
                            sub=subject.lower() 
                            #print(sub)
                            if sub.__contains__(s):
                                if j >=limit:
                                    raise StopIteration
                                
                                j=j+1
                                print("="*200)
                                st = "Message Number :- "+str(j)
                                st=st.center(200)
                                print(st)
                                print("="*200)
                                print('\n')
                                print("Subject:", subject)
                                print('\n')
                                print("Date:", dt)
                                print('\n')
                                print("From:", from_)
                                print('\n')
                                # if the email message is multipart
                                if msg.is_multipart():
                                    # iterate over email parts
                                    for part in msg.walk():
                                        # extract content type of email
                                        content_type = part.get_content_type()
                                        content_disposition = str(part.get("Content-Disposition"))
                                        try:
                                            # get the email body
                                            body = part.get_payload(decode=True).decode()
                                        except:
                                            pass
                                        if content_type == "text/plain" and "attachment" not in content_disposition:
                                            # print text/plain emails and skip attachments
                                            print(body)
                                        elif "attachment" in content_disposition:
                                            # download attachment
                                            filename = part.get_filename()
                                            if filename:
                                                if not os.path.isdir(subject):
                                                    # make a folder for this email (named after the subject)
                                                    os.mkdir(subject)
                                                filepath = os.path.join(subject, filename)
                                                # download attachment and save it
                                                open(filepath, "wb").write(part.get_payload(decode=True))
                                else:
                                    # extract content type of email
                                    content_type = msg.get_content_type()
                                    # get the email body
                                    body = msg.get_payload(decode=True).decode()
                                    if content_type == "text/plain":
                                        # print only text email parts
                                        print(body)
                                if content_type == "text/html":
                                    # if it's HTML, create a new HTML file and open it in browser
                                    if not os.path.isdir(subject):
                                        # make a folder for this email (named after the subject)
                                        os.mkdir(subject)
                                    filename = f"{subject[:50]}.html"
                                    filepath = os.path.join(subject, filename)
                                    # write the file
                                    open(filepath, "w").write(body)
                                    print(filepath)
                                    # open in the default browser
                                    #webbrowser.open(filepath)
                
                            else:
                                pass
            except StopIteration: pass
            connection.close()
            connection.logout()
        except:
            print("Invalid username / password ")
            os.remove("configs/insti_mail")
            os.remove("configs/insti_mail.key")
