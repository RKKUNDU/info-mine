from security.keys import Key
import requests
from bs4 import BeautifulSoup as bs
import json
PATH = '../../configs/' # set the path wrt to the calling function
class moodle_credential:
    def __init__(self):
        self.key = Key()
        try:
            self.key.read_key_from_file(PATH + "moodle.key")
        except Exception as ex:
            print("Error: ", ex)
            #TODO: Handle exceptions

        self.token = None
        self.userid = None
        if self.key.key == "":
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
            print("Error: ", err)

    def get_stored_token(self):
        return self.token

    def get_stored_userid(self):
        return self.userid

    def write_credential(self, id, password):
        self.key.write_key_to_file(PATH + 'moodle.key')
        self.token = self.get_token(id, password)

        # invalid login credentials or some other issue
        if self.token is None:
            return None

        self.userid = self.get_userid(self.token)
        
        if self.userid is None:
            return None

        txt = f"token={self.token},userid={self.userid}"
        self.key.encrypt_and_write_to_file(txt, PATH + 'moodle')

    def get_token(self, id, password):
        payload = {'username': id,'password': password,'service': 'moodle_mobile_app'}
        try:
            res = requests.post('https://moodle.iitb.ac.in/login/token.php', payload)
            if res.status_code == 200:
                token = json.loads(res.text)['token']
                return token 
            else:
                return None
        except Exception as err:
            print("Error: ", err)
            return None

    def get_userid(self, token):
        payload = {'wstoken': token,'wsfunction': 'core_webservice_get_site_info'} 
        try:
            res = requests.post('https://moodle.iitb.ac.in/webservice/rest/server.php?moodlewsrestformat=json',payload)
            res = json.loads(res.content)
            if "exception" in res.keys():
                print("Error: ", res['errorcode'])
                return None
            else:
                return res['userid']
        except Exception as err:
            print("Error: ", err)
            return None
