from django.shortcuts import render,redirect
from cryptography.fernet import Fernet
from  django.http import HttpResponse
from  django.shortcuts import get_object_or_404
from rest_framework import status
from django.http.response import JsonResponse
from usersapi.serializers import usersSerializer
from usersapi.views import Users
from usersapi.models import users

# Create your views here.
def home(request):

    return render(request,'index.html',{})


def update_page(request):

    return render(request,'update.html',{})




def register(request):


   # Get username and password and other credentials from posted data and store into the db

   if request.method == 'POST':
        name = request.POST.get('name')
        code = str(request.POST.get('countryCode'))
        mobile_no =code+ str(request.POST.get('mobile_no'))
        ldap_email = request.POST.get('ldap_email')
        ldap_pass = request.POST.get('ldap_pass')
        cse_email = request.POST.get('cse_email')
        cse_email_pass = request.POST.get('cse_email_pass')
        moodle_id = request.POST.get('moodle_id')
        moodle_pass = request.POST.get('moodle_pass')

        if str(ldap_pass) != "":

            ldap_pass = str(encrypt_message(ldap_pass))
        if str(cse_email_pass) != "":
            cse_email_pass = str(encrypt_message(cse_email_pass))
        if str(moodle_pass) != "":
            moodle_pass = str(encrypt_message(moodle_pass))

        if str(ldap_email)=="":
            ldap_email=None
        if str(ldap_pass)=="":
            ldap_pass=None

        if str(cse_email)=="":
            cse_email=None

        if str(cse_email_pass)=="":
            cse_email_pass=None

        if str(moodle_id)=="":
            moodle_id=None

        if str(moodle_pass)=="":
            moodle_pass=None

        data = {'name': name, 'mobile_no': mobile_no, 'ldap_email': ldap_email, 'ldap_pass': ldap_pass, 'cse_email':cse_email,'cse_email_pass':  cse_email_pass,'moodle_id':  moodle_id,'moodle_pass':  moodle_pass}


        users_serializer = usersSerializer(data=data)
        if users_serializer.is_valid():
            users_serializer.save()
            #return JsonResponse({'message': 'User has been registered successfully!'}, status=status.HTTP_201_CREATED,safe=False)

            return render(request, 'timer.html', {'message': {'k1':'User has been registered successfully!\n',
            'k2':'Please send \"join friend-identity\" (without quotes) to "+1 415 523-8886" to register to the whatsapp bot service. Then you can use the whatsapp bot as per your need.'}})
        else:
            #return JsonResponse(users_serializer.errors, status=status.HTTP_400_BAD_REQUEST, safe=False)

            return render(request, 'timer.html',{'message': {'k1':'HTTP_400_BAD_REQUEST: Please Try again!','k2':''}})

def update(request):
    # Get username and password and other credentials from posted data and updated into the db
    if request.method == 'POST':
        name = request.POST.get('name')
        code=  str(request.POST.get('countryCode'))
        mobile_no =code+ str(request.POST.get('mobile_no'))
        ldap_email = request.POST.get('ldap_email')
        ldap_pass = request.POST.get('ldap_pass')
        cse_email = request.POST.get('cse_email')
        cse_email_pass = request.POST.get('cse_email_pass')
        moodle_id = request.POST.get('moodle_id')
        moodle_pass = request.POST.get('moodle_pass')

        try:
            usr = Users(str(mobile_no))
            user = users.objects.get(pk=str(mobile_no))
            user_data = usr.getAll()

            if str(name) != "":
                user_data["name"] = name

            if str(ldap_email) != "":
                user_data["ldap_email"] = ldap_email

            if str(ldap_pass) != "":
                ldap_pass = str(encrypt_message(ldap_pass))
                user_data["ldap_pass"] = ldap_pass

            if str(cse_email) != "":
                user_data["cse_email"] = cse_email

            if str(cse_email_pass) != "":
                cse_email_pass = str(encrypt_message(cse_email_pass))
                user_data["cse_email_pass"] = cse_email_pass

            if str(moodle_id) != "":
                user_data["moodle_id"] = moodle_id

            if str(moodle_pass) != "":
                moodle_pass = str(encrypt_message(moodle_pass))
                user_data["moodle_pass"] = moodle_pass

            user_serializer = usersSerializer(user, data=user_data)
            if user_serializer.is_valid():
                user_serializer.save()
                #return JsonResponse({'message': 'User has been updated successfully!'}, status=status.HTTP_201_CREATED,safe=False)
                return render(request, 'timer.html', {'message': {'k1':'User has been updated successfully!\n ',
                'k2':'Please send \"join friend-identity\" (without quotes) to "+1 415 523-8886" to register to the whatsapp bot service. Then you can use the whatsapp bot as per your need.'}})
            else:
                #return JsonResponse(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST, safe=False)
                return render(request, 'timer.html', {'message': {'k1':'HTTP_400_BAD_REQUEST: Please Try again!','k2':''}})
        except users.DoesNotExist:
            #return JsonResponse({'message': 'The user does not exist'}, status=status.HTTP_404_NOT_FOUND, safe=False)
            return render(request, 'timer.html', {'message': {'k1':'The user does not exist','k2':''}})

def generate_key():
       """
       Generates a key and save it into a file
       """
       key = Fernet.generate_key()
       with open("secretkey.key", "wb") as key_file:
         key_file.write(key)



def load_key():
    """
    Load the previously generated key
    """
    return open("secretkey.key", "rb").read()
    #return 'oUM9KoViX9or94mAb8ENHXQyIHHRAsZApCYmTymBkpU='


def encrypt_message(message):
    """
    Encrypts a message
    """
    key = load_key()
    encoded_message = message.encode('utf-8')
    f = Fernet(key)
    encrypted_message = f.encrypt(encoded_message)

    return encrypted_message.decode()


def decrypt_message(encrypted_message):
    """
    Decrypts an encrypted message
    """
    key = load_key()
    f = Fernet(key)
    decrypted_message = f.decrypt(encrypted_message.encode())
    return decrypted_message.decode('utf-8')



