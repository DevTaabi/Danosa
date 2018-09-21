from django.shortcuts import render , get_object_or_404
from django.http import HttpResponse
from django.contrib import sessions
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
import json
import os.path
from firebase_admin import auth

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


import firebase_admin
from firebase_admin import credentials

basedir = os.path.abspath(os.path.dirname(__file__))
data_json = basedir+'/cred.json'

cred = credentials.Certificate(data_json)
default_app = firebase_admin.initialize_app(cred)

def index(request):
   # auth.set_custom_user_claims("CsHjMBKBEfhXjwc7oHDopTizzVg1", {'admin': True})
    return HttpResponse("working fine")

@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        email = request.data['email']
        password = request.data['password']
        try:
            res = authe.sign_in_with_email_and_password(email, password)
        except:
          return Response({'message': 'Invalid Credentials , Try Again'}, status=status.HTTP_200_OK)
    claims = auth.verify_id_token(res['idToken'])
    if claims['admin'] is True:
        user = authe.get_account_info(res['idToken'])
        return Response(user)
    else:
        return Response({'message': 'Invalid Credentials , Try Again'}, status=status.HTTP_200_OK)

#get users by id
@api_view(['GET'])
def userbyid(request,uid):
    try:
            user = auth.get_user(uid)
            userr = db.child("users").child(uid).get()
            userdata = userr.val()
            userid = format(user.uid)
            email = format(user.email)
            userjson = {
                        "uid": userid,
                         "fname": userdata['fname'],
                         "lname": userdata['lname'],
                         "email": email,
                         "contactno": userdata['contactno'],
                         "company": userdata['company'],
                         "role": userdata['role']
                          }
            return Response(userjson)
    except:
         return Response({'message': 'User Not Found!'}, status=status.HTTP_200_OK)

@api_view(['POST'])
def add_user(request):
    if request.method == 'POST':
     fname = request.data.get('fname')
     lname = request.data.get('lname')
     contactno = request.data.get('contactno')
     company = request.data.get('company')
     email = request.data.get('email')
     password = request.data.get('password')
     user = auth.create_user(
        email=email,
        email_verified=False,
        password=password,
        disabled=False)
     uid = format(user.uid)
     data = {"fname": fname, "lname": lname, "contactno": contactno, "company": company, "status": "0", "role": "0",
            "lastlogin": "null"}
     result = db.child("users").child(uid).set(data)
     print('Sucessfully created new user: {0}'.format(user.uid))
     if (result):
         return Response({'message': 'Successfully Added User'}, status=status.HTTP_200_OK)
     else:
         return Response({'message': 'Unable to add user, Try Again!'}, status=status.HTTP_200_OK)

#update User
@api_view(['PUT','GET'])
def update_user(request,uid):
    try:
        user = db.child("users").child(uid).get()
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'PUT':
        email = request.data.get('email')
        fname = request.data.get('fname')
        lname = request.data.get('lname')
        contactno = request.data.get('contactno')
        company = request.data.get('company')
        auth.update_user(uid,email=email,disabled=True)
        data = {"email":email,"fname": fname, "lname": lname, "contactno": contactno, "company": company}
        db.child("users").child(uid).update(data)
    elif request.method =='GET':
        use = auth.get_user(uid)
        userr = db.child("users").child(uid).get()
        userdata = userr.val()
        userid = format(use.uid)
        email = format(use.email)
        user = {
            "uid": userid,
            "fname": userdata['fname'],
            "lname": userdata['lname'],
            "email": email,
            "contactno": userdata['contactno'],
            "company": userdata['company']
        }
        return Response(user)

#delete users by id
@api_view(['GET'])
def del_user(request,uid):
        db.child("users").child(uid).remove()
        auth.delete_user(uid)
        return Response({'message': 'User deleted Successfully!'}, status=status.HTTP_200_OK)

#display all users
@api_view(['GET'])
def all_users(request):
    # users = db.child("users").order_by_child("role").equal_to(0).get()
    users = db.child("users").get()
    return Response(users.val())