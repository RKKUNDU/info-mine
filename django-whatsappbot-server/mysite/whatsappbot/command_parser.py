import argparse
import datetime
import shlex

from .functionalities.CSE.courses import Courses
from .functionalities.CSE.faculties import Faculties
from .functionalities.CSE.news import News
from .functionalities.CSE.students import Students

from .functionalities.moodle.announcements import Announcements
from .functionalities.moodle.assignments import Assignments
from .functionalities.moodle.courses import Courses as moodle_courses
from .functionalities.moodle.discussions import Discussions
from .functionalities.moodle.forums import discussion_forums
from .functionalities.moodle.grades import Grades
from .functionalities.moodle.quizzes import Quizzes

from .functionalities.insti_mail.Search_topn import search_topn
from .functionalities.insti_mail.Search_from import search_from
from .functionalities.insti_mail.Search_keyword import search_keyword
from .functionalities.insti_mail.Search_sub import search_sub
from .functionalities.insti_mail.Search_date import search_date
from .functionalities.insti_mail.Send_email import send_mail

from .functionalities.dept_mail.Search_topn import search_topn as dsearch_topn
from .functionalities.dept_mail.Search_from import search_from as dsearch_from
from .functionalities.dept_mail.Search_keyword import search_keyword as dsearch_keyword
from .functionalities.dept_mail.Search_sub import search_sub as dsearch_sub
from .functionalities.dept_mail.Search_date import search_date as dsearch_date
from .functionalities.dept_mail.Send_email import send_mail as dsend_mail

class Parser:
    def parse(self, command, sender_whatsapp_no):
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


        # ------------------------------------------------------ Mail --------------------------------------------------------------

        # create sub-parser for IITB mail command  for send and search
        mail_subparsers = mail_parser.add_subparsers(dest='mail_command', help='IITB Mail commands help')
        search_mail_parser = mail_subparsers.add_parser('search',help='Search Email from IITB Mailbox using filters')
        send_mail_parser = mail_subparsers.add_parser('send', help='Send Email from IITB Mail adding attachments ')

        #add arguements to search in IITB mail
        search_mail_parser.add_argument('-n', '--number', type=int, action='store', help='Show Top n mails in IITB Mailbox')
        search_mail_parser.add_argument('-k', '--keyword',type=str, action='store', help='Search in body of mail using keyword in IITB Mailbox')
        search_mail_parser.add_argument('-f', '--from_', type=str, action='store', help='Search using From/Senders mail address in IITB Mailbox')
        search_mail_parser.add_argument('-s', '--subject', type=str, action='store', help="Search using ubject in IITB Mailbox / substring match also possible")
        search_mail_parser.add_argument('-t', '--timeline', action='store', help='Search using timeline  in IITB Mailbox format DDMMYYYY DDMMYYYY', nargs=2)

        #add arguements to send from IITB mail
        send_mail_parser.add_argument('-to','--targets',type=str,action='store', help='Enter target email address as a  STRINGS separated by comma to send from IITB Mailbox')
        send_mail_parser.add_argument('-sub','--subject',type=str,action='store', help='Enter Subject of email to send from IITB Mailbox')
        send_mail_parser.add_argument('-b','--body',type=str,action='store', help='Enter Body of email to send from IITB  Mailbox')
        send_mail_parser.add_argument('-cc','--carboncopy',type=str,action='store', help='Enter CC address as a STRINGS separated by comma to send from IITB  Mailbox')
        send_mail_parser.add_argument('-bcc','--blindcarboncopy',type=str,action='store', help='Enter BCC address as a  STRINGS separated by comma to send from IITB  Mailbox')
        send_mail_parser.add_argument('-a','--attach',action='store_true', help='Enable attachments for email to send from IITB  Mailbox')
        send_mail_parser.add_argument('-fp','--filepath',action='store', help='Enter mutiple attachments file path using comma separated strings for email to send from IITB  Mailbox')

        # ------------------------------------------------------ Dmail --------------------------------------------------------------

        # create sub-parser for CSE Ldap mail command  for send and search
        dmail_subparsers = dmail_parser.add_subparsers(dest='dmail_command', help='CSE Ldap Mail commands help')
        dsearch_mail_parser = dmail_subparsers.add_parser('search',help='Search Email from CSE Ldap using filters')
        dsend_mail_parser = dmail_subparsers.add_parser('send', help='Send Email from CSE Ldap Mail adding attachments ')

        #add arguements to search in CSE Ldap mail
        dsearch_mail_parser.add_argument('-n', '--number', type=int,action='store', help='Show Top n mails in CSE Ldap Mailbox')
        dsearch_mail_parser.add_argument('-k', '--keyword', type=str,action='store', help='Search in body of mail using keyword in CSE Ldap Mailbox')
        dsearch_mail_parser.add_argument('-f', '--from_', type=str,action='store', help='Search using From/Senders mail address in CSE Ldap Mailbox')
        dsearch_mail_parser.add_argument('-s', '--subject', type=str,action='store', help="Search using ubject in CSE LdapMailbox / substring match also possible")
        dsearch_mail_parser.add_argument('-t', '--timeline', action='store', help='Search using timeline  in CSE Ldap Mailbox format DDMMYYYY DDMMYYYY', nargs=2)

        #add arguements to send from CSE Ldap mail
        dsend_mail_parser.add_argument('-to','--targets',type=str,action='store', help='Enter target email address as a  STRINGS separated by comma to send from CSE Ldap Mailbox')
        dsend_mail_parser.add_argument('-sub','--subject',type=str,action='store', help='Enter Subject of email to send from CSE Ldap Mailbox')
        dsend_mail_parser.add_argument('-b','--body',type=str,action='store', help='Enter Body of email to send from CSE Ldap Mailbox')
        dsend_mail_parser.add_argument('-cc','--carboncopy',type=str,action='store', help='Enter CC address as a STRINGS separated by comma to send from CSE Ldap Mailbox')
        dsend_mail_parser.add_argument('-bcc','--blindcarboncopy',type=str,action='store', help='Enter BCC address as a STRINGS separated by comma to send from CSE Ldap Mailbox')
        dsend_mail_parser.add_argument('-a','--attach',action='store_true', help='Enable attachments for email to send from CSE Ldap Mailbox')
        dsend_mail_parser.add_argument('-fp','--filepath',action='store', help='Enter multiple attachments file path using comma separated strings for email to send from CSE Ldap Mailbox')


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

        # parse the command
        args = parser.parse_args(shlex.split(command))

        print(args)
        # cse command is used
        if args.portal == 'cse':
            if args.cse_command == 'courses':
                c = Courses()

                # when any of autumn or spring is set, show courses in that semester only
                if args.autumn or args.spring:
                    return c.show_filtered_courses(args.filter, with_details = args.details, with_description = args.description,
                                        with_prereqs = args.prereqs, with_textrefs = args.textrefs,
                                        in_autumn = args.autumn, in_spring = args.spring)
                # when semester not given, show courses of both semester
                else:
                    return c.show_filtered_courses(args.filter, with_details = args.details, with_description = args.description,
                                        with_prereqs = args.prereqs, with_textrefs = args.textrefs)

            elif args.cse_command == 'students':
                s = Students()
                # filter based on name
                if args.filter is not None:
                    return s.show_filtered_students(args.batch, name_filter = args.filter, filters_name = True,
                                            with_advisor = args.advisor, with_interests = args.interest)

                # filter based on advisor name
                elif args.Advisor is not None:
                    return s.show_filtered_students(args.batch, advisor_filter = args.Advisor, filters_advisor = True,
                                            with_advisor = args.advisor, with_interests = args.interest)

                # filter based on interest
                elif args.Interest is not None:
                    return s.show_filtered_students(args.batch, interests_filter = args.Interest, filters_interests = True,
                                            with_advisor = args.advisor, with_interests = args.interest)

                else:
                    return s.show_students(args.batch, with_interests = args.interest, with_advisor = args.advisor)

            elif args.cse_command == 'faculties':

                f = Faculties()

                if args.filter is not None:
                    return f.show_filtered_faculties(name_filter = args.filter, filters_name = True, with_extension = args.extension,
                                            with_room = args.room, with_website = args.website, with_interests = args.interest)

                elif args.Interest is not None:
                    return f.show_filtered_faculties(interests_filter = args.Interest, filters_interests = True, with_extension = args.extension,
                                            with_room = args.room, with_website = args.website, with_interests = args.interest)

                else:
                    return f.show_faculties(with_extension = args.extension, with_room = args.room,
                                    with_website = args.website, with_interests = args.interest)

            elif args.cse_command == 'news':
                n = News()

                # show all news in the given timeline
                if args.timeline is not None:
                    return n.show_news_in_time_period(args.timeline[0], args.timeline[1], with_details = args.details)

                # show all news of the given year
                elif args.year is not None:
                    return n.show_news_in_a_year(args.year, with_details=args.details)

                # show all news of this year
                else:
                    return n.show_news_in_a_year(datetime.datetime.now().year, with_details=args.details)
            else:
                # return cse_parser.format_help()
                return "usage: cse [-h] {courses,students,faculties,news} ...\
\
positional arguments:\
{courses,students,faculties,news}\
                    CSE commands help\
courses             Info about courses\
students            Info about students\
faculties           Info about faculties\
news                Get news\
\
optional arguments:\
-h, --help            show this help message and exit"
        elif args.portal == 'moodle':
            if args.moodle_command == 'quizzes':
                q = Quizzes()
                if args.cid is not None:
                    return q.show_quizzes(sender_whatsapp_no, course_id = args.cid)
                else:
                    return q.show_all_quizzes(sender_whatsapp_no)

            elif args.moodle_command == 'grades':
                g  = Grades()
                return g.show_grades(sender_whatsapp_no, course_id = args.cid)

            elif args.moodle_command == 'forums':
                df = discussion_forums()
                return df.show_course_discussion_forums(args.cid, sender_whatsapp_no, args.number)

            elif args.moodle_command == 'discussions':
                d = Discussions()
                return d.show_discussions_from_a_forum(args.forum_id, sender_whatsapp_no, args.number)

            elif args.moodle_command == 'courses':
                c = moodle_courses()
                return c.show_courses(sender_whatsapp_no)

            elif args.moodle_command == 'announcements':
                a = Announcements()
                return a.show_course_announcements(args.cid, sender_whatsapp_no, args.number)

            elif args.moodle_command == 'assignments':
                a = Assignments()
                if args.course is not None:
                    return a.show_assignments(args.course, sender_whatsapp_no, show_only_due=args.due)
                else:
                    if args.due:
                        return a.show_all_due_assignments(sender_whatsapp_no)
                    else:
                        return a.show_all_assignments(sender_whatsapp_no)
            else:
                # return moodle_parser.format_help()
                return "usage: moodle [-h] {quizzes,grades,forums,discussions,courses,announcements,assignments} ...\
                        \
                        positional arguments:\
                          {quizzes,grades,forums,discussions,courses,announcements,assignments}\
                                                Moodle commands help\
                            quizzes             Info about quizzes\
                            grades              Info about grades\
                            forums              Info about discussion forums\
                            discussions         Info about discussions\
                            courses             Info about courses\
                            announcements       Info about announcements\
                            assignments         Info about assignments\
                        \
                        optional arguments:\
                          -h, --help            show this help message and exit"
        #Top level parser is mail
        elif args.portal == 'mail':
            #Second level parser is search
            if args.mail_command == 'search':
                # mail search -n and -k
                if args.keyword is not None:
                    if args.number is not None:
                        obj = search_keyword()
                        return obj.keyword(str(args.keyword),limit=int(args.number),sender_whatsapp_no=sender_whatsapp_no)
                    # mail search  -k
                    else:
                        obj = search_keyword()
                        return obj.keyword(str(args.keyword),sender_whatsapp_no=sender_whatsapp_no)
                elif args.subject is not None:
                    # mail search -n and -s
                    if args.number is not None:
                        obj = search_sub()
                        return obj.subject(str(args.subject),limit=int(args.number),sender_whatsapp_no=sender_whatsapp_no)
                    # mail search -s
                    else:
                        obj = search_sub()
                        return obj.subject(str(args.subject),sender_whatsapp_no=sender_whatsapp_no)
                elif args.from_ is not None:
                    # mail search -n and -f
                    if args.number is not None:
                        obj = search_from()
                        return obj.from_(str(args.from_),limit=int(args.number),sender_whatsapp_no=sender_whatsapp_no)
                    # mail search -f
                    else:
                        obj = search_from()
                        return obj.from_(str(args.from_),sender_whatsapp_no=sender_whatsapp_no)
                elif args.timeline is not None:
                    # mail search -n and -t
                    if args.number is not None:
                        obj = search_date()
                        return obj.date_(args.timeline[0], args.timeline[1],limit=int(args.number),sender_whatsapp_no=sender_whatsapp_no)
                    # mail search -t
                    else:
                        obj = search_date()
                        return obj.date_(args.timeline[0], args.timeline[1],sender_whatsapp_no=sender_whatsapp_no)
                # mail search -n
                elif args.number is not None:
                    obj = search_topn()
                    return obj.top(N=int(args.number),sender_whatsapp_no=sender_whatsapp_no)
                else :
                    send_mail_parser.print_help
            #Second level parser is send
            elif args.mail_command =='send':
                if args.targets is not None and args.subject is not None:
                    if args.attach is False:
                        obj=send_mail()
                        return obj.send_m(targets=args.targets,subject=args.subject,body=args.body,cc=args.carboncopy,bcc=args.blindcarboncopy,attach=False,sender_whatsapp_no=sender_whatsapp_no)
                    elif args.attach is True and args.filepath is not None :
                        obj=send_mail()
                        return obj.send_m(targets=args.targets,subject=args.subject,body=args.body,cc=args.carboncopy,bcc=args.blindcarboncopy,attach=True,filepath=args.filepath,sender_whatsapp_no=sender_whatsapp_no)
                    else :
                        send_mail_parser.print_help
                else :
                    mail_parser.print_help

        # Top level parser is dmail
        elif args.portal == 'dmail':
        #     #Second level parser is search
            if args.dmail_command == 'search':
                if args.keyword is not None:
                    #dmail search -n and -k
                    if args.number is not None:
                        obj = dsearch_keyword()
                        return obj.keyword(str(args.keyword),limit=int(args.number),sender_whatsapp_no=sender_whatsapp_no)
                    # dmail search -k
                    else:
                        obj = dsearch_keyword()
                        return obj.dkeyword(str(args.keyword),sender_whatsapp_no=sender_whatsapp_no)
                elif args.subject is not None:
                    # dmail search -n and -s
                    if args.number is not None:
                        obj = dsearch_sub()
                        return obj.subject(str(args.subject),limit=int(args.number),sender_whatsapp_no=sender_whatsapp_no)
                    # dmail search -s
                    else:
                        obj = dsearch_sub()
                        return obj.subject(str(args.subject),sender_whatsapp_no=sender_whatsapp_no)
                elif args.from_ is not None:
                    # dmail search -n and -f
                    if args.number is not None:
                        obj = dsearch_from()
                        return obj.from_(str(args.from_),limit=int(args.number),sender_whatsapp_no=sender_whatsapp_no)
                    # dmail search -f
                    else:
                        obj = dsearch_from()
                        return obj.from_(str(args.from_),sender_whatsapp_no=sender_whatsapp_no)

                elif args.timeline is not None:
                    # dmail search -n and -t
                    if args.number is not None:
                        obj = dsearch_date()
                        return obj.date_(args.timeline[0], args.timeline[1],limit=int(args.number),sender_whatsapp_no=sender_whatsapp_no)
                    # dmail search -t
                    else:
                        obj = dsearch_date()
                        return obj.date_(args.timeline[0], args.timeline[1],sender_whatsapp_no=sender_whatsapp_no)
                #dmail search -n
                elif args.number is not None:
                    obj = dsearch_topn()
                    return obj.top(sender_whatsapp_no=sender_whatsapp_no, N=int(args.number))

                else :
                    send_mail_parser.print_help
            #Second level parser is send
            elif args.dmail_command =='send':
                if args.targets is not None and args.subject is not None:
                    if args.attach is False:
                        obj=dsend_mail()
                        return obj.send_m(targets=args.targets,subject=args.subject,body=args.body,cc=args.carboncopy,bcc=args.blindcarboncopy,attach=False,sender_whatsapp_no=sender_whatsapp_no)
                    elif args.attach is True and args.filepath is not None :
                        obj=dsend_mail()
                        return obj.send_m(targets=args.targets,subject=args.subject,body=args.body,cc=args.carboncopy,bcc=args.blindcarboncopy,attach=True,filepath=args.filepath,sender_whatsapp_no=sender_whatsapp_no)
                    else :
                        dsend_mail_parser.print_help
                else:
                    dmail_parser.print_help
        else:
            return parser.format_help()