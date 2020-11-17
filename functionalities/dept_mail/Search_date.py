import imaplib
import email
from email.header import decode_header
import webbrowser
import os
import datetime
import sys
from dept_credentials import dept_credentials

class search_date:
    def date_(self,date1,date2):
        try:
            s1 = str(date1)
            s2 = str(date2)
            # print(s1)
            # print(s2)

            t1=datetime.datetime(int(s1[4:]),int(s1[2:4]),int(s1[0:2]))
            t2=datetime.datetime(int(s2[4:]),int(s2[2:4]),int(s2[0:2]))
            # print(t1)
            # print(t2)

            Cred=dept_credentials()
            username = str(Cred.get_stored_username())
            password=str(Cred.get_stored_password())
            imap_url = 'imap.cse.iitb.ac.in'
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
                            date_ = str(msg.get("Date"))[0:16]
                            if date_[7]!=' ':
                                date_=date_[0:5]+'0'+date_[5:15]
                            date_dt1 = datetime.datetime.strptime(date_, '%a, %d %b %Y')
                            if date_dt1 < t1:
                                raise StopIteration
                        
                            if date_dt1 >= t1 and date_dt1 <=t2 :
                                if j >=5:
                                    raise StopIteration
                                
                                j=j+1
                                print("="*200)
                                st = "Message Number :- "+str(j)
                                st=st.center(200)
                                print(st)
                                print("="*200)
                                print('\n')
                                print("Subject:", subject)
                                print("From:", from_)
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
                                    # open in the default browser
                                    #webbrowser.open(filepath)
                                    #print(filepath)
                            
                            else:
                                pass

            except StopIteration :
                pass

            connection.close()
            connection.logout()
        except:
            print("Invalid username / password ")
            os.remove("configs/dept_mail")
            os.remove("configs/dept_mail.key")