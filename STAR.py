#! /usr/bin/env python3
"""
STAR python STIX runtime

Copyright 2020, Battelle Energy Alliance, LLC    ALL RIGHTS RESERVED
"""

__version__ = '1.0.0'

import json
import os
import sys

from tempfile import gettempdir
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename


# file upload options
UPLOAD_FOLDER = './'

# Flask setup
app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

HOST = '127.0.0.1'
PORT = 9001

COAs = []
indicators = []


@app.route('/', methods=['GET'])
def show_usage():
    """
    Main landing page for web api
    """
    resp = jsonify({'message' : 'place holder'})
    resp.status_code = 200
    return resp


@app.route('/stix-bundle', methods=['POST'])
def upload_file():
    """
    route for easily sending a stix bundle to be parsed for coas
    """
    global UPLOAD_FOLDER
    # check if the post request has the file part
    if 'file' not in request.files:
        resp = jsonify({'message' : 'No file param in request'})
        resp.status_code = 400
        return resp

    file = request.files['file']

    if file.filename == '':
        resp = jsonify({'message' : 'No file selected'})
        resp.status_code = 400
        return resp

    if file and str(file.filename).endswith('.json'):
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)

        # to ensure json format
        try:
            with open(file_path) as json_file:
                data = json.load(json_file)
        except Exception as e:
            print(e)
            resp = jsonify({'message' : 'invalid file submitted'})
            resp.status_code = 400
            return resp

        count = parse_coa(file_path)
        resp = jsonify({'message' : 'File uploaded,  added '+count+' COAs'})
        resp.status_code = 201
        return resp

    else:
        resp = jsonify({'message' : 'Please send JSON file'})
        resp.status_code = 400
        return resp


@app.route('/api/stix-object', methods=['POST'])
def upload_cyb_obs():
    """
    route for sending the cyber observables to trigger COAs
    """
    try:
        obs = request.json
        if len(COAs) > 0:
            run_coa()
            resp = jsonify({'message' : 'received observable, running COAs'})
            resp.status_code = 200
            return resp
        else:
            resp = jsonify({'message' : 'No cyber observable sent'})
            resp.status_code = 400
            return resp

    except Exception as e:
        print(e)
        resp = jsonify({'message' : 'No cyber observable sent'})
        resp.status_code = 400
        return resp


def check_obs(json_obs):

    return


def parse_coa(json_file):
    """
    will parse COA type objects from
    STIX bundles and store them in list
    """
    global COAs
    count = 0

    with open(json_file) as file:
        data = json.load(file)
        for obj in data['objects']:
            try:
                if obj['type'] == 'course-of-action':
                    COAs.append(obj)
                    count += 1
            except:
                continue
    return str(count)


def run_coa():
    """
    limited to python COAs
    """
    global COAs

    for coa in COAs:

        # TODO: implement email functionality
        if coa['action'] == 'email-message':
            continue

        # Parses python and runs created /tmp/<obj uuid>.py file
        elif 'python' in coa['action']:
            run_python_coa(coa['action']['python'], str(coa['id']).split('--')[1])

        elif coa['action'] is None:
            continue


def run_python_coa(coa, uuid):
    """
    attempts to write code block to python file and import and run

    deletes file afterwards
    """
    func_name = coa['funcname']
    code = coa['code']

    temp = gettempdir()
    filename = str(temp) + '/' + uuid
    sys.path.append(temp)

    fp = open(filename+'.py', 'w')
    fp.write(code)
    fp.close()

    module = __import__(uuid)

    getattr(module, func_name)()


def main():
    global COAs

    if len(sys.argv) == 2:
        # provide command line arg to just run coas for testing
        json_file = sys.argv[1]

    else:
        print("no arg given starting webserver")

        print("Running on http://"+HOST+":"+str(PORT))
        app.run(host=HOST, port=PORT)
        sys.exit(0)

    count = parse_coa(json_file)
    print(count)
    run_coa()


if __name__ == '__main__':
    main()
