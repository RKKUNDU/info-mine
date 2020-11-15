from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint
import json
from tabulate import tabulate
url = "https://www.cse.iitb.ac.in/~internal-live/api/courses/all_courses/?format=json"

class Courses:
    def show_courses(self, in_autumn = True, in_spring = True):
        '''
        This function will fetch all the courses from CSE website and show them
        Input:
            in_autumn (boolean) : whether the course is offered in autumn semester
            in_spring (boolean) : whether the course is offered in spring semester
        Following things are shown for each course:
        ['Semester', 'Course Code', 'Course Name', 'Instructor Name']
        '''
        try:
            res = requests.get(url)
            table = []
            for x in json.loads(res.text):
                if x['autumncourse'] and in_autumn:
                    table.append(["Autumn", x['crsecode'], x['crsename'], x['autumninstructor']])

                if x['springcourse'] and in_spring:
                    table.append(["Spring", x['crsecode'], x['crsename'], x['springinstructor']])

        except Exception as err:
            print(f"Error: {err}")
        finally:
            print(tabulate(table, headers = ['Semester', 'Course Code', 'Course Name', 'Instructor Name']))

    def show_filtered_courses(self, filter, with_details = False, with_description = False, with_prereqs = False, with_textrefs = False, in_autumn = True, in_spring = True):
        '''
        This function will fetch all the courses from CSE website and show only the filtered courses
        case-insensitive filtering is done based on course code (space does not matter), course name, instructor name
        Input:
            filter (string): filter the courses
            with_details (boolean): print course(s) with additional information (discussed later)
            with_description (boolean): also print the description of the course(s) with other information
            with_prereqs (boolean):  also print the Pre-Requisites of the course(s) with other information
            with_textrefs (boolean):  also print the text references of the course(s) with other information
            in_autumn (boolean) : whether the course is offered in autumn semester
            in_spring (boolean) : whether the course is offered in spring semester
            
        with_details = True: Following things are shown for each courses
            ["Course Name", "Course Code", "Course Instructor", "Semester", "Total Credit", "Course Type", "Offered", "Courese Duration", "Homepage"]

        with_details = False:  Following things are shown for each courses
            ['Semester', 'Course Code', 'Course Name', 'Instructor Name']

        Output:
            Print in the mentioned format or print "No courses found with this filter. Please try with some other filter" if there is no courses found
        '''
        filter = filter.lower()
        cnt = 0
        try:
            res = requests.get(url)
            table = []
            for x in json.loads(res.text):
                # filter is not matched, then go to the next course
                if not (filter in x['crsecode'].lower() 
                        or filter in x['crsecode'].lower().replace(' ', '') 
                        or filter in x['crsename'].lower() 
                        or (x['autumncourse'] and filter in x['autumninstructor'].lower())
                        or (x['springcourse'] and filter in x['springinstructor'].lower())):
                        continue

                # if offered in autumn semester
                if x['autumncourse'] and in_autumn:
                    if with_details or with_description or with_prereqs or with_textrefs:
                        course_table = []
                        course_table.append(["Course Name", x['crsename']])
                        course_table.append(["Course Code", x['crsecode']])
                        course_table.append(["Course Instructor", x['autumninstructor']])
                        course_table.append(["Semester", "Autumn"])

                    if with_details:
                        course_table.append(["Total Credit", x['totcred']])
                        course_table.append(["Course Type", x['crsetype']])
                        course_table.append(["Offered", x['offered']])
                        course_table.append(["Courese Duration", x['crseduration']])
                        course_table.append(["Homepage", x['homepage']])

                    if with_description:
                        course_table.append(["Description", bs(x['description'], 'html.parser').get_text()])
                    
                    if with_prereqs:
                        course_table.append(["Pre-Requisites", bs(x['prereq'], 'html.parser').get_text()])
                    
                    if with_textrefs:
                        course_table.append(["References", bs(x['textref'], 'html.parser').get_text()])

                    if with_details or with_description or with_prereqs or with_textrefs:
                        print(tabulate(course_table))
                        cnt += 1
                    else:
                        table.append(["Autumn", x['crsecode'], x['crsename'], x['autumninstructor']])

                # if offered in spring semester
                if x['springcourse'] and in_spring:
                    if with_details or with_description or with_prereqs or with_textrefs:
                        course_table = []
                        course_table.append(["Course Name", x['crsename']])
                        course_table.append(["Course Code", x['crsecode']])
                        course_table.append(["Course Instructor", x['springinstructor']])
                        course_table.append(["Semester", "Spring"])
                        
                    if with_details:
                        course_table.append(["Total Credit", x['totcred']])
                        course_table.append(["Course Type", x['crsetype']])
                        course_table.append(["Offered", x['offered']])
                        course_table.append(["Courese Duration", x['crseduration']])
                        course_table.append(["Homepage", x['homepage']])

                    if with_description:
                        course_table.append(["Description", bs(x['description'], 'html.parser').get_text()])
                    
                    if with_prereqs:
                        course_table.append(["Pre-Requisites", bs(x['prereq'], 'html.parser').get_text()])
                    
                    if with_textrefs:
                        course_table.append(["References", bs(x['textref'], 'html.parser').get_text()])

                    if with_details or with_description or with_prereqs or with_textrefs:
                        print(tabulate(course_table))
                        cnt += 1
                    else:
                        table.append(["Spring", x['crsecode'], x['crsename'], x['springinstructor']])

        except Exception as err:
            print(f"Error: {err}")
        finally:
            if len(table) > 0:
                print(tabulate(table, headers = ['Semester', 'Course Code', 'Course Name', 'Instructor Name']))
            elif not (with_details or with_description or with_prereqs or with_textrefs) or cnt == 0:
                print("No courses found with this filter. Please try with some other filter")

