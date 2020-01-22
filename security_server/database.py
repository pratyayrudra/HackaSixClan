from pymongo import MongoClient
import datetime

db = None
log = None

client = MongoClient('mongodb://192.168.43.100:27017')
    
db = client["face_recognition"]
log = db["log"]
user = db["user"]
unknown = db["unknown"]

print("Database Started")

#Log
def insert_log(data,action,gate):
    temp = {
        "registered": True,
        "index": data,
        "time": datetime.datetime.now(),
        "entry": action,
        "gate": gate,
        "done": False
    }
    x = log.insert_one(temp)
    print("[DATABASE] Person Entry")

def exit_log(data,action,gate):
    temp = {
        "registered": True,
        "index": data,
        "time": datetime.datetime.now(),
        "entry": action,
        "gate": gate,
        "done": True
    }
    x = log.insert_one(temp)
    print("[DATABASE] Person exit")

def update_log(index,name):
    query = {"name":name,"index":index}
    update = { "$set": {"done": True}}
    log.update_one(query,update)

def check_log(index,action,done):
    query = {"index":index, "entry": action,"done":done}
    data = log.find(query)
    print("[DATABASE] Person Check")
    if data[0]:
        print("Inside")
        return True
    else:
        print("Outside")
        return False

#user
def add_unknown_user(data):
    unknown.insert_one(data)
    print("[DATABASE] Unknown User created")

def delete_unknown_user(data):
    unknown.delete_one(data)
    print("[DATABASE] Unknown user deleted")

def add_known_user(data):
    user.insert_one(data)
    print("[DATABASE] New user created")