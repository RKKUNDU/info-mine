from cryptography.fernet import Fernet 
import sys
sys.path.append('../')
class Key:
    '''
    self.key is in bytes
    store key in the file as string
    '''
    def __init__(self):
        '''
        Initializes the encryption key
        '''
        self.key = Fernet.generate_key()
    
    def read_key_from_file(self, path):
        '''
        Read the encryption key from a file
        Input:
            path (string): path to the file
        '''
        f = open(path, "r")
        self.key = bytes(f.read(), 'utf-8')

    def write_key_to_file(self, path):
        '''
        Write the encryption key to a file
        Input:
            path (string): path to the file
        '''
        f = open(path, "w")
        f.write(self.key.decode('utf-8'))

    def encrypt(self, txt):
        '''
        Encrypt the text with the encryption key
        Input:
            txt (string): text to encrypt
        Returns:
            encrypted text (string)
        '''
        f = Fernet(self.key)
        encrypted = f.encrypt(bytes(txt, 'utf-8')).decode('utf-8')
        return encrypted

    def decrypt(self, encrypted):
        '''
        Decrypt the text with the encryption key
        Input:
            txt (string): text to decrypt
        Returns:
            decrypted text (string)
        '''
        f = Fernet(self.key)
        txt = f.decrypt(bytes(encrypted, 'utf-8')).decode('utf-8')
        return txt

    def encrypt_and_write_to_file(self, txt, path):
        '''
        Encrypt the text and write it to a file
        Input:
            txt (string): text to encrypt
            path (string): path of the file to store the text
        '''
        encrypted = self.encrypt(txt)
        f = open(path, "w")
        f.write(encrypted)
   
    def read_from_file_and_decrypt(self, path):
        '''
        Read from a file and decrypt the text
        Input:
            path (string): path of the file to be read from
        Returns:
            decrypted file (string)
        '''
        f = open(path, "r")
        txt = f.read()
        decrypted = self.decrypt(txt)
        return decrypted
        