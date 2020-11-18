import requests
import json
from bs4 import BeautifulSoup as bs
from tabulate import tabulate
import datetime
url = "https://www.cse.iitb.ac.in/~internal-live/api/news/news_all/?format=json&year="

class News:
    def show_news_in_a_year(self, year, with_details = False):
        '''
        This function will fetch all the news of a particular year from CSE website and show them
        Input:
            year (string): show news of this particular year
            with_details (boolean): whether to show 'details' of the news in addition to other information

        Following things are shown for each news normally:
            ['Date', 'Snippet']
        '''
        global url
        url = url + str(year)
        table = []
        ret = ""
        try:
            res = requests.get(url)
            for x in json.loads(res.text):
                if with_details:
                    news = []
                    news.append(['Date', x['ndate']])
                    news.append(['Snippet', bs(x['snippet'], 'html.parser').get_text()])
                    news.append(['Details', bs(x['details'], 'html.parser').get_text()])
                    ret += (tabulate(news))
                else:
                    table.append([x['ndate'], bs(x['snippet'], 'html.parser').get_text()])

        except Exception as err:
            return (f"Error: {err}")
        else:
            if not with_details:
                return (tabulate(table, headers = ['Date', 'Snippet']))

        return ret

    def show_news_in_time_period(self, start_date, end_date, with_details = False):
        '''
        This function will fetch all the news in a particular time frame from CSE website and show them
        Input:
            start_date (string): show news starting from this date
            end_date (string): show news ending at this date
            with_details (boolean): whether to show 'details' of the news in addition to other information

        Following things are shown for each news normally:
            ['Date', 'Snippet']

        Output:
            Print in the mentioned format or print "No news found in this time frame" if there is no news found
        '''
        try:
            start_date = datetime.datetime.strptime(start_date, '%d%m%Y')
            start_year = int(start_date.strftime("%Y"))
            end_date = datetime.datetime.strptime(end_date, '%d%m%Y')
            end_year = int(end_date.strftime("%Y"))
        except ValueError:
            return ("Incorrect date format, format should be DDMMYYYY")

        table = []
        cnt = 0
        ret = ''
        for year in range(end_year, start_year - 1, -1):
            global url
            newurl = url + str(year)
            try:
                res = requests.get(newurl)

                for x in json.loads(res.text):
                    news_date = datetime.datetime.strptime(x['ndate'], '%Y-%m-%d')
                    # news date after end_date, ignore this news
                    if news_date > end_date:
                        continue

                    # news date before start_date, we have already got news in the mentioned time period
                    if news_date < start_date:
                        break

                    if with_details:
                        news = []
                        news.append(['Date', x['ndate']])
                        news.append(['Snippet', bs(x['snippet'], 'html.parser').get_text()])
                        news.append(['Details', bs(x['details'], 'html.parser').get_text()])
                        ret += (tabulate(news))
                    else:
                        table.append([x['ndate'], bs(x['snippet'], 'html.parser').get_text()])

                    cnt += 1

            except Exception as err:
                return (f"Error: {err}")

        if not with_details and cnt > 0:
            return (tabulate(table, headers = ['Date', 'Snippet']))
        elif cnt == 0:
            return ("No news found in this time frame")

        return ret
