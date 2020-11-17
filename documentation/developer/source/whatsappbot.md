## Whatsapp Bot

#### Registration
The front end, where a user registers is present in the:   
<b>/infomine/mysite/template/index.html</b>      
</br>Front end for a user update is present in the:   
<b>/infomine/mysite/template/update.html</b>

#### Backend
The views.py file for registration present in    
<b>/infomine/mysite/usersapi/views.py</b>.

The entry point for a registration request into the server
```
@api_view(['GET', 'POST', 'DELETE'])
def api(request):
'''
This function handles the requests received by a client for registration or to fetch details of a user.
'''
```

The users class, through which a user's creds are stored or retrieved.   
```
class Users:

def getLDAP(self):
'''
Gets the LDAP creds of a user object.
'''

def getCSEMail(self):
'''
Gets the CSE creds of a user object.
'''

def getMoodle(self):
'''
Gets the moodle creds of a user object.
'''

def load_key(self):
'''
Load the previously generated key
'''

def decrypt_message(self,encrypted_message):
'''
Decrypts an encrypted message
'''
```



The whatsapp bot uses Twilio to receive messages, call a callback function, and to send the message back to the user that sent the whatsapp message. The processing of the messages happen in our Django framework.   
Majority of the code for the command line tool is reused here to parse the requests by the user, hence the functions will remain the same as mentioned in the previous sections for moodle, email and cse.   
When a message arrives from our Twilio sandbox account, it is processed by:   
```
/infomine/mysite/whatsappbot/views.py (in views.py file)

 def post(self, request):
 '''
 This function receives the message, it sends the message to the parser which calls the one of the appropriate function availble in moodle, cse and email components
 '''
 ```
 The parser has to parse this request, the below function does this:   
 ```
  /infomine/mysite/whatsappbot/command_parser.py (in command_parser.py file)
  def parse(self, command, sender_whatsapp_no):
  '''
  This function determines what kind of a command has been sent as a whatsapp message and calls the appropriate function.
  '''
```
