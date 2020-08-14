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
appliedFilterdata = [] #image variable to hold the  filter

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
    global imageData,appliedFilterdata
    if request.method == "POST":
        filter = request.form['basic']
        if filter == 'Sharpen':
            kernal = np.array([[0,-1,0],[-1,5,-1],[0,-1,0]])
            sharpened_img = cv2.filter2D(imageData,-1,kernal)
            appliedFilterdata = sharpened_img
            return render_template("output.html")
        elif filter == 'Blur':
            kernal = np.array([[0.0625,0.125,0.0625],[0.125,0.25,0.125],[0.0625,0.125,0.0625]])
            blurred_img = cv2.filter2D(imageData,-1,kernal)
            appliedFilterdata = blurred_img
            return render_template("output.html")
        elif filter == 'Outline':
            kernal = np.array([[-1,-1,-1],[-1,8,-1],[-1,-1,-1]])
            outlined_img = cv2.filter2D(imageData,-1,kernal)
            appliedFilterdata = outlined_img
            return render_template("output.html")
        elif filter == 'Emboss':
            kernal = np.array([[-2,-1,0],[-1,1,1],[0,1,2]])
            embossed_img = cv2.filter2D(imageData,-1,kernal)
            appliedFilterdata = embossed_img
            return render_template("output.html")
        elif filter == 'Custom':
            kernal = np.array([[0,0,0],[0,1,0],[0,0,0]])
            custom_img = cv2.filter2D(imageData,-1,kernal)
            appliedFilterdata = custom_img
            return render_template("output.html")
        elif filter == 'Black & White':
            gray_img = cv2.cvtColor(imageData,cv2.COLOR_RGB2GRAY)
            appliedFilterdata = gray_img
            return render_template("output.html")

@app.route('/applyAdvance',methods=['GET','POST'])
def applyAdvance():
    global imageData,appliedFilterdata
    if request.method == "POST":
        filter = request.form['advance']
        if filter == 'Cartoonification':
            cartoon_image = cv2.stylization(imageData, sigma_s=150, sigma_r=0.25)  
            appliedFilterdata = cartoon_image
            return render_template("output.html")
        if filter == 'Pencil Sketch':
            dst_gray, dst_color = cv2.pencilSketch(imageData, sigma_s=60, sigma_r=0.07, shade_factor=0.05)   
            appliedFilterdata = dst_gray
            return render_template("output.html")
        if filter == 'Coloured Pencil Sketch':
            dst_gray, dst_color = cv2.pencilSketch(imageData, sigma_s=60, sigma_r=0.07, shade_factor=0.05)   
            appliedFilterdata = dst_color
            return render_template("output.html")
        if filter == 'Oil Paint':
            dst = cv2.xphoto.oilPainting(imageData, 7, 1)
            appliedFilterdata = dst
            return render_template("output.html")
        if filter == 'Water Colour':
            res = cv2.stylization(imageData, sigma_s=60, sigma_r=0.6)
            appliedFilterdata = res
            return render_template("output.html")

        
@app.route('/backTofilters',methods=['GET'])
def redirectTofilter():
    return render_template("filters.html")


@app.route('/filterImage' , methods=['POST'])
def render_image():
    global appliedFilterdata
    #imageData = np.array(imageData)
    img = Image.fromarray(appliedFilterdata.astype("uint8"))
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
