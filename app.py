from flask import Flask, render_template

app = Flask(__name__)

@app.route("/",methods=['GET','POST'])
def Welcome():
    return render_template("index.html")

def upload():
    imagefile = flask.request.files.get('upfile', '') 
    print(imagefile)     


if __name__ == '__main__':
    app.run(host="127.0.0.1",port=5000,debug=True,use_reloader=True)
