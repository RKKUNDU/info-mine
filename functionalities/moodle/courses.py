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

class Courses:
    def show_courses(self):
        url = 'https://moodle.iitb.ac.in/webservice/rest/server.php?moodlewsrestformat=json'
        
        token, userid = utils.get_credential()

        payload = {'wstoken': token,'wsfunction': 'core_enrol_get_users_courses','userid': userid}
        res = requests.post(url, data=payload)
        table = list()
        i = 1
        for x in json.loads(res.text):
            table.append([i, x['id'], x['progress'], x['shortname'], x['fullname']])
            i += 1
        
        print(tabulate(table, headers = ['sl No', 'Course id', 'Progress', 'Short Name', 'Full Name']))

# c = Courses()
# c.show_courses()