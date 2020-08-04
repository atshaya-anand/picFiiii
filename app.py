from flask import Flask, render_template, request
import flask
app = Flask(__name__)

@app.route("/")
def Welcome():
    return render_template("index.html")

@app.route('/imageFilters/',methods=['GET','POST'])
def upload():
    imagefile = flask.request.files.get('file') 
    print(imagefile)    
    return render_template("filters.html",user_image = imagefile) 


if __name__ == '__main__':
    app.run(host="127.0.0.1",port=5000,debug=True,use_reloader=True)
