import requests
import cv2
import time
import json

entry = True
gate_no = 1

video_capture = cv2.VideoCapture(0)

process_frame = True

while True:
    if process_frame:
        ret, frame = video_capture.read()
        cv2.imwrite("entry_frame.jpg",frame)
        entry_res = requests.post("http://192.168.43.100:5001/process",files={"file":open('entry_frame.jpg','rb')})
        entry_res_json = json.loads(entry_res.text)
        try:
            if entry_res_json[0]:
                for data in entry_res_json:
                    if data["face_matched"] and data["index"]:
                        r = requests.get(f"http://192.168.43.100:5010/check-entry/{data['index']}/{entry}/{gate_no}")
                        if r.text == "True":
                            print(f"Welcome {data['name']}")
                        else:
                            print(f"Welcome Back {data['name']}")
                    elif data["face_matched"] == False:
                        r = requests.post(f"http://192.168.43.100:5010/new-user/{gate_no}",files={"file":open('entry_frame.jpg','rb')}) 
                        print("Unknown")
        except:
            continue
