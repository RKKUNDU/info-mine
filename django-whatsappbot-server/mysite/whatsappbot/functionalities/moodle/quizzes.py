import requests
import json
from tabulate import tabulate
from datetime import datetime
import sys
sys.path.append("../../")
from usersapi.views import Users

class Quizzes:
    def show_quizzes(self, sender_whatsapp_no, course_id):
        '''
        Show quizzes of a course
        Input:
            course_id (int) : ID of the course
        '''
        token, userid = Users(sender_whatsapp_no).getMoodle()
        if token == -1:
            return "Please register moodle credentials"

        print("userid:", token, userid)
        if token is None:
            return "Please update Moodle Credentials"

        try:
            payload = {'wstoken': token, 'wsfunction': 'mod_quiz_get_quizzes_by_courses', 'courseids[0]': course_id}

            res = requests.post('https://moodle.iitb.ac.in/webservice/rest/server.php?moodlewsrestformat=json',data=payload)
            i = 1
            table = list()
            for x in json.loads(res.text)['quizzes']:
                table.append([i, x['id'], x['name'], x['grade'], datetime.fromtimestamp(x['timeopen']), datetime.fromtimestamp(x['timeclose'])])
                table.append([])
                i += 1

            return (tabulate(table, headers = ['sl No', 'id', 'Name', 'Total Score', 'Quiz Opens', 'Quiz Closes']))
        except:
            pass

    def show_all_quizzes(self, sender_whatsapp_no):
        '''
        Show quizzes of all courses
        '''
        token, userid = Users(sender_whatsapp_no).getMoodle()
        if token == -1:
            return "Please register moodle credentials"

        print("userid:", token, userid)
        if token is None:
            return "Please update Moodle Credentials"

        try:
            payload = {'wstoken': token, 'wsfunction': 'mod_quiz_get_quizzes_by_courses'}

            res = requests.post('https://moodle.iitb.ac.in/webservice/rest/server.php?moodlewsrestformat=json',data=payload)
            i = 1
            table = list()

            for x in json.loads(res.text)['quizzes']:
                table.append([i, x['course'], x['id'], x['name'], x['grade'], datetime.fromtimestamp(x['timeopen']), datetime.fromtimestamp(x['timeclose'])])
                table.append([])
                i += 1

            return (tabulate(table, headers = ['sl No', 'Course id', 'id', 'Name', 'Total Score', 'Quiz Opens', 'Quiz Closes']))
        except:
            pass
