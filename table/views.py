import time
import os
import json

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf
import pyrebase

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect

from table.models import Test


def Table(request):
    list = Test.objects.all()
    hello = tf.constant('Hello, TensorFlow!')
    sess = tf.Session()
    tensor = str(sess.run(hello))
    print (list)
    return render(request, 'pages/table/table.html', {'list': list, 'tensor': tensor})


def UpdateDB(response):
    if response['path'] == "/":
        return False
    if response['data'] == None:
        return False
    try:
        Test.createTest(response['data']['name'])
    except:
        return False


def FirebaseObserver():
    config = {
        "apiKey": "AIzaSyC9ZZrzdQi6ZhT3WkcfG_yiHpDv5-I4M2o",
        "authDomain": "test-861de.firebaseapp.com",
        "databaseURL": "https://test-861de.firebaseio.com/",
        "storageBucket": "test-861de.appspot.com"
    }

    firebase = pyrebase.initialize_app(config)
    db = firebase.database()
    db.child("user").stream(UpdateDB)


FirebaseObserver()