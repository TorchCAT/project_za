import os
from flask import Flask, request, jsonify, send_from_directory
from cumspeech import cmspch
import requests

UPLOAD_FOLDER = 'uploads'

requests_speech = 0
requests_main = 0
requests_speech_success = 0

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['JSON_AS_ASCII'] = False
app.config['PAGES'] = 'pages'


@app.route('/', methods=["GET"])
def index():
    global requests_main
    requests_main = requests_main+1
    return send_from_directory(app.config['PAGES'], "index.html")


@app.route('/speech', methods=['POST'])
def upload_file():
    global requests_speech, requests_speech_success
    requests_speech = requests_speech+1
    def allowed_file(filename: str):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() == "ogg"
    if 'booze' not in request.files:
        return jsonify({"error": "poshel nahui"}), 501
    file = request.files['booze']
    if file.filename == '':
        return jsonify({"error": "poshel v pizdu"}), 502
    if file and allowed_file(file.filename):
        input_path = os.path.join(
            app.config['UPLOAD_FOLDER'], "speech_input.webm")
        out_path = os.path.join(app.config['UPLOAD_FOLDER'], "speech.ogg")
        file.save(input_path)
        # os.system(f'mkvextract {filepath} tracks --raw 0:speech.ogg')
        requests.post('http://converter:4000/ffmpeg',
                      json={'args': ['-y', '-i', input_path, '-c:a', 'libopus', out_path]})
        txt = cmspch()
        requests_speech_success += 1
        return jsonify(txt)
    return jsonify({"error": "hacker"}), 503


@app.route('/_next/<path:next>', methods=['GET'])
def pizdaebanaja(next):
    print(next)
    return send_from_directory(app.config['PAGES'], '_next/' + next)
    # return '''
    # <!doctype html>
    # <title>Upload new File</title>
    # <h1>Upload new File</h1>
    # <form method=post enctype=multipart/form-data>
    #   <input type=file name=booze>
    #   <input type=submit value=Upload>
    # </form>
    # '''


@app.route('/metrics', methods=["GET"])
def metrics():
    return f"""
# TYPE projectza_requests counter
projectza_requests_failed{{endpoint="/speech",success="0"}} {requests_speech-requests_speech_success}
projectza_requests{{endpoint="/speech",success="1"}} {requests_speech_success}
projectza_requests{{endpoint="/"}} {requests_main}
"""
    # return jsonify({"requests_main": requests_main, "requests_speech": requests_speech, "requests_speech_success": requests_speech_success}), 200
