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
from werkzeug.utils import secure_filename

import pandas as pd
import numpy as np
import json
import os
import plotly

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


def get_employee_in_department_chart(df):
    xValue = list(df['department'].value_counts().index)
    yValue = list(df['department'].value_counts())

    trace1 = dict(
        x=xValue,
        y=yValue,
        type='bar',
        textposition='auto'
    )

    data = [trace1]

    layout = dict(
        title= 'January 2013 Sales Report',
        barmode= 'stack'
    )

    chart = json.dumps(dict(
        data=data,
        layout=layout
    ), cls=plotly.utils.PlotlyJSONEncoder)
    print("Ccc: ", chart)

    return chart

@bp.route('/info', methods=['GET'])
def eda_info():
    file_name = request.args.get('file_name')
    df = pd.read_csv(os.path.join(
        current_app.config['UPLOAD_FOLDER'], file_name))

    df = df.head(n=200)

    rows = df.to_dict(orient='records')
    column_names = list(df.columns)

    # Preprocess data:
    # RENAME column sale to department
    df.rename(columns={'sales': 'department'}, inplace=True)

    # Convert salary variable type to numeric
    df['salary'] = df['salary'].map({'low': 1, 'medium': 2, 'high': 3})

    return render_template('eda/charts.html',
                           file_name=file_name,
                           rows=rows,
                           column_headers=column_names,
                           employee_in_department_chart=get_employee_in_department_chart(df))
