import Constants
import firebase_admin
from firebase_admin import credentials
from google.cloud import firestore
import os
credential_path = "battle-43d91-firebase-adminsdk-yrqa4-09a62d5071.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path
cred = credentials.Certificate("battle-43d91-firebase-adminsdk-yrqa4-09a62d5071.json")
firebase_admin.initialize_app(cred)

firebaseConfig = {
  "apiKey": "AIzaSyALhtPCdlinDUTY3s6qqks2o_-arvuGDvo",
  "authDomain": "battle-43d91.firebaseapp.com",
  "databaseURL": "https://battle-43d91-default-rtdb.firebaseio.com",
  "projectId": "battle-43d91",
  "storageBucket": "battle-43d91.appspot.com",
  "messagingSenderId": "997153207623",
  "appId": "1:997153207623:web:3b2884420a3cf908270862",
  "measurementId": "G-JY8D52F5XK"
}
class DBHandler:
    def __init__(self):
        pass
    @staticmethod
    def get_mydb():
        

        db = DBHandler()
        mydb = db.connect()
        return mydb

    def connect(self):
        try:
            
            db=firestore.Client()
            print("hello")
            return db
        except Exception as e:
            print(e)
