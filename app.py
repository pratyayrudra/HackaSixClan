#Imports
import face_recognition
import cv2
import pickle
import pymongo
from flask import Flask 
  
# Flask constructor
app = Flask(__name__) 

#Connecting to mongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
#Connection to database
mydb = client["face-recognition"]

#Known people table
knowncol = mydb["known"]
#Unknown people table
unknowncol = mydb["unknown"]


if __name__ == '__main__': 
  
    app.run(debug=True)