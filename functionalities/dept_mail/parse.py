
# all enrolled courses
import sys
from Search_topn import search_topn
from Search_keyword import search_keyword
from Search_from import search_from
from Search_sub import search_sub
from Search_date import search_date 
#from Send_email import send_email
if len(sys.argv) == 1:
    exit(1)

if sys.argv[1] == '-n' or sys.argv[1] == '--number':
    obj = search_topn()
    obj.top(int(sys.argv[2]))
elif sys.argv[1] == '-k' or sys.argv[1] == '--keyword':
    obj = search_keyword()
    obj.keyword(sys.argv[2])
elif sys.argv[1] == '-s' or sys.argv[1] == '--subject':
    obj = search_sub()
    obj.subject(sys.argv[2])
elif sys.argv[1] == '-f' or sys.argv[1] == '--from':
    obj = search_from()
    obj.from_(sys.argv[2])
elif sys.argv[1] == '-t' or sys.argv[1] == '--timeline':
    obj = search_date()
    obj.date_(sys.argv[2],sys.argv[3])
elif sys.argv[1] == '-sd' or sys.argv[1] == '--send':
    obj = send_email()
    obj.from_(sys.argv[2],sys.argv[3])