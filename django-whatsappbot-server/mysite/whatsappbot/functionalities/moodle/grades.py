import requests
import json
from tabulate import tabulate
import sys
sys.path.append("../../")
from usersapi.views import Users

class Grades:
    def show_grades(self, sender_whatsapp_no, course_id):
        '''
        Show grades of a course
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
            payload = {'wstoken': token,'wsfunction': 'gradereport_user_get_grade_items', 'courseid': course_id, 'userid': userid}
            res = requests.post('https://moodle.iitb.ac.in/webservice/rest/server.php?moodlewsrestformat=json', data=payload)
            table = list()

            for x in json.loads(res.text)['usergrades']:
                i = 1
                for grades in x['gradeitems']:
                    table.append([i, grades['graderaw'], grades['grademax'], grades['percentageformatted']])
                    i += 1
                break

            return (tabulate(table, headers = ['sl No', 'Grade','Max', 'Percentage']))
        except:
            pass
