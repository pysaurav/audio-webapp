import datetime
import json
import os
import requests
from flask import Flask,render_template, redirect, request,flash, url_for, session,escape, abort
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.config['SECRET_KEY'] = 'hallucination'
app.config['UPLOAD_EXTENSIONS'] = ['.wav', '.mp3', '.mp4','.ogg']
app.config['UPLOAD_PATH'] = os.path.join(os.getcwd(),'static')

@app.route('/', methods=['GET','POST'])
def home():
   
    available_files = os.listdir(os.path.join(app.config['UPLOAD_PATH']))
    print(available_files)
    audio_files = [item for item in available_files if item.split(".")[-1] in ['wav','mp3','mp4','ogg']]
    print(audio_files)
    return render_template('home.html',to_play = audio_files[:-1], to_populate= audio_files )
   

@app.route('/about', methods=['GET','POST'])
def about():
    
    return render_template('about.html')

@app.route("/audioinput", methods=["GET", "POST"])
def audioinput():

    if request.method == "GET":
        return render_template("about.html")
    else:
        print("POST",request.files)
        audio_file = request.files['audiofile']
        print(audio_file)
        filename = secure_filename(audio_file.filename)
        print("filename",filename)
        available_directory=os.listdir(os.getcwd())
        if 'uploads' not in available_directory:
            os.mkdir(os.path.join(os.getcwd(),'static','uploads'))
        if filename != '':
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in app.config['UPLOAD_EXTENSIONS']:
                abort(400)
            audio_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
        return render_template("home.html")

@app.route('/playaudio', methods=['GET','POST'])
def playaudio():
   
    available_files = os.listdir(os.path.join(app.config['UPLOAD_PATH']))
    audio_files = [item for item in available_files if item.split(".")[-1] in ['wav','mp3','mp4','ogg']]
    selected = request.form["dropdown"]
    return render_template('home.html',to_play = [selected],  to_populate= audio_files )


app.run(debug=True,host='127.0.0.1', port=5000)
# app.run(debug=True,host='127.0.0.1', port=7050)
