import requests
from bs4 import BeautifulSoup as bs
from pprint import pprint
import json
from tabulate import tabulate
from datetime import datetime 
import sys
sys.path.append("../../")

from utility import utils
from security.keys import Key
from security.moodle_credentials import moodle_credential

class Discussions:
    def show_discussions_from_a_forum(self, forum_id, n = None):
        '''
        Show all discussions of a particular discussion forum
        Input:
            forum_id (int) : ID of the discussion forum
            n (int) : show only top `n` discussions
        '''
        token, userid = utils.get_credential()
        payload = {'wstoken': token,'wsfunction':'mod_forum_get_forum_discussions', 'forumid': forum_id}
        res = requests.post('https://moodle.iitb.ac.in/webservice/rest/server.php?moodlewsrestformat=json', data=payload)
        print('Discussions:')
        i = 1
        for x in json.loads(res.text)['discussions']:
            if n is not None and int(n) < i:
                break

            print("\t",f"{i}.", datetime.fromtimestamp(x['created']), x['name'])
            print('{}'.format(bs(x['message'],'html.parser').get_text()),end='\n\n')
            i += 1    

