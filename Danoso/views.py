from django.shortcuts import render , get_object_or_404
from django.http import HttpResponse
from django.contrib import sessions
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User

import pyrebase

config = {
    "apiKey": "AIzaSyD0OCk7jM9iw-EWekxwrupBtkj-JjuUiMU",
    "authDomain": "danoso-49851.firebaseapp.com",
    "databaseURL": "https://danoso-49851.firebaseio.com",
    "projectId": "danoso-49851",
    "storageBucket": "danoso-49851.appspot.com",
    "messagingSenderId": "390406362382"
}
firebase = pyrebase.initialize_app(config)

authe = firebase.auth()
db = firebase.database()

# User SignUp Api
@api_view(['POST'])
def signup(request):
    if request.method == 'POST':
        fname = request.data.get('fname')
        lname = request.data.get('lname')
        contactno = request.data.get('contactno')
        company = request.data.get('company')
        email = request.data.get('email')
        password = request.data.get('password')
        return HttpResponse(request.data.get)
    #     print(fname)
    #     try:
    #         user = authe.create_user_with_email_and_password(email, password)
    #         print(user)
    #     except:
    #         return Response({'message': 'Unable create user , Try Again!'}, status=status.HTTP_200_OK)
    # 
    # uid = user['localId']
    # data = {"fname": fname, "lname": lname, "contactno": contactno, "company": company, "status": "0", "role": "0","lastlogin": "null"}
    # result =db.child("users").child(uid).set(data)
    # if(result):
    #     return Response({'message': 'Successfully User Signup'}, status=status.HTTP_200_OK)
    # else:
    #     return Response({'message': 'Unable to Signup , Try Again!'}, status=status.HTTP_200_OK)

# User Login Api
@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        email = request.data['email']
        password = request.data['password']
        try:
            user = authe.sign_in_with_email_and_password(email, password)

            if (user):
                return Response({'message': 'Successfully Login'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Username or Password are wrong'}, status=status.HTTP_200_OK)
        except:
            return Response({'message': 'Username or Password are wrong'}, status=status.HTTP_200_OK)

# User Logout Api
@api_view(['GET'])
def logout(request):
    authe.logout(request)
    return Response({'message': 'Successfully Logout'}, status=status.HTTP_200_OK)

@api_view(['GET'])
def viewUsers(requrest):
    users = db.child("users").get()
    return Response(users.val())


