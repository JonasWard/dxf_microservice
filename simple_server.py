import json
import os
import time

from flask import Flask, request, send_from_directory, Response, jsonify
from test_functions import multi_threaded_stress_test
import api.importing_dxf.dxf_to_json
import api.importing_dxf.dxf_parsers

valid_response = Response()
valid_response.status_code = 200

invalid_response = Response()
invalid_response.status_code = 500

app = Flask(__name__)


@app.route("/")
def home():
    return """Hello world!\nI do work!"""


@app.route("/data/list")
def test_data_list():
    files = []
    file_dir = "./test_data"

    # r=root, d=directories, f = files
    for r, d, f in os.walk(file_dir):
        for file in f:
            if '.dxf' in file:
                files.append(os.path.join(r, file))

    return '\n'.join(files)


@app.route("/data/stress_test")
def stress_test():
    global HOST, PORT
    return multi_threaded_stress_test("./test_data/dxf", "./stress_testing_output/dxf", HOST, PORT)


@app.route("/dxf_to_json", methods=['GET', 'POST'])
def dxf_to_json():
    start_time = time.time()
    f = request.files['file']
    print(f)
    f.save(f.filename)

    response_object = {
        'status': 'error',
        'message': 'Invalid payload.'
    }
    output_code = 415

    try:
        output_json = api.importing_dxf.dxf_to_json.dxf_to_json(f.filename)

        response_object = {
            'status': 'success',
            'message': 'Successfully registered.',
            'geometry_data': output_json,
        }
        output_code = 201



    # handler errors
    except:
        response_object = {
            'status': 'error',
            'message': 'Failed to convert this dxf file',
            'geometry_data': {},
        }
        output_code = 400

    # removing the imported file after handling
    os.remove(f.filename)

    if output_code == 201:
        print("converted {} to json in {} seconds".format(
            f.filename, time.time() - start_time))
    else:
        print("failed to convert {} to json in {} seconds".format(
            f.filename, time.time() - start_time))

    return jsonify(response_object), output_code


@app.route("/json_to_dxf", methods=['GET', 'POST'])
def json_to_dxf():
    start_time = time.time()
    f = request.files['file']
    f.save(f.filename)

    # if not f:
    response_object = {
        'status': 'error',
        'message': 'Invalid payload.'
    }
    output_code = 415

    # # with open(f.filename, 'r') as a_json:
    # this_context = json.load(f)
    # # pass

    try:
        file_name, output_dxf = api.importing_dxf.dxf_parsers.json_to_dxf(f.filename)

        response_object = {
            'status': 'success',
            'message': 'Successfully registered.',
            'dxf_content': str(output_dxf),
            'dxf_name': file_name
        }
        output_code = 201

    # handler errors
    except:
        response_object = {
            'status': 'error',
            'message': 'Failed to convert this json file',
            'dxf_content': {},
            'dxf_name': None
        }
        output_code = 400

    if output_code == 201:
        print("converted {} to dxf in {} seconds".format(
            f.filename, time.time() - start_time))
    else:
        print("failed to convert {} to dxf in {} seconds".format(
            f.filename, time.time() - start_time))

    os.remove(f.filename)

    return jsonify(response_object), output_code


@app.route("/dxf_to_json/with_ui", methods=['GET', 'POST'])
def dxf_to_json_ui():
    global HOST, PORT
    return """<html>
       <body>
          <form action = "http://""" + str(HOST) + ':' + str(PORT) + """/dxf_to_json" method = "POST" 
             enctype = "multipart/form-data">
             <input type = "file" name = "file" />
             <input type = "submit"/>
          </form>   
       </body>
    </html>"""


@app.route("/json_to_dxf/with_ui", methods=['GET', 'POST'])
def json_to_dxf_ui():
    global HOST, PORT
    return """<html>
       <body>
          <form action = "http://""" + str(HOST) + ':' + str(PORT) + """/json_to_dxf" method = "POST" 
             enctype = "multipart/form-data">
             <input type = "file" name = "file" />
             <input type = "submit"/>
          </form>   
       </body>
    </html>"""


if __name__ == "__main__":
    global HOST, PORT

    HOST="0.0.0.0"
    PORT=1337

    print("I started a server")

    app.run(host=HOST, port=PORT, debug=True)

