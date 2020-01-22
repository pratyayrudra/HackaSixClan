import face_recognition
from flask import Flask, jsonify, request, redirect
import pickle
# You can change this to any folder on your system
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/add', methods=['POST'])
def upload_data():
    # Check if a valid image file was uploaded
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']
        name = request.form['name']

        if file.filename == '' and name == '':
            return redirect(request.url)

        if file and name:
            # The image file seems valid! Detect faces and return the result.
            return add_new_face(file,name)

@app.route('/process', methods=['POST'])
def upload_image():
    # Check if a valid image file was uploaded
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            return redirect(request.url)

        if file:
            # The image file seems valid! Detect faces and return the result.
            return detect_faces_in_image(file)

def add_new_face(image,name):
    img = face_recognition.load_image_file(image)
    # Get face encodings for any faces in the uploaded image
    unknown_face_locations = face_recognition.face_locations(img)
    unknown_face_encodings = face_recognition.face_encodings(img,unknown_face_locations)

    known_encodings = pickle.load(open('known_encodings.pickle','rb'))
    known_names = pickle.load(open('known_names.pickle','rb'))

    known_encodings.append(unknown_face_encodings[0])
    known_names.append(name)

    pickle.dump(known_encodings,open('known_encodings.pickle','wb'))
    pickle.dump(known_names,open('known_names.pickle','wb'))

    return jsonify({"success":True,"id":known_names.index(name)})

def detect_faces_in_image(file_stream):
    known_encodings = pickle.load(open('known_encodings.pickle','rb'))
    known_names = pickle.load(open('known_names.pickle','rb'))
    # Load the uploaded image file
    img = face_recognition.load_image_file(file_stream)
    # Get face encodings for any faces in the uploaded image
    unknown_face_locations = face_recognition.face_locations(img)
    unknown_face_encodings = face_recognition.face_encodings(img,unknown_face_locations)

    results = []

    for (face_encoding,face_location) in zip(unknown_face_encodings,unknown_face_locations):
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(known_encodings, face_encoding)
        index = -1
        name = ""
        found = False
        location = face_location
        # # If a match was found in known_face_encodings, just use the first one.
        if True in matches:
            first_match_index = matches.index(True)
            name = known_names[first_match_index]
            found = True
            index = matches.index(True)

        result = {
            "face_matched": found,
            "name": name,
            "location": location,
            "index": index
        }
        results.append(result)
    
    return jsonify(results)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)