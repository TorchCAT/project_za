import os
from flask import Flask, request, jsonify
from cumspeech import cmspch
import requests

UPLOAD_FOLDER = 'uploads'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['JSON_AS_ASCII'] = False

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    def allowed_file(filename: str):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() == "ogg"
    if request.method == 'POST':
        if 'booze' not in request.files:
            return jsonify({"error":"poshel nahui"}), 501
        file = request.files['booze']
        if file.filename == '':
            return jsonify({"error":"poshel v pizdu"}), 502
        if file and allowed_file(file.filename):
            input_path = os.path.join(app.config['UPLOAD_FOLDER'], "speech_input.webm")
            out_path = os.path.join(app.config['UPLOAD_FOLDER'], "speech.ogg")
            file.save(input_path)
            # os.system(f'mkvextract {filepath} tracks --raw 0:speech.ogg')
            requests.post('http://converter:4000/ffmpeg', json={'args': ['-i', input_path, '-c:a', 'libopus', out_path]})
            txt = cmspch()
            return jsonify({"result":txt})
        return jsonify({"error":"hacker"}), 503
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=booze>
      <input type=submit value=Upload>
    </form>
    '''