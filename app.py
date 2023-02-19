from flask import Flask, request, jsonify
import os
from sustainabilty import *
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'image'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400
    image = request.files['image']
    if image.filename == '':
        return jsonify({'error': 'No image selected'}), 400
    filename = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
    image.save(filename)

    resp = get_sustainability_score("image/" + image.filename)
    return jsonify(resp), 200

@app.route('/ping')
def ping():
    return "pong"

if __name__ == "__main__":
    app.run()