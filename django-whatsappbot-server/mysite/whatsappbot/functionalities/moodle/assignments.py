import requests
import json
from tabulate import tabulate
from datetime import datetime
import sys
import time
sys.path.append("../../")

from usersapi.views import Users

class Assignments:
    def show_assignments(self, course, sender_whatsapp_no, show_only_due):
        '''
        Show assignments of a course
        Input:
            course (string) : filter for course name
            show_only_due (boolean) : when set to True, shows only due assignments
        '''
        course = course.lower()
        token, userid = Users(sender_whatsapp_no).getMoodle()
        if token == -1:
            return "Please register moodle credentials"

        print("userid:", token, userid)
        if token is None:
            return "Please update Moodle Credentials"


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
                    table.append([])
                    i += 1

                table.append([])
                break
        if i > 1:
            return (tabulate(table, headers = ['sl No', 'Course Name','Assignment', 'Due Date']))
        else:
            return "No assignments"

    def show_all_assignments(self, sender_whatsapp_no):
        '''
        Show assignments of all courses
        '''
        token, userid = Users(sender_whatsapp_no).getMoodle()
        if token == -1:
            return "Please register moodle credentials"

        print("userid:", token, userid)
        if token is None:
            return "Please update Moodle Credentials"


        payload = {'wstoken': token,'wsfunction':'mod_assign_get_assignments'}
        res = requests.post('https://moodle.iitb.ac.in/webservice/rest/server.php?moodlewsrestformat=json',data=payload)

        table = list()

        for x in json.loads(res.text)['courses']:
            i = 1
            for assignment in x['assignments']:
                table.append([i, x['shortname'], assignment['name'], datetime.fromtimestamp(assignment['duedate'])])
                table.append([])
                i += 1

            table.append([])

        return (tabulate(table, headers = ['sl No', 'Course Name','Assignment', 'Due Date']))

    def show_all_due_assignments(self, sender_whatsapp_no):
        '''
        Show due assignments of all courses
        '''
        token, userid = Users(sender_whatsapp_no).getMoodle()
        if token == -1:
            return "Please register moodle credentials"

        print("userid:", token, userid)
        if token is None:
            return "Please update Moodle Credentials"


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
                table.append([])
                i += 1
                cnt += 1

            if cnt > 0:
                table.append([])

        return (tabulate(table, headers = ['sl No', 'Course Name','Assignment', 'Due Date']))

