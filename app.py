from flask import Flask, render_template,request, redirect, send_from_directory, flash,url_for
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = "./upload"
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def Welcome():
    return render_template("index.html")

@app.route("/confirmimage",methods=["GET", "POST"])
def redirect_page():
	#print("inside confirm :::")
	return render_template("Manipulator.html")

@app.route("/upload",methods=["GET", "POST"])
def upload_img():
    print("inside:")
    if request.method == "POST":
       if 'file' not in request.files:
           print('No file part')
           return redirect(request.url)
       file = request.files['file']
       if file.filename == '':
           print('No image selected for uploading')
           return redirect(request.url)
       if file and allowed_file(file.filename):
           filename = secure_filename(file.filename)
           file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
           print('Image successfully uploaded and displayed')
           return redirect(url_for('display_image', filename=filename))
       else:
           print('Allowed image types are -> png, jpg, jpeg, gif')
           return redirect(request.url)

@app.route('/display/<filename>')
def display_image(filename):
    print('display_image filename: ' + filename)
    return render_template('index.html', filename=filename)

@app.route('/uploads/<filename>')
def send_file(filename):
    print('inside filename: ' + filename)
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(host="127.0.0.1",port=5000,debug=True,use_reloader=True)
