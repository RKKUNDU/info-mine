import imaplib
import email
from email.header import decode_header
import webbrowser
import os
import datetime
import sys


s1 = str(sys.argv[1])
s2 = str(sys.argv[2])
print(s1)
print(s2)

t1=datetime.datetime(int(s1[4:]),int(s1[2:4]),int(s1[0:2]))
t2=datetime.datetime(int(s2[4:]),int(s2[2:4]),int(s2[0:2]))
print(t1)
print(t2)

f = open("key.txt", "r")
username=str(f.readlines(1))
username=username[2:-4]
password=str(f.readlines(2))
password=password[2:-2]
imap_url = 'imap.iitb.ac.in'
incoming_port = int(993)


connection = imaplib.IMAP4_SSL(imap_url,incoming_port)
# authenticate
connection.login(username, password)
# number of top emails to fetch
status, messages = connection.select("INBOX")
# total number of emails
messages = int(messages[0])

# for i in range(1,messages+1):
#     res, msg = connection.fetch(str(i), "(RFC822)")
#     msg.get

for i in range(messages, 0, -1):
    print('\n\n')
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
            if date_[5]!='0':
                date_=date_[0:5]+'0'+date_[5:15]

            date_dt1 = datetime.datetime.strptime(date_, '%a, %d %b %Y')
           
            print(date_dt1)
            
           
            if date_dt1 >= t1 and date_dt1 <=t2 :
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
                print("="*180)
                print('\n\n')
            else:
                print("no match")
connection.close()
connection.logout()