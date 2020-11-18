from rest_framework import serializers
from .models import users

class usersSerializer(serializers.ModelSerializer):
    class Meta:
        model=users
        #fields={'name','mobile_no','ldap_email','ldap_pass','cse_email','cse_email_pass','moodle_id','moodle_pass'}
        fields ='__all__'

