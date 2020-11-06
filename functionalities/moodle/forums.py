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

class discussion_forums:
    def show_course_discussion_forums(self, course_id, n = None):
        token, userid = utils.get_credential()
        payload = {'wstoken': token,'wsfunction':'mod_forum_get_forums_by_courses','courseids[0]': course_id}
        res = requests.post('https://moodle.iitb.ac.in/webservice/rest/server.php?moodlewsrestformat=json',data=payload)
        # print(res)
        table = []
        i = 1
        for x in json.loads(res.text):
            if n is not None and int(n) < i:
                break

            table.append([x['id'], x['name']])
            i += 1
        
        print(tabulate(table, headers = ["Forum ID", "Forum Name"]))

# c = discussion_forums()
# x = input("Enter course id: ")
# c.show_course_discussion_forums(x, 5)