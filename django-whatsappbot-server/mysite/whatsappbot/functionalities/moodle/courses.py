import requests
import json
from tabulate import tabulate
import sys
sys.path.append("../../")
from usersapi.views import Users

class Courses:
    def show_courses(self, sender_whatsapp_no):
        '''
        Show details of all enrolled courses
        '''
        token, userid = Users(sender_whatsapp_no).getMoodle()
        if token == -1:
            return "Please register moodle credentials"

        print("userid:", token, userid)
        if token is None:
            return "Please update Moodle Credentials"

        url = 'https://moodle.iitb.ac.in/webservice/rest/server.php?moodlewsrestformat=json'

        payload = {'wstoken': token,'wsfunction': 'core_enrol_get_users_courses','userid': userid}
        res = requests.post(url, data=payload)
        table = list()
        i = 1
        for x in json.loads(res.text):
            table.append([i, x['id'], x['progress'], x['shortname'], x['fullname']])
            i += 1

        return (tabulate(table, headers = ['sl No', 'Course id', 'Progress', 'Short Name', 'Full Name']))

