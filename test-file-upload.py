#!/usr/bin/env python
# -*- coding: utf-8 -*-

# https://blog.miguelgrinberg.com/post/handling-file-uploads-with-flask

import os
from flask import Flask, render_template, request, redirect, url_for, abort
from werkzeug.utils import secure_filename

from logging.config import dictConfig

from parseaia import Project

import emoji

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})
    
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 10 * 1000 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.aia']
app.config['UPLOAD_PATH'] = 'uploads'

@app.template_filter('emojify')
def emoji_filter(s):
    return emoji.emojize(s)

@app.route('/')
def index():
    return render_template('file-upload.html')

@app.errorhandler(413)
def too_large(e):
    return "File is too large", 413

@app.route('/', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS']:
            return "Invalid file format", 400        
        app.logger.info('%s submitted succesfully', filename)
        save_filename = os.path.join(app.config['UPLOAD_PATH'], filename)
        uploaded_file.save(save_filename)
        app.logger.debug('%s saved', save_filename)
        output_parser=parse_aia_file(save_filename)
        return render_template('output.html', msg=output_parser)
    return redirect(url_for('index'))

def parse_aia_file(filename):
    mp = Project(filename)
    app.logger.info("Avaliando arquivo %s", filename)

    # Check number of screens
    if (len(mp.screens) == 1):
        app.logger.info("OK  : Tem uma tela")
        return(':check_mark_button:    Tem uma tela')
    else:
        app.logger.info("FAIL: Número de telas não é um")
        return(':cross_mark:    Número de telas não é um :red_exclamation_mark:')

