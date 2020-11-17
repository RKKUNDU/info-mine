## Email

### Institute mail

The institute mail has five classes for searching the email based on different mechanisms/flags. It has one class to send the email with the respective flags. For the first time usage, the user is asked for his/her credentials. These credentials are encrypted and stored on the local system of the user in a file under the configs folder. Incase the user enters the wrong credentials, the credentials are not stored and no request is made. Please use the "security" module to encrypt and decrypt the creds. Here is a list of the classes available in the institute mail component. 

#### Searching for mails

* <b>Search_Date</b>
  * ```
    def date_(self,date1,date2):
    ''' 
    This function searches for email within the specified timeline between date1 as the starting time and date2 as the finish time
    '''
    ```

* <b>Search_from</b>
  * ```
    def from_(self,sender):
    ''' 
    This function searches for mail based on the substring of the 'sender' variable
    '''
    ```

* <b>Search_keyword</b>
  * ```
    def keyword(self,key):
    '''
    This function searches for email based on the key variable passed by the user, it will try to match any substring present in the key variable
    '''
    ```

* <b>Search_sub</b>
  * ```
    def subject(self,sub):
    '''
    This function searches for email based on the subject of the mails, and tries to match any substring with the the value present in the 'sub' variable.
    '''
    ```

* <b>Search_topn</b>
  * ```
    def top(self,N):
    '''
    This function fetches the top n latest mails, where n is an integer.
    '''
    ```
#### Sending mails
* This is a standalone script 'Send_mail.py' which will send the email based on the flags passed to it.

### Department mail

The department mail has five classes for searching the email based on different mechanisms/flags. It has one class to send the email with the respective flags. For the first time usage, the user is asked for his/her credentials. These credentials are encrypted and stored on the local system of the user in a file under the configs folder. Incase the user enters the wrong credentials, the credentials are not stored and no request is made. Please use the "security" module to encrypt and decrypt the creds. Here is a list of the classes available in the department mail component. 

#### Searching for mails

* <b>Search_Date</b>
  * ```
    def date_(self,date1,date2):
    ''' 
    This function searches for email within the specified timeline between date1 as the starting time and date2 as the finish time
    '''
    ```

* <b>Search_from</b>
  * ```
    def from_(self,sender):
    ''' 
    This function searches for mail based on the substring of the 'sender' variable
    '''
    ```

* <b>Search_keyword</b>
  * ```
    def keyword(self,key):
    '''
    This function searches for email based on the key variable passed by the user, it will try to match any substring present in the key variable
    '''
    ```

* <b>Search_sub</b>
  * ```
    def subject(self,sub):
    '''
    This function searches for email based on the subject of the mails, and tries to match any substring with the the value present in the 'sub' variable.
    '''
    ```

* <b>Search_topn</b>
  * ```
    def top(self,N):
    '''
    This function fetches the top n latest mails, where n is an integer.
    '''
    ```
#### Sending mails
* This is a standalone script 'Send_mail.py' which will send the email based on the flags passed to it.