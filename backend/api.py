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
            return Response({'message': 'Unable create user , Try Again!'}, status=status.HTTP_200_OK)
    uid = user['localId']
    data = {"email":email,"fname": fname, "lname": lname, "contactno": contactno, "company": company}
    result =db.child("users").child(uid).set(data)
    if(result):
        return Response({'message': 'Successfully User Signup'}, status=status.HTTP_200_OK)
    else:
        return Response({'message': 'Unable to Signup , Try Again!'}, status=status.HTTP_200_OK)

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
            return Response({'message': 'Invalid Credentials , Try Again'}, status=status.HTTP_200_OK)
        if (res):
            userdet = authe.get_account_info(res['idToken'])
            userid = res['localId']
            # email = res['email']
            email = userdet["users"][0]["email"]
            emailVerified = userdet["users"][0]['emailVerified']
            if(emailVerified  == True):
                    user = db.child("users").child(userid).get()
                    userdata = user.val()
                    fname = userdata['fname']
                    lname = userdata['lname']
                    contact = userdata['contactno']
                    company = userdata['company']
                    role = userdata['role']
                    userjson = {
                                "fname": fname ,
                                "lname": lname,
                                "email" : email,
                              # " emailVerified" :emailVerified,
                                "contactno": contact,
                                "company": company,
                                }
                    return Response(userjson)
            else:
                return Response({'message': 'Please verified your email and Login !'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'No User Found!'}, status=status.HTTP_200_OK)


# User Logout Api
@api_view(['GET'])
def logout(request):
    authe.logout(request)
    return Response({'message': 'Successfully Logout'}, status=status.HTTP_200_OK)


# get users by id
@api_view(['GET'])
def userbyid(request,userid):
    # user = authe.get_account_info(userid)
    user = db.child("users").child(userid).get()
    return Response(user.val())

#update User
@api_view(['PUT','GET'])
def user_update(request,userid):
    try:
        user = db.child("users").child(userid).get()
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'PUT':
        email = request.data.get('email')
        fname = request.data.get('fname')
        lname = request.data.get('lname')
        contactno = request.data.get('contactno')
        company = request.data.get('company')
        # authe.sign_in_with_email_and_password(email, password)
        authe.updateEmail(email)
        data = {"email": email,"fname": fname, "lname": lname, "contactno": contactno, "company": company}
        db.child("users").child(userid).update(data)
    elif request.method =='GET':
        user = db.child("users").child(userid).get()
        return Response(user.val())

# Add Products
@api_view(['POST'])
def add_products(request):
    if request.method == 'POST':
        prod_id = request.data.get('prod_id')
        prod_type = request.data.get('prod_type')
        name_val = request.data.get('name_val')
        name_sta = request.data.get('name_sta')
        reinforcement_val = request.data.get('reinforcement_val')
        reinforcement_sta = request.data.get('reinforcement_sta')
        system_val = request.data.get('system_val')
        system_sta = request.data.get('system_sta')
        install_method_val = request.data.get('install_method_val')
        install_method_sta = request.data.get('install_method_sta')
        penetrations_val = request.data.get('penetrations_val')
        penetrations_sta = request.data.get('penetrations_sta')
        base_val = request.data.get('base_sta')
        base_sta = request.data.get('base_sta')
        termination_val = request.data.get('termination_val')
        termination_sta = request.data.get('termination_sta')
        finish_coat_val = request.data.get('finish_coat_val')
        finish_coat_sta = request.data.get('finish_coat_sta')
        qty_val = request.data.get('qty_val')
        qty_sta = request.data.get('qty_sta')
        coverage_val = request.data.get('coverage_val')
        coverage_sta = request.data.get('coverage_sta')
        type_val = request.data.get('type_val')
        type_sta = request.data.get('type_sta')
        primer_val = request.data.get('primer_val')
        primer_sta = request.data.get('primer_sta')
        asphaltic_val = request.data.get('asphaltic_val')
        asphaltic_sta = request.data.get('asphaltic_sta')
        aluminum_coat_val = request.data.get('aluminum_coat_val')
        aluminum_coat_sta = request.data.get('aluminum_coat_sta')
        adhesive_val = request.data.get('adhesive_val')
        adhesive_sta = request.data.get('adhesive_sta')
        name = {"name_val": name_val,"name_sta":name_sta}
        reinforcement = {"reinforcement_val": reinforcement_val,"reinforcement_sta":reinforcement_sta}
        system = {"system_val": system_val,"system_sta":system_sta}
        install = {"install_method_val": install_method_val,"install_method_sta":install_method_sta}
        base = {"base_val": base_val,"base_sta":base_sta}
        penetrations = {"penetrations_val": penetrations_val,"penetrations_sta":penetrations_sta}
        termination = {"termination_val": termination_val,"termination_sta":termination_sta}
        finish_coat = {"finish_coat_val": finish_coat_val,"finish_coat_sta":finish_coat_sta}
        qty = {"qty_val": qty_val,"qty_sta":qty_sta}
        coverage = {"coverage_val": coverage_val,"coverage_sta":coverage_sta}
        type = {"type_val": type_val,"type_sta":type_sta}
        primer = {"primer_val": primer_val,"primer_sta":primer_sta}
        asphaltic = {"asphaltic_val": asphaltic_val,"asphaltic_sta":asphaltic_sta}
        aluminum_coat = {"aluminum_coat_val": aluminum_coat_val,"aluminum_coat_sta":aluminum_coat_sta}
        adhesive = {"adhesive_val": adhesive_val,"adhesive_sta":adhesive_sta}
    try:
        db.child("products").child(prod_type).child(prod_id).child("name").set(name)
        db.child("products").child(prod_type).child(prod_id).child("reinforcement").set(reinforcement)
        db.child("products").child(prod_type).child(prod_id).child("system").set(system)
        db.child("products").child(prod_type).child(prod_id).child("install_method").set(install)
        db.child("products").child(prod_type).child(prod_id).child("base").set(base)
        db.child("products").child(prod_type).child(prod_id).child("penetrations").set(penetrations)
        db.child("products").child(prod_type).child(prod_id).child("termination").set(termination)
        db.child("products").child(prod_type).child(prod_id).child("finish_coat").set(finish_coat)
        db.child("products").child(prod_type).child(prod_id).child("qty").set(qty)
        db.child("products").child(prod_type).child(prod_id).child("coverage").set(coverage)
        db.child("products").child(prod_type).child(prod_id).child("type").set(type)
        db.child("products").child(prod_type).child(prod_id).child("primer").set(primer)
        db.child("products").child(prod_type).child(prod_id).child("asphaltic").set(asphaltic)
        db.child("products").child(prod_type).child(prod_id).child("aluminum_coat").set(aluminum_coat)
        db.child("products").child(prod_type).child(prod_id).child("adhesive").set(adhesive)
        return Response({'message': 'Products added Successfully!'}, status=status.HTTP_200_OK)
    except:
       return Response({'message': ' Products not save, Try Again!'}, status=status.HTTP_200_OK)

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
