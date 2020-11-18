import requests
from bs4 import BeautifulSoup as bs
import json
from datetime import datetime
import sys
sys.path.append("../../")
sys.path.append("functionalities/moodle/")
from usersapi.views import Users



class Announcements:
    def show_course_announcements(self, course_id, sender_whatsapp_no, n = None):
        '''
        Show course announcements of a particular course
        Input:
            course_id (int)
            n (int)
        '''
        token, userid = Users(sender_whatsapp_no).getMoodle()
        if token == -1:
            return "Please register moodle credentials"

        print("userid:", token, userid)
        if token is None:
            return "Please update Moodle Credentials"

        payload = {'wstoken': token,'wsfunction':'mod_forum_get_forums_by_courses','courseids[0]': course_id}

        res = requests.post('https://moodle.iitb.ac.in/webservice/rest/server.php?moodlewsrestformat=json',data=payload)

        id = None
        for x in json.loads(res.text):
            if 'announce' in x['name'].lower():
                id = x['id']
                break

        if id is None:
            return ("Course does not exist")
        else:
            payload = {'wstoken': token,'wsfunction':'mod_forum_get_forum_discussions', 'forumid': id}

            res = requests.post('https://moodle.iitb.ac.in/webservice/rest/server.php?moodlewsrestformat=json', data=payload)
            ret = 'Announcements:\n'
            i = 1
            for x in json.loads(res.text)['discussions']:
                if n is not None and int(n) < i:
                    break

                ret += "\t" f"{i}. [" + str(datetime.fromtimestamp(x['created'])) + "] " + x['name'] + '\n'
                ret +=  bs(x['message'],'html.parser').get_text() + '\n\n'
                i += 1

        return ret
