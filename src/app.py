from flask import Flask,render_template,request
from detection.distance_live import distanceLive
from detection.distance import distanceWebcam
import os
# Get the project root directory (parent of src/)
os.environ['TF_ENABLE_ONEDNN_OPTS'] = os.getenv('TF_ENABLE_ONEDNN_OPTS', '0')
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


app=Flask(__name__,
          template_folder=os.path.join(ROOT_DIR, 'templates'),
          static_folder=os.path.join(ROOT_DIR, 'static'))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/webcam")
def webcam():
    distanceLive()
    return('',204)

@app.route("/video")
def video():
    output=request.args.get("path")
    distanceWebcam(output)
    return('',204)

if __name__ == '__main__':
    app.run(debug=True,port=1080)

