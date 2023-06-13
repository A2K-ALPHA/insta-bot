import datetime, TimeHelper

from pyparsing import results
from DBHandler import *


def delete_user(username):
    mydb = DBHandler.get_mydb()
    collection = mydb.collection('followers')
    collection.document(username).delete
    


#add new username
def add_user(username):
    mydb = DBHandler.get_mydb()
    collection = mydb.collection('followers')
    now = datetime.datetime.now().date()
    res=collection.document(username).set({
        "username":username,
        "date_added":str(now)
        

    })


#check if any user qualifies to be unfollowed
def check_unfollow_list():
    mydb = DBHandler.get_mydb()
    results=[]
    all_users_ref_2 = mydb.collection("followers").stream()
    for users in all_users_ref_2:
        results.append(users.to_dict())
    users_to_unfollow = []
    print(results)
    for r in results:
        d = TimeHelper.days_since_date(r["date_added"])
        if d > Constants.DAYS_TO_UNFOLLOW:
            users_to_unfollow.append(r["username"])
    return users_to_unfollow


#get all followed users
def get_followed_users():
    users1 = []
    mydb = DBHandler.get_mydb()
    results=[]
    all_users_ref_2= mydb.collection("followers").stream()
    for users in all_users_ref_2:
        results.append(users.to_dict())
    
    print(results)
    for r in results:
        users1.append(r["username"])

    return users1
