from django.shortcuts import render , get_object_or_404
from django.http import HttpResponse
from django.contrib import sessions
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
import json

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
        try:
            user = authe.create_user_with_email_and_password(email, password)
            authe.send_email_verification(user['idToken'])
        except:
            return Response({"error":{"Code" : 400,"Content" : { "msg" : "Email already exists" }}}, status=status.HTTP_400_BAD_REQUEST)
    uid = user['localId']
    data = {"uid":uid,"email":email,"fname": fname, "lname": lname, "contactno": contactno, "company": company,"device":"null","device_type":"null"}
    result =db.child("users").child("user").child(uid).set(data)
    if(result):
          return Response({"success":{"Code" : 200,"Content" : { "msg" : "Successfully User Signup" }}},  status=status.HTTP_200_OK)
    else:
         return Response({"error":{"Code" : 400,"Content" : { "msg" : "Unable to Signup , Try Again!" }}}, status=status.HTTP_400_BAD_REQUEST)

# User Login Api
@api_view(['POST'])
# @permission_classes((IsAuthenticated, ))
def login(request):
    if request.method == 'POST':
        email = request.data['email']
        password = request.data['password']
        try:
           res = authe.sign_in_with_email_and_password(email, password)
        except:
             return Response({"error":{"Code" : 400,"Content" : { "msg" : "Invalid Credentials , Try Again" }}}, status=status.HTTP_400_BAD_REQUEST)
        if (res):
            userdet = authe.get_account_info(res['idToken'])
            userid = res['localId']
            email = userdet["users"][0]["email"]
            emailVerified = userdet["users"][0]['emailVerified']
            if(emailVerified  == True):
                    user = db.child("users").child("user").child(userid).get()
                    userjson = {
                                "uid": userid
                                }
                    return Response(userjson)
            else:
                return Response({"error":{"Code" : 400,"Content" : { "msg" : "Please verified your email and Login !" }}}, status=status.HTTP_400_BAD_REQUEST)
        else:
             return Response({"error":{"Code" : 400,"Content" : { "msg" : "No User Found!" }}}, status=status.HTTP_400_BAD_REQUEST)


# User Logout Api
@api_view(['GET'])
def logout(request):
    authe.logout(request)
    return Response({'message': 'Successfully Logout'}, status=status.HTTP_200_OK)


# get users by id
@api_view(['GET'])
def userbyid(request,userid):
    # user = authe.get_account_info(userid)
    user = db.child("users").child("user").child(userid).get()
    return Response(user.val())

#update User
@api_view(['PUT'])
def user_update(request,userid):
    if request.method == 'PUT':
        fname = request.data.get('fname')
        lname = request.data.get('lname')
        contactno = request.data.get('contactno')
        company = request.data.get('company')
        data = {"fname": fname, "lname": lname, "contactno": contactno, "company": company}
        db.child("users").child("user").child(userid).update(data)
        return Response({'message': 'User Updated Successfully !'}, status=status.HTTP_200_OK)


@api_view(['GET'])
def getproducts(request):
    if request.method =='GET':
        products = db.child("products").get()
        print(products.val())
        return Response(products.val())

@api_view(['POST'])
def reset_password(request):
    email = request.data.get('email')
    authe.send_password_reset_email(email)
    return Response({'message': 'Password Reset email sent !'}, status=status.HTTP_200_OK)


# Add Quote
@api_view(['POST'])
def add_quote(request,userid):
    if request.method == 'POST':
          data = request.data
          id = request.data.get('id')
          qoute = db.child("Quotes").child("Quote").child(userid).child(id).set(data)
          return Response({'message': ' Quote made successfully!'}, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_key(request):
    if request.method == 'GET':
       key = db.child("products").child("key").get()
       return Response(key.val())