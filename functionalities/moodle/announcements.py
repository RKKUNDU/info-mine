import requests
from bs4 import BeautifulSoup as bs
from pprint import pprint
import json
from tabulate import tabulate
from datetime import datetime 
import sys
sys.path.append("../../")
sys.path.append("functionalities/moodle/")

from utility import utils
from security.keys import Key
from security.moodle_credentials import moodle_credential

class Announcements:
    def show_course_announcements(self, course_id, n = None):
        '''
        Show course announcements of a particular course
        Input:
            course_id (int)
            n (int)
        '''
        token, userid = utils.get_credential()
        payload = {'wstoken': token,'wsfunction':'mod_forum_get_forums_by_courses','courseids[0]': course_id}

        res = requests.post('https://moodle.iitb.ac.in/webservice/rest/server.php?moodlewsrestformat=json',data=payload)
        
        id = None
        for x in json.loads(res.text):
            if 'announce' in x['name'].lower():
                id = x['id']
                break
                
        if id is None:
            print("Course does not exist")
        else:
            payload = {'wstoken': token,'wsfunction':'mod_forum_get_forum_discussions', 'forumid': id}
        
            res = requests.post('https://moodle.iitb.ac.in/webservice/rest/server.php?moodlewsrestformat=json', data=payload)
            print('Announcements:')
            i = 1
            for x in json.loads(res.text)['discussions']:
                if n is not None and int(n) < i:
                    break

                print("\t",f"{i}.", datetime.fromtimestamp(x['created']), x['name'])
                print('{}'.format(bs(x['message'],'html.parser').get_text()),end='\n\n')
                i += 1    

