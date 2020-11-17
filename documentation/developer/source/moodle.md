## Moodle

#### Intro
Moodle consists of 7 subcomponents where the user will fetch information from. 
Source code for this can be found in the functionalities/moodle folder. 

Each of the 7 classes represent one subcomponent:

#### Class names, with their functions
* <b>courses</b>
  * ```
    def show_courses(self):
        '''
        Show details of all enrolled courses
        '''
    ```

* <b>discussions</b>
  * ```
    def show_discussions_from_a_forum(self, forum_id, n = None):
        '''
        Show all discussions of a particular discussion forum
        Input:
            forum_id (int) : ID of the discussion forum
            n (int) : show only top `n` discussions
        '''
    ```

* <b>quizzes</b>
  * ```
    def show_quizzes(self, course_id):
        '''
        Show quizzes of a course
        Input:
            course_id (int) : ID of the course
        '''
    ```
  * ``` 
    def show_all_quizzes(self):
        '''
        Show quizzes of all courses
        '''
    ```

* <b>announcements</b>
  * ```
    def show_assignments(self, course, show_only_due):
        '''
        Show assignments of a course
        Input:
            course (string) : filter for course name
            show_only_due (boolean) : when set to True, shows only due assignments
        '''
    ```
* <b>forums</b>
  * ```
    def show_course_discussion_forums(self, course_id, n = None):
        '''
        Show all discussion forums of a particular course
        Input:
            course_id (int) : ID of the course
            n (int) : show only top `n` discussion forums
        '''
    ```
* <b>grades</b>
  * ```
    def show_grades(self, course_id):
        '''
        Show grades of a course
        Input:
            course_id (int) : ID of the course
        '''
    ```

* <b>assignments</b>
  * ```
    def show_assignments(self, course, show_only_due):
        '''
        Show assignments of a course
        Input:
            course (string) : filter for course name
            show_only_due (boolean) : when set to True, shows only due assignments
        '''
    ```

#### Developing the moodle component
* The documentation to use the moodle apis can be found at:
  * “https://docs.moodle.org/dev/Creating_a_web_service_client”
* Also, a developer can create a sandbox account for moodle, where list of all the APIs are available. ("https://sandbox.moodledemo.net/")
* When a user logs in the first time, the user token is stored in an encrypted manner in the moodle file under the configs folder.
* This token is decrypted just before every call and a request is sent to the respective moodle resource from where information is fetched.
* Please go through the moodle component's source code for more details on parsing and making API calls.
* A developer can add more functionalities for the moodle component by using the APIs, and can also add more flags to the existing classes.


