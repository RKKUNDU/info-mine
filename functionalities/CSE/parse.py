# all enrolled courses
import sys
from courses import Courses
from faculties import Faculties
from news import News
from students import Students
if len(sys.argv) == 1:
    exit(1)

if sys.argv[1] == '-c' or sys.argv[1] == '--courses':
    c = Courses()
    if len(sys.argv) == 2:
        c.show_courses()
    elif len(sys.argv) == 3 and (sys.argv[2] == '-a' or sys.argv[2] == '-autumn'):
        c.show_courses(in_autumn = True, in_spring = False)
    elif len(sys.argv) == 3 and (sys.argv[2] == '-s' or sys.argv[2] == '-spring'):
        c.show_courses(in_autumn = False, in_spring = True)
    elif len(sys.argv) == 3:
        c.show_filtered_courses(sys.argv[2])
    elif len(sys.argv) > 3:
        with_details = False 
        with_description = False
        with_prereqs = False
        with_textrefs = False
        in_autumn = False
        in_spring = False
        for x in sys.argv[3]:
            if x == 'd':
                with_details = True
            elif x == 'p':
                with_prereqs = True
            elif x == 't':
                with_textrefs = True
            elif x == 'v':
                with_description = True
            elif x == 'a':
                in_autumn = True
            elif x == 's':
                in_spring = True

        if not(in_autumn or in_spring): 
            in_autumn = True
            in_spring = True

        c.show_filtered_courses(sys.argv[2], with_details, with_description, with_prereqs, with_textrefs, in_autumn, in_spring)


elif sys.argv[1] == '-f' or sys.argv[1] == '--faculty':
    c = Faculties()
    if len(sys.argv) == 2: # -f
        c.show_faculties()
    elif len(sys.argv) == 3 and (sys.argv[2][0] != '-'): # -f iwer
        with_interests = False
        with_website = False
        with_extension = False
        with_room = False
        for x in sys.argv[2]:
            if x == 'i':
                with_interests = True
            elif x == 'w':
                with_website = True
            elif x == 'e':
                with_extension = True
            elif x == 'r':
                with_room = True

        c.show_faculties(with_interests, with_website, with_extension, with_room)
    elif len(sys.argv) == 5 and (sys.argv[2][0] != '-'): # -f iwer -[n, i] filter
        with_interests = False
        with_website = False
        with_extension = False
        with_room = False
        name_filter = None
        interests_filter = None
        filters_name = False
        filters_interests = False
        for x in sys.argv[2]:
            if x == 'i':
                with_interests = True
            elif x == 'w':
                with_website = True
            elif x == 'e':
                with_extension = True
            elif x == 'r':
                with_room = True
        
        if sys.argv[3] == '-n':
            filters_name = True
            name_filter = sys.argv[4]
        elif sys.argv[3] == '-i':
            filters_interests = True
            interests_filter = sys.argv[4]

        c.show_filtered_faculties(name_filter, interests_filter, filters_name, filters_interests, with_extension, with_room, with_website, with_interests)
        
    elif len(sys.argv) == 4 and (sys.argv[2][0] == '-'): # -f -[n, i] filter
        with_interests = False
        with_website = False
        with_extension = False
        with_room = False
        name_filter = None
        interests_filter = None
        filters_name = False
        filters_interests = False
        
        if sys.argv[2] == '-n':
            filters_name = True
            name_filter = sys.argv[3]
        elif sys.argv[2] == '-i':
            filters_interests = True
            interests_filter = sys.argv[3]

        c.show_filtered_faculties(name_filter, interests_filter, filters_name, filters_interests, with_extension, with_room, with_website, with_interests)
    
elif sys.argv[1] == '-n' or sys.argv[1] == '--news':
    c = News()
    if len(sys.argv) == 2:
        pass
    elif len(sys.argv[2]) == 4:
        if len(sys.argv) == 4 and sys.argv[3] == '-v': # -n 2020 -v
            c.show_news_in_a_year(sys.argv[2], with_details = True)
        else:
            c.show_news_in_a_year(sys.argv[2])
    elif len(sys.argv) == 5 and sys.argv[2] == '-t': # -n -t start end
        c.show_news_in_time_period(sys.argv[3], sys.argv[4])
    elif len(sys.argv) == 6 and sys.argv[3] == '-t': # -n -v -t start end
        c.show_news_in_time_period(sys.argv[4], sys.argv[5], with_details = True)

elif sys.argv[1] == '-s' or sys.argv[1] == '--student':
    c = Students()
    if len(sys.argv) == 3:
        c.show_students(sys.argv[2])
    elif len(sys.argv) == 4 and (sys.argv[3][0] != '-'): # -s batch ia
        with_interests = False
        with_advisor = False
        for x in sys.argv[3]:
            if x == 'i':
                with_interests = True
            elif x == 'a':
                with_advisor = True
            
        c.show_students(sys.argv[2], with_interests, with_advisor)
    elif len(sys.argv) == 6 and (sys.argv[3][0] != '-'): # -f batch ia -[n, i, a] filter
        with_interests = False
        with_advisor = False
        advisor_filter = None
        name_filter = None
        interests_filter = None
        filters_name = False
        filters_interests = False
        filters_advisor = False
        for x in sys.argv[3]:
            if x == 'i':
                with_interests = True
            elif x == 'a':
                with_advisor = True
        
        if sys.argv[4] == '-n':
            filters_name = True
            name_filter = sys.argv[5]
        elif sys.argv[4] == '-i':
            filters_interests = True
            interests_filter = sys.argv[5]
        elif sys.argv[4] == '-a':
            filters_advisor = True
            advisor_filter = sys.argv[5]

        c.show_filtered_students(sys.argv[2], name_filter , interests_filter , advisor_filter , filters_name , filters_interests , filters_advisor , with_advisor , with_interests )

    elif len(sys.argv) == 5 and (sys.argv[3][0] == '-'): # -f batch -[n, i, a] filter
        with_interests = False
        with_advisor = False
        advisor_filter = None
        name_filter = None
        interests_filter = None
        filters_name = False
        filters_interests = False
        filters_advisor = False
        
        if sys.argv[3] == '-n':
            filters_name = True
            name_filter = sys.argv[4]
        elif sys.argv[3] == '-i':
            filters_interests = True
            interests_filter = sys.argv[4]
        elif sys.argv[3] == '-a':
            filters_advisor = True
            advisor_filter = sys.argv[4]

        c.show_filtered_students(sys.argv[2], name_filter , interests_filter , advisor_filter , filters_name , filters_interests , filters_advisor , with_advisor , with_interests )