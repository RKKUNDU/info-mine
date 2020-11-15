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

class Grades:
    def show_grades(self, course_id):
        token, userid = utils.get_credential()
        payload = {'wstoken': token,'wsfunction': 'gradereport_user_get_grade_items', 'courseid': course_id, 'userid': userid}
        res = requests.post('https://moodle.iitb.ac.in/webservice/rest/server.php?moodlewsrestformat=json', data=payload)
        table = list()
        
        for x in json.loads(res.text)['usergrades']:
            i = 1
            for grades in x['gradeitems']:
                table.append([i, grades['graderaw'], grades['grademax'], grades['percentageformatted']])
                i += 1
            break
        
        print(tabulate(table, headers = ['sl No', 'Grade','Max', 'Percentage']))
    
