import requests
from bs4 import BeautifulSoup as bs
import json
from datetime import datetime
import sys
sys.path.append("../../")

from usersapi.views import Users

class Discussions:
    def show_discussions_from_a_forum(self, forum_id, sender_whatsapp_no, n = None):
        '''
        Show all discussions of a particular discussion forum
        Input:
            forum_id (int) : ID of the discussion forum
            n (int) : show only top `n` discussions
        '''
        token, userid = Users(sender_whatsapp_no).getMoodle()
        if token == -1:
            return "Please register moodle credentials"

        print("userid:", token, userid)
        if token is None:
            return "Please update Moodle Credentials"

        try:
            payload = {'wstoken': token,'wsfunction':'mod_forum_get_forum_discussions', 'forumid': forum_id}
            res = requests.post('https://moodle.iitb.ac.in/webservice/rest/server.php?moodlewsrestformat=json', data=payload)
            ret = 'Discussions:\n'
            i = 1

            for x in json.loads(res.text)['discussions']:
                if n is not None and int(n) < i:
                    break

                ret += "\t" + f"{i}. [" + str(datetime.fromtimestamp(x['created'])) + '], ' + x['name'] + '\n'
                ret += bs(x['message'],'html.parser').get_text() + '\n\n'
                i += 1
        except:
            pass

        return ret
