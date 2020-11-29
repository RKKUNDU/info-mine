import getpass
import sys
sys.path.append("../../")

from security.moodle_credentials import moodle_credential
class utils:
    def get_credential():
        '''
        fetch moodle credential from config file or USER INPUT
        Prompt user to give user correct credentials until correct credentials given or
        the user gives 'q' or 'quit' as id
        '''
        moodle = moodle_credential()
        if moodle.get_stored_token() is None or moodle.get_stored_userid is None:
            credential_set = False
            while not credential_set:
                id, password = utils.take_input()
                if id == 'q' or id == 'quit':
                    exit(0)

                credential_set = moodle.write_credential(id, password)
                if not credential_set:
                    print("Invalid username/password. Type q or quit to exit")

        return moodle.get_stored_token(), moodle.get_stored_userid()

    def take_input():
        '''
        Take moodle credential from user
        '''
        id = input("Enter your Moodle User ID: ")   
        if id == 'q' or id == 'quit':
            return id, None

        password = getpass.getpass()
        return id, password

    
