import os
from urllib.parse import urlparse
from uuid import uuid4
import requests
from flask import Flask, request, render_template, redirect, url_for, flash
from werkzeug.utils import secure_filename
import HighResST
import Colorization
app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
sourcename = ''
stylename = ''
@app.route('/')
def index():
    return render_template('./index.HTML')
@app.route('/stylize', methods = ['GET', 'POST'])
def get_img():
    if request.method == 'POST':
        if 'source' not in request.files:
            print('No file part')
            return redirect(request.url)
        if 'style' not in request.files:
            print('No file part')
            return redirect(request.url)
        source = request.files['source']
        style = request.files['style']
        if style.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if source.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if source:
            global sourcename
            sourcename, extension1 = os.path.splitext(source.filename)
            source.save(os.path.join(app.config['UPLOAD_FOLDER'], 'source.png'))
        if style:
            global stylename
            stylename, extension2 = os.path.splitext(style.filename)
            style.save(os.path.join(app.config['UPLOAD_FOLDER'], 'style.png'))
        HighResST.styleTransfer(extension1,extension2)
        render_template('./styletransfer.HTML')
    return render_template('./styletransfer.HTML')
@app.route('/colorize', methods = ['GET', 'POST'])
def get_img_color():
    if request.method == 'POST':
        if 'source' not in request.files:
            print('No file part')
            return redirect(request.url)
        source = request.files['source']
        if source.filename == '':
            print('No selected file')
            return redirect(request.url)
        if source:
            global sourcename
            sourcename, extension1 = os.path.splitext(source.filename)
            source.save(os.path.join(app.config['UPLOAD_FOLDER'], 'source.png'))
        Colorization.color()
        render_template('./colorization.HTML')
    return render_template('./colorization.HTML')
app.run(port = 5000)