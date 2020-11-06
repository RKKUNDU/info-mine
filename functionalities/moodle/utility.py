import getpass
import sys
sys.path.append("../../")

from security.moodle_credentials import moodle_credential
class utils:
    def get_credential():
        moodle = moodle_credential()
        if moodle.get_stored_token() is None or moodle.get_stored_userid is None:
            id, password = utils.take_input()
            moodle.write_credential(id, password)   

        return moodle.get_stored_token(), moodle.get_stored_userid()

    def take_input():
        id = input("Enter your Moodle User ID: ")
        password = getpass.getpass()
        return id, password

    
