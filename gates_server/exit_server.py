from flask import Flask, render_template, Response
import requests
import cv2
import time
import json

entry = False
gate_no = 1

video_capture = cv2.VideoCapture(0)

known_captured_index = []

process_frame = True

while True:
    if process_frame:
        ret, frame = video_capture.read()
        cv2.imwrite("exit_frame.jpg",frame)
        exit_res = requests.post("http://192.168.43.100:5001/process",files={"file":open('exit_frame.jpg','rb')})
        exit_res_json = json.loads(exit_res.text)
        try:
            if exit_res_json[0]:
                for data in exit_res_json:
                    if data["face_matched"] and data["index"]:
                        r = requests.get(f"http://192.168.43.100:5010/check-exit/{data['index']}/{entry}/{gate_no}")
                        if r.text == "True":
                            print(f"Bye {data['name']}")
                        else:
                            print(f"Bye Again {data['name']}")
                    # elif data["face_matched"] == False:
                        # print('Unknown')
        except:
            continue