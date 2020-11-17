## CSE 

#### Intro
The cse component of  info-mine consists of four classes. Each of these classes represent a subcomponent under the cse component. 

#### Class names, with their functions
* <b>courses</b>
  * ```
    def show_courses(self, in_autumn = True, in_spring = True):
        '''
        This function will fetch all the courses from CSE website and show them
        Input:
            in_autumn (boolean) : whether the course is offered in autumn semester
            in_spring (boolean) : whether the course is offered in spring semester
        Following things are shown for each course:
        ['Semester', 'Course Code', 'Course Name', 'Instructor Name']
        '''
    ```
  * ```
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
    ```

* <b>faculties</b>
  * ```
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
    ```
  * ```
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
    ```

* <b>news</b>
  * ```
    def show_news_in_a_year(self, year, with_details = False):
        '''
        This function will fetch all the news of a particular year from CSE website and show them
        Input:
            year (string): show news of this particular year
            with_details (boolean): whether to show 'details' of the news in addition to other information
            
        Following things are shown for each news normally:
            ['Date', 'Snippet']
        '''
    ```
  * ```
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
    ```

* <b>students</b>
  * ```
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
    ```
  * ```
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
    ```


#### Developing the cse component
* To scrape information from the cse website, we call the API made available by the cse department:
  * https://www.cse.iitb.ac.in/~internal-live/api/
* Using these APIs a developer can always add more functionalities to the existing classes, and also implement new features of their own.
* For example, subcomponents such as exam timetable, publications etc. can be further added to this component.
* Please go through the classes in the source code to further understand the details.