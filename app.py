from flask import Flask,render_template,request
from distance_live import distanceLive
from distance import distanceWebcam
app=Flask(__name__)

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

