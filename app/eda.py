import functools

from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
    jsonify,
    current_app,
    Response
)
import uuid
from flask_paginate import Pagination, get_page_parameter
from werkzeug.security import check_password_hash, generate_password_hash

from werkzeug.utils import secure_filename
from werkzeug.exceptions import abort

import pandas as pd
import numpy as np
import json
import zipfile
import os


import plotly

from datetime import datetime

# univariate lstm example
from numpy import array

bp = Blueprint('eda', __name__, url_prefix='/eda')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ['csv']
           
@bp.route('/', methods=['GET'])
def list_eda():
    list_file_name = []
    for _, _, files_list in os.walk(current_app.config['UPLOAD_FOLDER']):
        for file_name in files_list:
            if allowed_file(file_name):
                list_file_name.append(file_name)

    return render_template('eda/list.html', list_file_name=list_file_name)


@bp.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)

            if not os.path.exists(current_app.config['UPLOAD_FOLDER']):
                os.makedirs(current_app.config['UPLOAD_FOLDER'])

            file.save(os.path.join(
                current_app.config['UPLOAD_FOLDER'], filename))

            return redirect("/eda/")
    return redirect("/eda/")

@bp.route('/info', methods=['GET'])
def eda_info():
    return "hello world"




