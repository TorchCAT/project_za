import os
from flask import Flask, flash, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
from cumspeech import cmspch

UPLOAD_FOLDER = 'uploads'


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['JSON_AS_ASCII'] = False

def allowed_file(filename: str):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == "ogg"

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'booze' not in request.files:
            return jsonify({"error":"poshel nahui"}), 200
        file = request.files['booze']
        if file.filename == '':
            return jsonify({"error":"poshel v pizdu"}), 200
        if file and allowed_file(file.filename):
            # filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], "speech.ogg"))
            txt = cmspch()
            return jsonify({"result":txt})
        return jsonify({"error":"hacker"}), 200
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=booze>
      <input type=submit value=Upload>
    </form>
    '''