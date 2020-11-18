import requests
import json
from tabulate import tabulate
url = "https://www.cse.iitb.ac.in/~internal-live/api/faculty/?format=json"

class Faculties:
    def show_faculties(self, with_interests = False, with_website = False, with_extension = False, with_room = False):
        '''
        This function will fetch all the faculties from CSE website and show them
        Input:
            with_interests (boolean): whether to show 'interests' of the faculties in addition to other information
            with_website (boolean): whether to show website of the faculties in addition to other information
            with_extension (boolean): whether to show extensions of the faculties in addition to other information
            with_room (boolean): whether to show room detail of the faculties in addition to other information

        Following things are shown for each faculty normally:
            ['User ID', 'Name']
        '''
        try:
            res = requests.get(url)
            table = []
            for x in json.loads(res.text):
                name = ""
                if x['firstname'] != "None":
                    name += x['firstname']
                    name += " "

                if x['lastname'] != "None":
                    name += x['lastname']

                # don't show strings like 'NULL' or 'na' or '-'
                extn_residence = '' if x['extn_residence'] == 'NULL' or x['extn_residence'] == 'na' or x['extn_residence'] == '-'  else x['extn_residence']
                extn = '' if x['extn'] == 'NULL' or x['extn'] == 'na' or x['extn'] == '-'  else x['extn']
                website = '' if x['website'] == 'NULL' or x['website'] == 'na' or x['website'] == '-'  else x['website']

                faculty = [x['userid'], name]
                if with_extension:
                    faculty.append(extn)
                    faculty.append(extn_residence)

                if with_room:
                    faculty.append(x['room'])

                if with_website:
                    faculty.append(website)

                if with_interests:
                    faculty.append(x['interests'])

                table.append(faculty)

        except Exception as err:
            return (f"Error: {err}")
        finally:
            header = ['User ID', 'Name']
            if with_extension:
                header.append('Extension')
                header.append('Residence Extension')

            if with_room:
                header.append('Room')

            if with_website:
                header.append('Website')

            if with_interests:
                header.append('Interests')

            return (tabulate(table, headers = header))

    def show_filtered_faculties(self, name_filter = None, interests_filter = None,
                                filters_name = False, filters_interests = False,
                                with_extension = False, with_room = False, with_website = False, with_interests = False):
        '''
        This function will fetch all the faculties from CSE website and show filtered faculties
        Input:
            batch (string): batch name of the students to show (eg. MTech1, BTech1)
            filters_name (boolean): whether filters based on name or userid
            name_filter (string): filter for name
            filters_interests (boolean): whether filters based on 'interests'
            interests_filter (string): filter for 'interests'
            with_interests (boolean): whether to show 'interests' of the faculties in addition to other information
            with_website (boolean): whether to show website of the faculties in addition to other information
            with_extension (boolean): whether to show extensions of the faculties in addition to other information
            with_room (boolean): whether to show room detail of the faculties in addition to other information

        Following things are shown for each faculy normally:
            ['User ID', 'Name']
        Output:
            Print in the mentioned format or print "No faculty found with this filter. Please try with some other filter" if there is no faculty found
        '''
        # nothing to filter
        if not (filters_name or filters_interests):
            return

        # if filtering based on interesrs, also show the interests
        if filters_interests:
            with_interests = True

        if name_filter is not None:
            name_filter = name_filter.lower()

        if interests_filter is not None:
            interests_filter = interests_filter.lower()

        cnt = 0
        try:
            res = requests.get(url)
            table = []
            for x in json.loads(res.text):
                # filter is not matched, then go to the next student
                if not ((filters_name and name_filter in x['firstname'].lower())
                        or (filters_name and name_filter in x['lastname'].lower())
                        or (filters_name and name_filter in x['userid'].lower())
                        or (filters_interests and x['interests'] is not None and interests_filter in x['interests'].lower())):
                    continue

                name = ""
                if x['firstname'] != "None":
                    name += x['firstname']
                    name += " "

                if x['lastname'] != "None":
                    name += x['lastname']

                # don't show strings like 'NULL' or 'na' or '-'
                extn_residence = '' if x['extn_residence'] == 'NULL' or x['extn_residence'] == 'na' or x['extn_residence'] == '-'  else x['extn_residence']
                extn = '' if x['extn'] == 'NULL' or x['extn'] == 'na' or x['extn'] == '-'  else x['extn']
                website = '' if x['website'] == 'NULL' or x['website'] == 'na' or x['website'] == '-'  else x['website']

                faculty = [x['userid'], name]
                if with_extension:
                    faculty.append(extn)
                    faculty.append(extn_residence)

                if with_room:
                    faculty.append(x['room'])

                if with_website:
                    faculty.append(website)

                if with_interests:
                    faculty.append(x['interests'])

                table.append(faculty)
                cnt += 1

        except Exception as err:
            return (f"Error: {err}")
        finally:
            header = ['User ID', 'Name']
            if with_extension:
                header.append('Extension')
                header.append('Residence Extension')

            if with_room:
                header.append('Room')

            if with_website:
                header.append('Website')

            if with_interests:
                header.append('Interests')

            if cnt > 0:
                return (tabulate(table, headers = header))
            else:
                return ("No faculty found with this filter. Please try with some other filter")
