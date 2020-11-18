import requests
import json
from tabulate import tabulate
import sys
sys.path.append("../../")

from usersapi.views import Users

class discussion_forums:
    def show_course_discussion_forums(self, course_id, sender_whatsapp_no, n = None):
        '''
        Show all discussion forums of a particular course
        Input:
            course_id (int) : ID of the course
            n (int) : show only top `n` discussion forums
        '''
        token, userid = Users(sender_whatsapp_no).getMoodle()
        if token == -1:
            return "Please register moodle credentials"

        print("userid:", token, userid)
        if token is None:
            return "Please update Moodle Credentials"

        try:
            payload = {'wstoken': token,'wsfunction':'mod_forum_get_forums_by_courses','courseids[0]': course_id}
            res = requests.post('https://moodle.iitb.ac.in/webservice/rest/server.php?moodlewsrestformat=json',data=payload)
            table = []
            i = 1
            for x in json.loads(res.text):
                if n is not None and int(n) < i:
                    break

                table.append([x['id'], x['name']])
                i += 1

            return (tabulate(table, headers = ["Forum ID", "Forum Name"]))
        except:
            pass

