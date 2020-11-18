import imaplib
import email
from email.header import decode_header
import webbrowser
import os
import sys
import pprint
from security.dept_credentials import dept_credentials

class search_topn:
    def top(self,N=5):
        try:
          
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

            # Fetch top N mails
            status, messages = connection.select("INBOX")

            #Total number of mails
            messages = int(messages[0])
            for i in range(messages, messages-N, -1):

                
                print("="*200)
                st = "Message Number :- "+str(messages-i+1)
                st=st.center(200)
                print(st)
                print("="*200)
                print('\n')
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
                        from_ = str(msg.get("From"))
                        dt=msg.get("Date")
                        print('\n')
                        print("Subject:", subject)
                        print('\n')
                        print("Date:", dt)
                        print('\n')
                        print("From:", from_)
                        print('\n')

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
            #Close connection and logout                 
            connection.close()
            connection.logout()
        except:
            print("Invalid username / password ")
            os.remove("configs/dept_mail")
            os.remove("configs/dept_mail.key")