#!/usr/bin/env python
# -*- coding: utf-8 -*-

# https://blog.miguelgrinberg.com/post/handling-file-uploads-with-flask

import os
from flask import Flask, render_template, request, redirect, url_for, abort
from werkzeug.utils import secure_filename

from logging.config import dictConfig

from parse.classes import OutMsg 
from parse.parse_tarefas import *

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
app.config['MAX_CONTENT_LENGTH'] = 70 * 1000 * 1024
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

        task_id = int(request.form['task'])
        app.logger.debug('task id: %d', task_id)

        output_parser=OutMsg()
        output_parser=parse_aia_file(filename=save_filename, task_id=task_id)
        app.logger.debug('success: %d, fail: %d', len(output_parser.success), len(output_parser.fail))
        return render_template('output.html', output=output_parser)
    return redirect(url_for('index'))

def parse_aia_file(filename, task_id=2):
    outmsg = OutMsg()
    outmsg.success.clear()
    outmsg.fail.clear()
    if task_id == 2:
        outmsg = parse_tarefa2(filename)
    elif task_id == 3:
        outmsg = parse_tarefa3(filename)
    elif task_id == 4:
        outmsg = parse_tarefa4(filename)
    else:
        outmsg.fail.append(':construction:    Não sei avaliar ainda')
    return outmsg
