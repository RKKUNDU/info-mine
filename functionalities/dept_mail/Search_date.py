import imaplib
import email
from email.header import decode_header
import webbrowser
import os
import datetime
import sys
import os.path
from os import path
from security.dept_credentials import dept_credentials

class search_date:
    def date_(self,date1,date2,limit=5):
        try:
            #Get strings of dates 
            s1 = str(date1)
            s2 = str(date2)
            t1=datetime.datetime(int(s1[4:]),int(s1[2:4]),int(s1[0:2]))
            t2=datetime.datetime(int(s2[4:]),int(s2[2:4]),int(s2[0:2]))

            #Generate username and password
            Cred=dept_credentials()
            username = str(Cred.get_stored_username())
            password=str(Cred.get_stored_password())

            #Imap url and port
            imap_url = 'imap.cse.iitb.ac.in'
            incoming_port = int(993)

            #Establish connection
            connection = imaplib.IMAP4_SSL(imap_url,incoming_port)

            # Authentication using username and password
            connection.login(username, password)

            # Select Inbox for the connection
            status, messages = connection.select("INBOX")

            # Total number of emails
            messages = int(messages[0])
            j=0
            try:
                for i in range(messages, 0, -1):
                    
                    # Fetch emails by ID
                    res, msg = connection.fetch(str(i), "(RFC822)")
                    for response in msg:

                        if isinstance(response, tuple):

                            # Parse a bytes email into a message object
                            msg = email.message_from_bytes(response[1])
                            # Decode the email subject
                            subject = decode_header(msg["Subject"])[0][0]

                            if isinstance(subject, bytes):
                                # If subject is byte decode it to string
                                subject = subject.decode()

                            # Fetch information of Emails
                            from_ = msg.get("From")
                            dt=msg.get("Date")
                            
                            date_ = str(msg.get("Date"))[0:16]
                            if date_[7]!=' ':
                                date_=date_[0:5]+'0'+date_[5:15]
                            date_dt1 = datetime.datetime.strptime(date_, '%a, %d %b %Y')

                            #If you reach date less than first date stop
                            if date_dt1 < t1:
                                raise StopIteration

                            #Check range of dates between t1 and t2
                            if date_dt1 >= t1 and date_dt1 <=t2 :
                                #Checking for limit of mails 
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
                                # If Email has multiple part
                                if msg.is_multipart():
                                    # Span over each part

                                    for part in msg.walk():
                                    # Fetch content type
                                        content_type = part.get_content_type()
                                        content_disposition = str(part.get("Content-Disposition"))
                                        try:
                                            # Fetch body of Email
                                            body = part.get_payload(decode=True).decode()
                                        except:
                                            pass
                                        if content_type == "text/plain" and "attachment" not in content_disposition:

                                            # Print text/plain emails and skip attachments
                                            print(body)
                                        elif "attachment" in content_disposition:
                                            # Download attachments and save in local file
                                            filename = part.get_filename()
                                            if filename:
                                                if not os.path.isdir(subject):
                                                    # Make folder with name as subject
                                                    os.mkdir(subject)
                                                filepath = os.path.join(subject, filename)
                                                # Download attachment and save it
                                                open(filepath, "wb").write(part.get_payload(decode=True))
                                else:
                                    # Fetch content type
                                    content_type = msg.get_content_type()

                                    # Fetch body of Email
                                    body = msg.get_payload(decode=True).decode()
                                    if content_type == "text/plain":
                                        # Print only text email parts
                                        print(body)
                                    if content_type == "text/html":
                                        # If mail is HTML type create a new HTML file 
                                        if not os.path.isdir(subject):
                                            # Make a folder for this email with name as subject
                                            os.mkdir(subject)
                                        filename = f"{subject[:50]}.html"
                                        filepath = os.path.join(subject, filename)
                                        # Write the file
                                        open(filepath, "w").write(body)
                                    
                            else:
                                pass
            # Stop when limit reached
            except StopIteration :
                pass
            #Close connection and logout 
            connection.close()
            connection.logout()
        except:
            print("Invalid username / password ")
            if path.exists("configs/dept_mail"):
                os.remove("configs/dept_mail")
            if path.exists("configs/dept_mail.key"):
                os.remove("configs/dept_mail.key")
