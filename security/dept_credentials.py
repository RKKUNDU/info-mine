from security.keys import Key
import os.path
from os import path
import getpass

PATH = 'configs/' # set the path wrt to the calling function
class dept_credentials:
    def __init__(self):
        self.key = Key()

        if path.exists(PATH + 'dept_mail.key'):
            f = open(PATH + 'dept_mail.key', "r")
            self.key.key=bytes(f.read(), 'utf-8')
        
        if path.exists(PATH + 'dept_mail'):
            txt = self.key.read_from_file_and_decrypt(PATH + 'dept_mail')
            x=txt.split(',')
            user = x[0]
            passwd= x[1]
            self.username=user
            self.password=passwd
        else:
            self.key.write_key_to_file(PATH + 'dept_mail.key')
            uname=str(input("Enter CSE user name : "))
            pwd = getpass.getpass() 
            txt= uname+','+pwd
            self.key.encrypt_and_write_to_file(txt,PATH + 'dept_mail')
            txt = self.key.read_from_file_and_decrypt(PATH + 'dept_mail')
            x=txt.split(',')
            user = x[0]
            passwd= x[1]
            self.username=user
            self.password=passwd
           
    
    def get_stored_username(self):
        return self.username
    def get_stored_password(self):
        return self.password
