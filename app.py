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


imageData = [] #image variable to hold the user selecte image

@app.route("/")
def Welcome():
    return render_template("index.html")


@app.route('/imageFilters',methods=['GET','POST'])
def upload():
    global imageData
    imagefile = flask.request.files.get('file') 
    image = imagefile.read()
    npimg = np.frombuffer(image, np.uint8)
    img = cv2.imdecode(npimg,cv2.IMREAD_COLOR)
    imageData = cv2.cvtColor(img,cv2.COLOR_BGR2RGB) 
    return render_template("filters.html") 


@app.route('/applyBasics',methods=['GET','POST'])
def applyBasics():
    global imageData
    if request.method == "POST":
        filter = request.data.decode('UTF-8')
        print(filter)
        img = Image.fromarray(imageData.astype("uint8"))
        rawBytes = io.BytesIO()
        img.save(rawBytes,"JPEG")
        rawBytes.seek(0)
        img_base64 = base64.b64encode(rawBytes.read())
        return jsonify({'status':str(img_base64)})


@app.route('/maskImage' , methods=['POST'])
def mask_image():
    global imageData
    #imageData = np.array(imageData)
    img = Image.fromarray(imageData.astype("uint8"))
    rawBytes = io.BytesIO()
    img.save(rawBytes,"JPEG")
    rawBytes.seek(0)
    img_base64 = base64.b64encode(rawBytes.read())
    return jsonify({'status':str(img_base64)})



if __name__ == '__main__':
    app.run(host="127.0.0.1",port=5000,debug=True,use_reloader=True)
