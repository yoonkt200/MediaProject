import time
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf

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


# def FirebaseObserver():
    # while True:
    #     time.sleep(5)
    #     print ("hello world")
    # hello = tf.constant('Hello, TensorFlow!')
    # sess = tf.Session()
    # print(sess.run(hello))


# FirebaseObserver()