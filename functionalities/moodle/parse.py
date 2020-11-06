# all enrolled courses
import sys
from courses import Courses
from grades import Grades
from quizzes import Quizzes
from assignments import Assignments
from forums import discussion_forums
from discussions import Discussions
from announcements import Announcements

if len(sys.argv) == 1:
    exit(1)

if sys.argv[1] == '-c' or sys.argv[1] == '--courses':
    c = Courses()
    c.show_courses()
elif sys.argv[1] == '-g' or sys.argv[1] == '--grade':
    c = Grades()
    x = sys.argv[2]
    c.show_grades(x)
elif sys.argv[1] == '-q' or sys.argv[1] == '--quiz':
    c = Quizzes()
    x = sys.argv[2]
    c.show_quizzes(x)
elif sys.argv[1] == '-a' or sys.argv[1] == '--assignment':
    c = Assignments()
    if len(sys.argv) == 2:
        c.show_all_assignments()
    elif len(sys.argv) ==3 and sys.argv[2] == '-due':
        c.show_all_due_assignments()
elif sys.argv[1] == '-f' or sys.argv[1] == '--forum':
    c = discussion_forums()
    if len(sys.argv) == 3:
        c.show_course_discussion_forums(sys.argv[2])
    elif len(sys.argv) ==4:
        c.show_course_discussion_forums(sys.argv[2], sys.argv[3])
elif sys.argv[1] == '-d' or sys.argv[1] == '--discussion':
    c = Discussions()
    if len(sys.argv) == 3:
        c.show_discussions_from_a_forum(sys.argv[2])
    elif len(sys.argv) ==4:
        c.show_discussions_from_a_forum(sys.argv[2], sys.argv[3])
elif sys.argv[1] == '-n' or sys.argv[1] == '--announcements':
    c = Announcements()
    if len(sys.argv) == 3:
        c.show_course_announcements(sys.argv[2])
    elif len(sys.argv) ==4:
        c.show_course_announcements(sys.argv[2], sys.argv[3])    