import argparse
import sys
import datetime

from functionalities.CSE.courses import Courses
from functionalities.CSE.faculties import Faculties
from functionalities.CSE.news import News
from functionalities.CSE.students import Students

from functionalities.moodle.announcements import Announcements
from functionalities.moodle.assignments import Assignments
from functionalities.moodle.courses import Courses as moodle_courses
from functionalities.moodle.discussions import Discussions
from functionalities.moodle.forums import discussion_forums
from functionalities.moodle.grades import Grades
from functionalities.moodle.quizzes import Quizzes


# top-level parser
parser = argparse.ArgumentParser()


# 2nd-level parser
subparsers = parser.add_subparsers(dest='portal', help='portals help')

# create the parser for the "moodle" sub-command
moodle_parser = subparsers.add_parser('moodle', help='Commands for Moodle portal')

# create the parser for the "cse" sub-command
cse_parser = subparsers.add_parser('cse', help='Commands for CSE website')

# create the parser for the "mail" sub-command
mail_parser = subparsers.add_parser('mail', help='Commands for institute email service')

# create the parser for the "dmail" sub-command
dmail_parser = subparsers.add_parser('dmail', help='Commands for department email service')


# ------------------------------------------------------ CSE --------------------------------------------------------------

# create sub-parser for 'cse' command
cse_subparsers = cse_parser.add_subparsers(dest='cse_command', help='CSE commands help')

# create the sub-parser for the "courses" command
courses_parser = cse_subparsers.add_parser('courses', help='Info about courses')

# create the parser for the "students" command
students_parser = cse_subparsers.add_parser('students', help='Info about students')

# create the parser for the "faculties" command
faculties_parser = cse_subparsers.add_parser('faculties', help='Info about faculties')

# create the parser for the "news" command
news_parser = cse_subparsers.add_parser('news', help='Get news')


# arguments for 'courses' sub-command
courses_parser.add_argument('-a', '--autumn', action='store_true', help="Show courses from Autumn semester")
courses_parser.add_argument('-s', '--spring', action='store_true', help="Show courses from Spring semester")
courses_parser.add_argument('-d', '--details', action='store_true', help="Show courses with details")
courses_parser.add_argument('-D', '--description', action='store_true', help="Show description of courses")
courses_parser.add_argument('-p', '--prereqs', action='store_true', help="Show pre-requisites of courses")
courses_parser.add_argument('-t', '--textrefs', action='store_true', help="Show text references of courses")
courses_parser.add_argument('-f', '--filter', action='store', help='Filter courses based on course name or course id or instructor name', default='')


# arguments for 'students' sub-command
# mandatory option -> batch
students_parser.add_argument('-b', '--batch', type=str, help='Give batch name (eg. phd, mtech1, btech3)', required=True)
students_parser.add_argument('-i', '--interest', action='store_true', help='Show student\'s interests')
students_parser.add_argument('-a', '--advisor', action='store_true', help='Show student\'s advisor name')
students_parser.add_argument('-f', '--filter', action='store', help='filter students based on name')
students_parser.add_argument('-A', '--Advisor', action='store', help='filter students based on advisor name')
students_parser.add_argument('-I', '--Interest', action='store', help='filter students based on interest')


# arguments for 'faculties' sub-command
faculties_parser.add_argument('-i', '--interest', action='store_true', help='Show faculty\'s interests')
faculties_parser.add_argument('-w', '--website', action='store_true', help='Show faculty\'s website')
faculties_parser.add_argument('-e', '--extension', action='store_true', help='Show faculty\'s extension')
faculties_parser.add_argument('-r', '--room', action='store_true', help='Show faculty\'s room details')
faculties_parser.add_argument('-F', '--filter', action='store', help='filter faculties based on name')
faculties_parser.add_argument('-I', '--Interest', action='store', help='filter faculties based on interest')


# arguments for 'news' sub-command
group = news_parser.add_mutually_exclusive_group()
news_parser.add_argument('-d', '--details', action='store_true', help='Show detailed news')
group.add_argument('-t', '--timeline', action='store', help='Show news in a timeline (DDMMYYYY DDMMYYYY)', nargs=2)    
group.add_argument('-y', '--year', action='store', help='Show news of a year')    


# ---------------------------------------------------- Moodle ------------------------------------------------------------

# create sub-parser for 'moodle' command
moodle_subparsers = moodle_parser.add_subparsers(dest='moodle_command', help='Moodle commands help')

# create the sub-parser for the "quiz" command
quizzes_parser = moodle_subparsers.add_parser('quizzes', help='Info about quizzes')

# create the parser for the "grades" command
grades_parser = moodle_subparsers.add_parser('grades', help='Info about grades')

# create the parser for the "forums" command
forums_parser = moodle_subparsers.add_parser('forums', help='Info about discussion forums')

# create the parser for the "discussions" command
discussions_parser = moodle_subparsers.add_parser('discussions', help='Info about discussions')

# create the parser for the "courses" command
courses_parser = moodle_subparsers.add_parser('courses', help='Info about courses')

# create the parser for the "discussions" command
announcements_parser = moodle_subparsers.add_parser('announcements', help='Info about announcements')

# create the parser for the "discussions" command
assignments_parser = moodle_subparsers.add_parser('assignments', help='Info about assignments')


quizzes_parser.add_argument('-c', '--cid', type=int, action='store', help='Show quizzes of given course')

grades_parser.add_argument('-c', '--cid', type=int, required = True, action='store', help='Show grades of given course')

forums_parser.add_argument('-c', '--cid', type=int, required = True, action='store', help='Show forums of given course')
forums_parser.add_argument('-n', '--number', type=int, default=None, action='store', help='Show only top n discussion forums')

discussions_parser.add_argument('-f', '--forum-id', type=int, required = True, action='store', help='Show discussions of given forum')
discussions_parser.add_argument('-n', '--number', type=int, default=None, action='store', help='Show only top n discussions')

announcements_parser.add_argument('-c', '--cid', type=int, required = True, action='store', help='Show announcements of given course')
announcements_parser.add_argument('-n', '--number', type=int, default=None, action='store', help='Show only top n announcements')

assignments_parser.add_argument('-d', '--due', action='store_true', help='Show only due assignments')
assignments_parser.add_argument('-c', '--course', action='store', help='Filter for course name')



args = parser.parse_args()

# cse command is used
if args.portal == 'cse':
    if args.cse_command == 'courses':
        c = Courses()

        # when any of autumn or spring is set, show courses in that semester only
        if args.autumn or args.spring:
            c.show_filtered_courses(args.filter, with_details = args.details, with_description = args.description,
                                with_prereqs = args.prereqs, with_textrefs = args.textrefs,
                                in_autumn = args.autumn, in_spring = args.spring)
        # when semester not given, show courses of both semester
        else:
            c.show_filtered_courses(args.filter, with_details = args.details, with_description = args.description,
                                with_prereqs = args.prereqs, with_textrefs = args.textrefs)

    elif args.cse_command == 'students':
        s = Students()
        # filter based on name
        if args.filter is not None:
            s.show_filtered_students(args.batch, name_filter = args.filter, filters_name = True, 
                                    with_advisor = args.advisor, with_interests = args.interest)
        # filter based on advisor name
        elif args.Advisor is not None:
            s.show_filtered_students(args.batch, advisor_filter = args.Advisor, filters_advisor = True, 
                                    with_advisor = args.advisor, with_interests = args.interest)
        # filter based on interest
        elif args.Interest is not None:
            s.show_filtered_students(args.batch, interests_filter = args.Interest, filters_interests = True, 
                                    with_advisor = args.advisor, with_interests = args.interest)
        else:
            s.show_students(args.batch, with_interests = args.interest, with_advisor = args.advisor)

    elif args.cse_command == 'faculties':

        f = Faculties()

        if args.filter is not None:
            f.show_filtered_faculties(name_filter = args.filter, filters_name = True, with_extension = args.extension, 
                                    with_room = args.room, with_website = args.website, with_interests = args.interest)
        elif args.Interest is not None:
            f.show_filtered_faculties(interests_filter = args.Interest, filters_interests = True, with_extension = args.extension, 
                                    with_room = args.room, with_website = args.website, with_interests = args.interest)
        else:
            f.show_faculties(with_extension = args.extension, with_room = args.room, 
                            with_website = args.website, with_interests = args.interest)

    elif args.cse_command == 'news':
        n = News()

        # show all news in the given timeline
        if args.timeline is not None:
            n.show_news_in_time_period(args.timeline[0], args.timeline[1], with_details = args.details)
        # show all news of the given year
        elif args.year is not None:
            n.show_news_in_a_year(args.year, with_details=args.details)
        # show all news of this year
        else:
            n.show_news_in_a_year(datetime.datetime.now().year, with_details=args.details)
    else:
        cse_parser.print_help()
elif args.portal == 'moodle':
    if args.moodle_command == 'quizzes':
        q = Quizzes()
        if args.cid is not None:
            q.show_quizzes(course_id = args.cid)
        else:
            q.show_all_quizzes()
    elif args.moodle_command == 'grades':
        g  = Grades()
        g.show_grades(course_id = args.cid)
    elif args.moodle_command == 'forums':
        df = discussion_forums()
        df.show_course_discussion_forums(args.cid, args.number)
    elif args.moodle_command == 'discussions':
        d = Discussions()
        d.show_discussions_from_a_forum(args.forum_id, args.number)
    elif args.moodle_command == 'courses':
        c = moodle_courses()
        c.show_courses()
    elif args.moodle_command == 'announcements':
        a = Announcements()
        a.show_course_announcements(args.cid, args.number)
    elif args.moodle_command == 'assignments':
        a = Assignments()
        if args.course is not None:
            a.show_assignments(args.course, show_only_due=args.due)
        else:
            if args.due:
                a.show_all_due_assignments()
            else:
                a.show_all_assignments()
    else:
        moodle_parser.print_help()