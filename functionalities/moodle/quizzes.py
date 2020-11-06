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

class Quizzes:
    def show_quizzes(self, course_id):
        token, userid = utils.get_credential()
        payload = {'wstoken': token, 'wsfunction': 'mod_quiz_get_quizzes_by_courses', 'courseids[0]': course_id}
        
        res = requests.post('https://moodle.iitb.ac.in/webservice/rest/server.php?moodlewsrestformat=json',data=payload)
        i = 1
        table = list()
        for x in json.loads(res.text)['quizzes']:
            table.append([i, x['id'], x['name'], x['grade'], datetime.fromtimestamp(x['timeopen']), datetime.fromtimestamp(x['timeclose'])])
            i += 1
        
        print(tabulate(table, headers = ['sl No', 'id', 'Name', 'Total Score', 'Quiz Opens', 'Quiz Closes']))

    def show_all_quizzes(self):
        token, userid = utils.get_credential()
        payload = {'wstoken': token, 'wsfunction': 'mod_quiz_get_quizzes_by_courses'}
        
        res = requests.post('https://moodle.iitb.ac.in/webservice/rest/server.php?moodlewsrestformat=json',data=payload)
        i = 1
        table = list()
        
        for x in json.loads(res.text)['quizzes']:
            table.append([i, x['course'], x['id'], x['name'], x['grade'], datetime.fromtimestamp(x['timeopen']), datetime.fromtimestamp(x['timeclose'])])
            i += 1
            
        print(tabulate(table, headers = ['sl No', 'Course id', 'id', 'Name', 'Total Score', 'Quiz Opens', 'Quiz Closes']))
    
# c = Quizzes()
# x = input("Enter course id: ")
# c.show_quizzes(x)
# c.show_all_quizzes()