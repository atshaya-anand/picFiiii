from flask import Flask, render_template, request, jsonify
import flask
from PIL import Image
import os , io , sys
import numpy as np 
import cv2
import base64
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


imageData = []

@app.route("/")
def Welcome():
    return render_template("index.html")

@app.route('/imageFilters/',methods=['GET','POST'])
def upload():
    global imageData
    imagefile = flask.request.files.get('file') 
    imageData = imagefile.read()
    #print(imageData,"file data")    
    return render_template("filters.html",user_image = imagefile) 

@app.route('/maskImage' , methods=['POST'])
def mask_image():
    #file = request.files['image'].read()
    global imageData
    npimg = np.frombuffer(imageData, np.uint8)
    img = cv2.imdecode(npimg,cv2.IMREAD_COLOR)
    img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    #print("runnnnnnnnnnn")
    img = Image.fromarray(img.astype("uint8"))
    rawBytes = io.BytesIO()
    img.save(rawBytes,"JPEG")
    rawBytes.seek(0)
    img_base64 = base64.b64encode(rawBytes.read())
    return jsonify({'status':str(img_base64)})



if __name__ == '__main__':
    app.run(host="127.0.0.1",port=5000,debug=True,use_reloader=True)
