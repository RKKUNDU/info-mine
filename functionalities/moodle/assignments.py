import requests
from bs4 import BeautifulSoup as bs
from pprint import pprint
import json
from tabulate import tabulate
from datetime import datetime 
import sys
import time
sys.path.append("../../")

from utility import utils
from security.keys import Key
from security.moodle_credentials import moodle_credential

class Assignments:
    def show_assignments(self, course, show_only_due):
        '''
        Show assignments of a course
        Input:
            course (string) : filter for course name
            show_only_due (boolean) : when set to True, shows only due assignments
        '''
        course = course.lower()
        token, userid = utils.get_credential()
        payload = {'wstoken': token,'wsfunction': 'mod_assign_get_assignments'}
        
        res = requests.post('https://moodle.iitb.ac.in/webservice/rest/server.php?moodlewsrestformat=json',data=payload)
        
        table = list()
        
        for x in json.loads(res.text)['courses']:
            i = 1
            if course in x['shortname' ].lower() or course in x['fullname'].lower():
                for assignment in x['assignments']:
                    # assignment is not due
                    if show_only_due and datetime.fromtimestamp(assignment['duedate']) < datetime.fromtimestamp(time.time()):
                        continue

                    table.append([i, x['shortname'], assignment['name'], datetime.fromtimestamp(assignment['duedate'])])
                    i += 1
                table.append([])
                break
            
        print(tabulate(table, headers = ['sl No', 'Course Name','Assignment', 'Due Date']))

    def show_all_assignments(self):
        '''
        Show assignments of all courses
        '''
        token, userid = utils.get_credential()
        payload = {'wstoken': token,'wsfunction':'mod_assign_get_assignments'}
        res = requests.post('https://moodle.iitb.ac.in/webservice/rest/server.php?moodlewsrestformat=json',data=payload)
        
        table = list()
        
        for x in json.loads(res.text)['courses']:
            i = 1
            for assignment in x['assignments']:
                table.append([i, x['shortname'], assignment['name'], datetime.fromtimestamp(assignment['duedate'])])
                i += 1

            table.append([])
            
        print(tabulate(table, headers = ['sl No', 'Course Name','Assignment', 'Due Date']))

    def show_all_due_assignments(self):
        '''
        Show due assignments of all courses
        '''
        token, userid = utils.get_credential()
        payload = {'wstoken': token,'wsfunction': 'mod_assign_get_assignments'}
        res = requests.post('https://moodle.iitb.ac.in/webservice/rest/server.php?moodlewsrestformat=json',data=payload)
        
        table = list()
        
        for x in json.loads(res.text)['courses']:
            i = 1
            cnt = 0
            for assignment in x['assignments']:
                # assignment is not due
                if datetime.fromtimestamp(assignment['duedate']) < datetime.fromtimestamp(time.time()):
                    continue

                table.append([i, x['shortname'], assignment['name'], datetime.fromtimestamp(assignment['duedate'])])
                i += 1
                cnt += 1

            if cnt > 0:    
                table.append([])
            
        print(tabulate(table, headers = ['sl No', 'Course Name','Assignment', 'Due Date']))

