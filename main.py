import os
from flask import Flask, request, jsonify, send_from_directory
from prometheus_flask_exporter import PrometheusMetrics
from cumspeech import cmspch
import requests

UPLOAD_FOLDER = 'uploads'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['JSON_AS_ASCII'] = False
app.config['PAGES'] = 'pages'
metrics = PrometheusMetrics(app)


@app.route('/', methods=["GET"])
def index():
    return send_from_directory(app.config['PAGES'], "index.html")


@app.route('/speech', methods=['POST'])
def upload_file():
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
        return jsonify(txt)
    return jsonify({"error": "hacker"}), 503


@app.route('/_next/<path:next>', methods=['GET'])
def nexty(next):
    print(next)
    return send_from_directory(app.config['PAGES'], '_next/' + next)