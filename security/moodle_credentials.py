from security.keys import Key
import requests
from bs4 import BeautifulSoup as bs
import json
import os

PATH = 'configs/' # set the path wrt to the calling function
class moodle_credential:
    def __init__(self):
        '''
        Read token, userid from file if exists
        '''
        self.token = None
        self.userid = None
        self.key = Key()
        try:
            self.key.read_key_from_file(PATH + "moodle.key")
        except Exception as ex:
            # print("Error: ", ex)
            if os.path.exists(PATH + 'moodle.key'):
                os.remove(PATH + 'moodle.key')
            
            return
        
        if self.key.key == "":
            if os.path.exists(PATH + 'moodle.key'):
                os.remove(PATH + 'moodle.key')
            
            return

        try:    
            txt = self.key.read_from_file_and_decrypt(PATH + 'moodle')
            self.token = None # private token for api
            self.userid = None # userid of the user
            for x in txt.split(","):
                field = x.split("=")[0]
                value = x.split("=")[1]
                if field == "userid":
                    self.userid = value
                elif field == "token":
                    self.token = value
            
        except Exception as err:
            if os.path.exists(PATH + 'moodle.key'):
                os.remove(PATH + 'moodle.key')

            # print("Error: ", err)

    def get_stored_token(self):
        '''
        return stored token
        '''
        return self.token

    def get_stored_userid(self):
        '''
        return store userid
        '''
        return self.userid

    def write_credential(self, id, password):
        '''
        Wrtite the (token, userid) to the file configs/moodle
        Returns:
            True: when valid credentials given
            False: otherwise
        '''
        self.key = Key()
        self.key.write_key_to_file(PATH + 'moodle.key')
        self.token = self.get_token(id, password)

        # invalid login credentials or some other issue
        if self.token is None:
            return False

        self.userid = self.get_userid(self.token)
        
        if self.userid is None:
            return False

        txt = f"token={self.token},userid={self.userid}"
        try:
            self.key.encrypt_and_write_to_file(txt, PATH + 'moodle')
        except Exception as er:
            return False

        return True

    def get_token(self, id, password):
        '''
        find the token 
        '''
        payload = {'username': id,'password': password,'service': 'moodle_mobile_app'}
        try:
            res = requests.post('https://moodle.iitb.ac.in/login/token.php', payload)
            if res.status_code == 200:
                token = json.loads(res.text)['token']
                return token 
            else:
                return None
        except Exception as err:
            # print("Error: ", err)
            if os.path.exists(PATH + 'moodle.key'):
                os.remove(PATH + 'moodle.key')

            return None

    def get_userid(self, token):
        '''
        find the userid
        '''
        payload = {'wstoken': token,'wsfunction': 'core_webservice_get_site_info'} 
        try:
            res = requests.post('https://moodle.iitb.ac.in/webservice/rest/server.php?moodlewsrestformat=json',payload)
            res = json.loads(res.content)
            if "exception" in res.keys():
                # print("Error: ", res['errorcode'])
                if os.path.exists(PATH + 'moodle.key'):
                    os.remove(PATH + 'moodle.key')

                return None
            else:
                return res['userid']
        except Exception as err:
            # print("Error: ", err)
            if os.path.exists(PATH + 'moodle.key'):
                os.remove(PATH + 'moodle.key')

            return None
