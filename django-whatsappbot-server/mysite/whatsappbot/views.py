from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from twilio.rest import Client

from .command_parser import Parser

class Message(APIView):
    def get(self,request):
        # c = Courses()
        # table = c.show_courses(True, True)

        return Response("Whatsapp Bot")

    def post(self, request):
        msg = request.POST.get('Body')
        print(f"Received Msg: {msg}")
        account_sid = "AC671319f0a2437a4bca6af1644c772830"
        auth_token = "a00d6c3e2488a507404a43a6307a2b4d"
        client = Client(account_sid, auth_token)

        # this is the Twilio number
        from_whatsapp_number='whatsapp:+14155238886'

        to_whatsapp_number=request.POST.get('From')

        print(f"Received Msg: {msg} from: {to_whatsapp_number}")

        p = Parser()
        # response = p.parse(msg, '9800400408')
        response = p.parse(msg, to_whatsapp_number[10:]) # remove first few characters that is 'whatsapp:+'
        print(response)
        # client.messages.create(body=f"Hi from server! You said: \'{msg}\'",
        #                       from_=from_whatsapp_number,
        #                       to=to_whatsapp_number)


        # api can send maxm 1600 characters
        while len(response) > 0:
            client.messages.create(body=response[:1600],
                                  from_=from_whatsapp_number,
                                  to=to_whatsapp_number)
            response = response[1600:]


        # client.messages.create(body=response,
        #                       from_=from_whatsapp_number,
        #                       to=to_whatsapp_number)
        #self.generate_key()
        # users_data = JSONParser().parse(request)
        # if users_data["ldap_pass"] != "":
        #   users_data["ldap_pass"] =str(self.encrypt_message(users_data["ldap_pass"]))
        # if users_data["cse_email_pass"] != "":
        #   users_data["cse_email_pass"] =str( self.encrypt_message(users_data["cse_email_pass"] ))
        # if users_data["moodle_pass"] != "":
        #   users_data["moodle_pass"] = str(self.encrypt_message(users_data["moodle_pass"]))
        # users_serializer = usersSerializer(data=users_data)
        # if users_serializer.is_valid():
        #     users_serializer.save()
        #     return JsonResponse(users_serializer.data, status=status.HTTP_201_CREATED)
        # return JsonResponse(users_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # print("Got a POST request")
        # print(request.POST)


        # c = Courses()
        # table = c.show_courses()
        # print(table, len(table))



        # return Response("done!")
        return Response(msg)
