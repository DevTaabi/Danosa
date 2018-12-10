from django.shortcuts import render , get_object_or_404
from django.http import HttpResponse
from django.contrib import sessions
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import os.path
from firebase_admin import auth
from firebase_admin import messaging

import datetime
import uuid
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
    except:
         return Response({'message': 'User Not Found!'}, status=status.HTTP_200_OK)
    userr = db.child("users").child("user").child(uid).get()
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
        "device": userdata['device']
    }
    return Response(userjson)

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
     data = {"uid": uid, "email": email, "fname": fname, "lname": lname, "contactno": contactno, "company": company}
     result = db.child("users").child("user").child(uid).set(data)
     if (result):
         return Response({'message': 'Successfully Added User'}, status=status.HTTP_200_OK)
     else:
         return Response({'message': 'Unable to add user, Try Again!'}, status=status.HTTP_200_OK)

#update User
@api_view(['PUT'])
def update_user(request,uid):
    try:
        user = db.child("users").child("user").child(uid).get()
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'PUT':
        email = request.data.get('email')
        fname = request.data.get('fname')
        lname = request.data.get('lname')
        contactno = request.data.get('contactno')
        company = request.data.get('company')
        auth.update_user(uid,email=email)
        data = {"email":email,"fname": fname, "lname": lname, "contactno": contactno, "company": company}
        db.child("users").child("user").child(uid).update(data)
        return Response({'message': 'User updated Successfully!'}, status=status.HTTP_200_OK)

#delete users by id
@api_view(['GET'])
def del_user(request,uid):
        db.child("users").child("user").child(uid).remove()
        auth.delete_user(uid)
        return Response({'message': 'User deleted Successfully!'}, status=status.HTTP_200_OK)

#display all users
@api_view(['GET'])
def all_users(request):
    # users = db.child("users").order_by_child("role").equal_to(0).get()
    users = db.child("users").get()
    return Response(users.val())

# Add Products
@api_view(['POST'])
def add_products(request):
    if request.method == 'POST':
        pid = request.data.get('id')
        prod_type = request.data.get('prod_type')
        name = request.data.get('name')
        reinforcement = request.data.get('reinforcement')
        system = request.data.get('system')
        install_method = request.data.get('install_method')
        penetrations= request.data.get('penetrations')
        base = request.data.get('base')
        termination= request.data.get('termination')
        qty = request.data.get('qty')
        coverage= request.data.get('coverage')
        type= request.data.get('type')
        primer= request.data.get('primer')
        asphaltic_mass = request.data.get('asphaltic_mass')
        aluminum_coat = request.data.get('aluminum_coat')
        adhesive = request.data.get('adhesive')
        pdf = request.data.get('pdf')
        val1 = request.data.get('val1')
        val2 = request.data.get('val2')
        if(val1 != "null" and val2 != "null"):
            finish_coat = {"val1":val1, "val2":val2}

        elif(val1 != "null" and val2 == "null"):
            finish_coat = {"val1":val1}

        else:
            finish_coat = {"val1":"null"}
        data = {"id":pid,
                "name_val": name,
                "reinforcement": reinforcement,
                "system": system,
                "install_method": install_method,
                "base": base,
                "penetrations": penetrations,
                "termination": termination,
                "finish_coat": finish_coat,
                "qty": qty,
                "coverage": coverage,
                "type": type,
                "category": prod_type,
                "pdf": pdf ,
               "complement": {
                             "primer": primer,
                             "asphaltic_mass": asphaltic_mass,
                             "aluminum_coat": aluminum_coat,
                              "adhesive": adhesive,
                             }
                }

    try:
        db.child("products").child("product").child(prod_type).child(pid).set(data)
        key = uuid.uuid4().hex[:6].upper()
        data = {"updated_key":key}
        db.child("products").child("key").set(data)
        return Response({'message': 'Products added Successfully!'}, status=status.HTTP_200_OK)
    except:
       return Response({'message': ' Products not save, Try Again!'}, status=status.HTTP_200_OK)

@api_view(['GET'])
def getproducts(request):
    if request.method =='GET':
        products = db.child("products").get()
        return Response(products.val())

#get product by id
@api_view(['GET'])
def productbyid(request,type,id):
    product = db.child("products").child("product").child(type).child(id).get()
    return Response(product.val())


#get product by type
@api_view(['GET'])
def productbytype(request,type):
    product = db.child("products").child("product").child(type).get()
    return Response(product.val())

#update Products
@api_view(['PUT','GET'])
def updateproduct(request,typ,id):
    if request.method == 'PUT':
        name = request.data.get('name')
        reinforcement = request.data.get('reinforcement')
        system = request.data.get('system')
        install_method = request.data.get('install_method')
        penetrations = request.data.get('penetrations')
        base = request.data.get('base')
        termination = request.data.get('termination')
        qty = request.data.get('qty')
        coverage = request.data.get('coverage')
        type = request.data.get('type')
        primer = request.data.get('primer')
        asphaltic_mass = request.data.get('asphaltic_mass')
        aluminum_coat = request.data.get('aluminum_coat')
        adhesive = request.data.get('adhesive')
        pdf = request.data.get('pdf')
        val1 = request.data.get('val1')
        val2 = request.data.get('val2')
        if(val1 != "null" and val2 != "null"):
            finish_coat = {"val1":val1, "val2":val2}

        elif(val1 != "null" and val2 == "null"):
            finish_coat = {"val1":val1}

        else:
            finish_coat = {"val1":"null"}
        data = {
                "id":id,
                "name_val": name,
                "reinforcement": reinforcement,
                "system": system,
                "install_method": install_method,
                "base": base,
                "penetrations": penetrations,
                "termination": termination,
                "finish_coat": finish_coat,
                "qty": qty,
                "coverage": coverage,
                "type": type,
                "category":typ,
                "pdf":pdf,
                "complement": {
                    "primer": primer,
                    "asphaltic_mass": asphaltic_mass,
                    "aluminum_coat": aluminum_coat,
                    "adhesive": adhesive,
                }
                }
        db.child("products").child("product").child(typ).child(id).update(data)
        key = uuid.uuid4().hex[:6].upper()
        data = {"updated_key":key}
        db.child("products").child("key").set(data)
    return Response({'message': 'Product Successfully!'}, status=status.HTTP_200_OK)

#delete product
@api_view(['GET'])
def delproduct(request,type,id):
        db.child("products").child("product").child(type).child(id).remove()
        key = uuid.uuid4().hex[:6].upper()
        data = {"updated_key":key}
        db.child("products").child("key").set(data)
        return Response({'message': 'Product deleted Successfully!'}, status=status.HTTP_200_OK)

#Get all qoutations
@api_view(['GET'])
def all_quotes(request):
    if request.method == 'GET':
        qoutations = db.child("Quotes").get()
        return Response(qoutations.val())



#Get qoutations by userid
@api_view(['GET'])
def quote_by_userid(request,userid):
    if request.method == 'GET':
        qoutations = db.child("Quotes").child("Quote").child(userid).get()
        return Response(qoutations.val())


#Send Notify
@api_view(['POST'])
def sendnotify(request):
   if request.method == 'POST':
    title = request.data.get('title')
    body = request.data.get('body')
    device = request.data.get('device')
    device_type = request.data.get('device_type')
    registration_token = device
    if(device_type == "android"):
      message = messaging.Message(
            android=messaging.AndroidConfig(
                ttl=datetime.timedelta(seconds=3600),
                priority='high',
                notification=messaging.AndroidNotification(
                    title=title,
                    body=body,
                    sound="default",
                ),
            ),
            token=registration_token,
        )
      messaging.send(message)
    else:
        message = messaging.Message(
            apns=messaging.APNSConfig(
                headers={'apns-priority': '10'},
                payload=messaging.APNSPayload(
                    aps=messaging.Aps(
                        alert=messaging.ApsAlert(
                            title=title,
                            body=body,
                            sound="default",
                        ),
                        badge=42,
                    ),
                ),
            ),
            token=registration_token,
        )
        messaging.send(message)

    return Response({'message': 'Notification sent Successfully!'}, status=status.HTTP_200_OK)



# update Token
@api_view(['PUT'])
def update_token(request,userid):
   if request.method == 'PUT':
     fcm_token = request.data.get('fcm_token')
     device_type= request.data.get('device_type')
     data = {"device": fcm_token, "device_type":device_type}
     db.child("users").child("user").child(userid).update(data)
     if(device_type == "android"):
         topic = 'users'
     else:
         topic = 'ios_users'
     registration_tokens = [fcm_token]
     messaging.subscribe_to_topic(registration_tokens, topic)
     return Response({'message': 'Token Updated !'}, status=status.HTTP_200_OK)


#Send Notify to all
@api_view(['POST'])
def sendnotify_to_all(request):
    title = request.data.get('title')
    body = request.data.get('body')
    android = 'users'
    message = messaging.Message(
        android=messaging.AndroidConfig(
            ttl=datetime.timedelta(seconds=3600),
            priority='high',
            notification=messaging.AndroidNotification(
                title=title,
                body=body,
                sound="default",
            ),
        ),
        topic=android,
    )
    result = messaging.send(message)
    ios = 'ios_users'
    message = messaging.Message(
        apns=messaging.APNSConfig(
            headers={'apns-priority': '10'},
            payload=messaging.APNSPayload(
                aps=messaging.Aps(
                    alert=messaging.ApsAlert(
                        title=title,
                        body=body,
                    ),
                    badge=42,
                ),
            ),
        ),
        topic=ios,
    )
    messaging.send(message)
    return Response({'message': 'Notification sent Successfully'}, status=status.HTTP_200_OK)

#del qoute
@api_view(['GET'])
def del_quote(request,userid,id):
    db.child("Quotes").child("Quote").child(userid).child(id).remove()
    return Response({'message': 'Quote deleted Successfully!'}, status=status.HTTP_200_OK)



#update User
@api_view(['PUT'])
def update_note(request,userid,id):
     if request.method == 'PUT':
        note = request.data.get('note')
        data = {"note":note}
        db.child("Quotes").child("Quote").child(userid).child(id).update(data)
        return Response({'message': 'User updated Successfully!'}, status=status.HTTP_200_OK)

@api_view(['GET'])
def qoutes_notify(request):
    notifications = db.child("notifications").get()
    return Response(notifications.val())








