from django.shortcuts import render
from cryptography.fernet import Fernet
from rest_framework.decorators import api_view
from  django.http import HttpResponse
from  django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import users

from .serializers import usersSerializer
from .demo import Courses
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser

from twilio.rest import Client
import requests
import json
# Create your views here.

@api_view(['GET', 'POST', 'DELETE'])
def api(request):
        if request.method=="GET":
            users1 = users.objects.all()
            serializer = usersSerializer(users1, many=True)
            return JsonResponse(serializer.data,safe=False)
        elif request.method=="POST":
            users_data = JSONParser().parse(request)
            if users_data["ldap_pass"] != "":
                users_data["ldap_pass"] = str(encrypt_message(users_data["ldap_pass"]))
            if users_data["cse_email_pass"] != "":
                users_data["cse_email_pass"] = str(encrypt_message(users_data["cse_email_pass"]))
            if users_data["moodle_pass"] != "":
                users_data["moodle_pass"] = str(encrypt_message(users_data["moodle_pass"]))
            users_serializer = usersSerializer(data=users_data,safe=False)
            '''if users_serializer.is_valid():
                users_serializer.save()
                return JsonResponse(users_serializer.data, status=status.HTTP_201_CREATED)
            return JsonResponse(users_serializer.errors, status=status.HTTP_400_BAD_REQUEST)'''
        elif request.method == 'DELETE':
            count =[]
            #count = users.objects.all().delete()
            return JsonResponse({'message': '{} Users were deleted successfully!'.format(count[0])},
                                status=status.HTTP_204_NO_CONTENT,safe=False)

@api_view(['GET', 'PUT', 'DELETE'])
def api_detail(request, pk):
        try:
            user = users.objects.get(pk=pk)
        except users.DoesNotExist:
            return JsonResponse({'message': 'The user does not exist'}, status=status.HTTP_404_NOT_FOUND,safe=False)

        if request.method == 'GET':
            user_serializer = usersSerializer(user)
            return JsonResponse(user_serializer.data,safe=False)

        elif request.method == 'PUT':
            user_data = JSONParser().parse(request)
            user_serializer = usersSerializer(user, data=user_data)
            '''if user_serializer.is_valid():
                user_serializer.save()
                return JsonResponse(user_serializer.data)
            else:
                return JsonResponse(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST,safe=False)'''

        elif request.method == 'DELETE':
            #user.delete()

            return JsonResponse({'message': 'User was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT,safe=False)

class Users:
    def  __init__(self,pk):


            self.pk = pk


    def getLDAP(self):
     try:
         self.user = users.objects.get(pk=self.pk)
         return self.user.ldap_email, self.decrypt_message(self.user.ldap_pass)
     except users.DoesNotExist:
         return None, None

    def getCSEMail(self):
      try:
         self.user = users.objects.get(pk=self.pk)
         return self.user.cse_email, self.decrypt_message(self.user.cse_email_pass)

      except users.DoesNotExist:
         return None, None


    def getMoodle(self):
      try:
        self.user = users.objects.get(pk=self.pk)
        token = None


        print("haha", self.user.moodle_id, "adsjfha", self.decrypt_message(self.user.moodle_pass))
        payload = {'username': self.user.moodle_id,'password': self.decrypt_message(self.user.moodle_pass), 'service': 'moodle_mobile_app'}
        try:
            # get the token
            res = requests.post('https://moodle.iitb.ac.in/login/token.php', payload)
            if res.status_code == 200:
                print("MOODLE: Got token")
                token = json.loads(res.text)['token']
            else:
                return None, None
        except Exception:
            return None, None

        if token is None:
            return None, None

        payload = {'wstoken': token,'wsfunction': 'core_webservice_get_site_info'}
        try:
            # get the userid
            res = requests.post('https://moodle.iitb.ac.in/webservice/rest/server.php?moodlewsrestformat=json',payload)
            res = json.loads(res.content)
            if "exception" in res.keys():
                return token, None
            else:
                print("MOODLE: Got userid")
                userid = res['userid']
                return token, res['userid']
        except Exception:
            return token, None

        return token, userid
        # return self.user.moodle_id, self.decrypt_message(self.user.moodle_pass)
      except users.DoesNotExist:
         return -1, -1

    def getAll(self):
       try:
           self.user = users.objects.get(pk=self.pk)

           data = {'name': self.user.name, 'mobile_no': self.user.mobile_no, 'ldap_email': self.user.ldap_email, 'ldap_pass': self.user.ldap_pass,
                'cse_email': self.user.cse_email, 'cse_email_pass': self.user.cse_email_pass, 'moodle_id': self.user.moodle_id,
                'moodle_pass': self.user.moodle_pass}

           return data

       except users.DoesNotExist:
         return None, None



    def load_key(self):
        """
        Load the previously generated key
        """
        return open("secretkey.key", "rb").read()



    def decrypt_message(self,encrypted_message):
        """
        Decrypts an encrypted message
        """
        key = self.load_key()
        f = Fernet(key)
        bcode=(encrypted_message).encode()
        decrypted_message = f.decrypt(bcode)
        return decrypted_message.decode('utf-8')




class userList(APIView):
    def get(self,request):
        c = Courses()
        table = c.show_courses(True, True)

        return Response(table)

    def post(self,request):
        self.generate_key()
        users_data = JSONParser().parse(request)
        if users_data["ldap_pass"] != "":
          users_data["ldap_pass"] =str(self.encrypt_message(users_data["ldap_pass"]))
        if users_data["cse_email_pass"] != "":
          users_data["cse_email_pass"] =str( self.encrypt_message(users_data["cse_email_pass"] ))
        if users_data["moodle_pass"] != "":
          users_data["moodle_pass"] = str(self.encrypt_message(users_data["moodle_pass"]))
        users_serializer = usersSerializer(data=users_data)
        if users_serializer.is_valid():
            users_serializer.save()
            return JsonResponse(users_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(users_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # print("Got a POST request")
        # print(request.POST)
        # msg = request.POST.get('Body')

        # print(f"Received Msg: {msg}")



        # account_sid = "AC10b5aee8f4096723a3d942118fccdfae"
        # auth_token = "d3156a5cfb9a2aecd870b863e93d8f96"
        # client = Client(account_sid, auth_token)
        # # this is the Twilio sandbox testing number
        # from_whatsapp_number='whatsapp:+14155238886'
        # # replace this number with your own WhatsApp Messaging number
        # to_whatsapp_number=request.POST.get('From')
        # # to_whatsapp_number='whatsapp:+918101482399'


        # c = Courses()
        # table = c.show_courses()
        # print(table, len(table))

        # # client.messages.create(body=f"Hi from server! You said {msg}",
        # #                       from_=from_whatsapp_number,
        # #                       to=to_whatsapp_number)

        # while len(table) > 0:
        #     client.messages.create(body=table[:1600],
        #                           from_=from_whatsapp_number,
        #                           to=to_whatsapp_number)
        #     table = table[1600:]


        # response = MessagingResponse()
        # message = Message()
        # message.body(f"Hi from server! You said {msg}")
        # response.append(message)
        # response.redirect('https://demo.twilio.com/welcome/sms/')


        # resp = MessagingResponse()
        # resp.message(f"Hi from server! You said {msg}")
        return Response("done!")


    def load_key(self):
        """
        Load the previously generated key
        """
        return open("secretkey.key", "rb").read()
        #return "oUM9KoViX9or94mAb8ENHXQyIHHRAsZApCYmTymBkpU="

    def encrypt_message(self,message):
        """
        Encrypts a message
        """
        key = self.load_key()
        encoded_message = message.encode('utf-8')
        f = Fernet(key)
        encrypted_message = f.encrypt(encoded_message)

        return encrypted_message.decode()

    def decrypt_message(self,encrypted_message):
        """
        Decrypts an encrypted message
        """
        key = self.load_key()
        f = Fernet(key)
        decrypted_message = f.decrypt(encrypted_message.encode())

        return decrypted_message.decode('utf-8')
