from firebase import firebase
import pyrebase
from django.shortcuts import render, redirect

from commerce.models import Category, Item

# get remote FB Application
firebased = firebase.FirebaseApplication('https://vaportalk-6725e.firebaseio.com', authentication=None)


# delete FB object
def deleteFBObj(child, key):
    firebased.delete("child", key)


# Callback function for Observer
def UpdateUserDB(response):
    if response['path'] == "/":
        return False
    if response['data'] == None:
        return False
    return False


# Callback function for Observer
def UpdateCommerceDB(response):
    # hi = firebased.get('/commerceData', '-KkyZdmsWarwzarFeLJ1')
    # print(hi['commerceAnalysis'])
    # print(hi['content'])
    # print(hi['distance'])
    # print(hi['hostName'])

    if response['data'] == None:
        return False
    elif response['data'] == True:
        commerceKey = response['path'].replace("/", "")
        commerceObj = firebased.get('/commerceData', commerceKey)
        ## Create object
        ## firebased.delete("/completedCommerces/", commerceKey)
    else:
        return False


# FB DB Observer
def FirebaseObserver():
    config = {
        "apiKey": "AIzaSyDigu179_TBrh8xU7C_ZgJypnpOKYxggFc",
        "authDomain": "vaportalk-6725e.firebaseapp.com",
        "databaseURL": "https://vaportalk-6725e.firebaseio.com/",
        "storageBucket": "vaportalk-6725e.appspot.com"
    }

    pyrebased = pyrebase.initialize_app(config)
    db = pyrebased.database()
    db.child("completedCommerces").stream(UpdateCommerceDB)


# Django - background must need linker view
def Linker(request):
    return render(request)


# Attach to FB with django Observer
FirebaseObserver()