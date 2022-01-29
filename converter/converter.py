# web imports
import os
from flask import Flask, request

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.route('/<command>', methods=['POST'])
def run(command):
    args = request.json.get('args', [])
    os.system(" ".join([command, *args]))
    # ffmpeg -i /uploads/speech_input.webm -c:a libopus /uploads/speech.ogg
    return "done"
