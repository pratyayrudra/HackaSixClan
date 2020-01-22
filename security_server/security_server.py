from flask import Flask, jsonify, request, redirect, url_for, render_template
import requests
import cv2
import time
import json
import database as db
import random
app = Flask(__name__)

entered_indexes = []
unknown_detected = []

@app.route('/index')
def index():
    return render_template('index.html', entered=len(entered_indexes), unknown_detected=len(unknown_detected))

@app.route('/entry/<index>/<entry>/<gate>',methods=['GET'])
def new_entry(index,entry,gate):
    entered_indexes.append(index)
    db.insert_log(index,entry,gate)
    return index

@app.route('/exit/<index>/<entry>/<gate>')
def exit_entry(index,entry,gate):
    entered_indexes.remove(index)
    db.exit_log(index,entry,gate)
    return index

@app.route('/check-entry/<index>/<entry>/<gate>')
def check_entry(index,entry,gate):
    if index not in entered_indexes:
        i = new_entry(index,entry,gate)
        return "True"
    else:
        return "False"

@app.route('/check-exit/<index>/<entry>/<gate>')
def check_exit(index,entry,gate):
    if index in entered_indexes:
        i = exit_entry(index,entry,gate)
        return "True"
    else:
        return "False"

@app.route('/new-user/<gate>',methods=['POST'])
def add_user(gate):
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)

        if file and gate not in unknown_detected:
            # The image file seems valid! Detect faces and return the result.
            print(f"Unknown at gate {gate}")
            unknown_detected.append(gate)
            file.save(f"Unknown-{gate}.jpg")
            data = {
                "gate": gate,
                "image": f"Unknown-{gate}.jpg"
            }
            db.add_unknown_user(data)
            return "Unknown User"
        else:
            return "Wait for registration"

def delete_unknown(gate):
    unknown_detected.remove(gate)
    data = {
        "gate": gate,
        "image": f"Unknown-{gate}.jpg"
    }
    db.delete_unknown_user(data)

@app.route('/add-new-user',methods=['POST'])
def add_new_user():
    name = request.form.get('name')
    gate = request.form.get('gate')
    res = requests.post("http://192.168.43.100:5001/add",files={"file":open(f"Unknown-{gate}.jpg",'rb')},data={"name":name})
    res_json = json.loads(res.text)
    # user = {
    #     "name": name,
    #     "index": res_json['id']
    # }
    # db.add_known_user(user)
    delete_unknown(gate)
    return res.text

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True,port=5010)