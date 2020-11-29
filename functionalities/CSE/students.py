import requests
import json
from tabulate import tabulate
url = "https://www.cse.iitb.ac.in/~internal-live/api/student/students_all/?batch="

class Students:
    def show_students(self, batch, with_interests = False, with_advisor = False):
        '''
        This function will fetch all the students in a particular batch from CSE website and show them
        Input:
            batch (string): batch name of the students to show (eg. MTech1, BTech1)
            with_interests (boolean): whether to show 'interests' of the students in addition to other information
            with_advisor (boolean): whether to show 'advisor' of the students in addition to other information

        Following things are shown for each student normally:
            ['User ID', 'Name']
        '''
        try:
            global url
            url = url + batch
            res = requests.get(url)
            table = []
            for x in json.loads(res.text):
                name = ""
                if x['firstname'] != "None":
                    name += x['firstname']
                    name += " "
                
                if x['lastname'] != "None":
                    name += x['lastname']

                if with_advisor and with_interests:
                    table.append([x['userid'], name, x['advisor'], x['interests']])
                elif with_interests:
                    table.append([x['userid'], name, x['interests']])
                elif with_advisor:
                    table.append([x['userid'], name, x['advisor']])
                else:
                    table.append([x['userid'], name])

        except Exception as err:
            pass
        else:
            if with_advisor and with_interests:
                print(tabulate(table, headers = ['User ID', 'Name', 'Advisor', 'Interests']))
            elif with_advisor:
                print(tabulate(table, headers = ['User ID', 'Name', 'Advisor']))
            elif with_interests:
                print(tabulate(table, headers = ['User ID', 'Name', 'Interests']))
            else:
                print(tabulate(table, headers = ['User ID', 'Name']))

    def show_filtered_students(self, batch, 
                                name_filter = None, interests_filter = None, advisor_filter = None, 
                                filters_name = False, filters_interests = False, 
                                filters_advisor = False, with_advisor = False, with_interests = False):
        '''
        This function will fetch all the students in a particular batch from CSE website and show filtered students
        Input:
            batch (string): batch name of the students to show (eg. MTech1, BTech1)
            filters_name (boolean): whether filters based on name or userid
            name_filter (string): filter for name 
            filters_interests (boolean): whether filters based on 'interests'
            interests_filter (string): filter for 'interests' 
            filters_advisor (boolean): whether filters based on advisor
            advisor_filter (string): filter for 'advisor name' 
            with_interests (boolean): whether to show 'interests' of the students in addition to other information
            with_advisor (boolean): whether to show 'advisor' of the students in addition to other information

        Following things are shown for each student normally:
            ['User ID', 'Name']
        Output:
            Print in the mentioned format or print "No student found with this filter. Please try with some other filter" if there is no student found
        '''
        # nothing to filter
        if not (filters_name or filters_advisor or filters_interests):
            return

        # if filtering based on advisor, also show the advisor name
        if filters_advisor:
            with_advisor = True
        
        # if filtering based on interesrs, also show the interests
        if filters_interests:
            with_interests = True

        if name_filter is not None:
            name_filter = name_filter.lower()
        
        if advisor_filter is not None:
            advisor_filter = advisor_filter.lower()
        
        if interests_filter is not None: 
            interests_filter = interests_filter.lower()

        global url
        url = url + batch
        cnt = 0
        try:
            res = requests.get(url)
            table = []
            for x in json.loads(res.text):
                # filter is not matched, then go to the next student
                if not ((filters_name and name_filter in x['firstname'].lower()) 
                        or (filters_name and x['lastname'] != "None" and name_filter in x['lastname'].lower())
                        or (filters_name and name_filter in x['userid'].lower())
                        or (filters_advisor and x['advisor'] is not None and  advisor_filter in x['advisor'].lower()) 
                        or (filters_interests and x['interests'] is not None and interests_filter in x['interests'].lower())):
                    continue

                name = ""
                if x['firstname'] != "None":
                    name += x['firstname']
                    name += " "
                
                if x['lastname'] != "None":
                    name += x['lastname']

                if with_advisor and with_interests:
                    table.append([x['userid'], name, x['advisor'], x['interests']])
                elif with_interests:
                    table.append([x['userid'], name, x['interests']])
                elif with_advisor:
                    table.append([x['userid'], name, x['advisor']])
                else:
                    table.append([x['userid'], name])

                cnt += 1
                
        except Exception as err:
            pass
        else:
            if with_advisor and with_interests and cnt > 0:
                print(tabulate(table, headers = ['User ID', 'Name', 'Advisor', 'Interests']))
            elif with_advisor and cnt > 0:
                print(tabulate(table, headers = ['User ID', 'Name', 'Advisor']))
            elif with_interests and cnt > 0:
                print(tabulate(table, headers = ['User ID', 'Name', 'Interests']))
            elif cnt > 0:
                print(tabulate(table, headers = ['User ID', 'Name']))
            else:
                print("No student found with this filter. Please try with some other filter")
                