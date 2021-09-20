from flask import Blueprint, request, jsonify
from api.importing_dxf.dxf_to_json import dxf_to_json
import os

import_blueprint = Blueprint('import', "import")
export_blueprint = Blueprint('export', "export")

@import_blueprint.route('/data/import', methods=['POST'])
def retrieve_file():
    f = request.files['file']
    print(f)
    f.save(f.filename)

    # if not f:
    response_object = {
        'status': 'error',
        'message': 'Invalid payload.'
    }
    output_code = 415

    try:
        output_json = dxf_to_json(f.filename)

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
            'geometry_fata': jsonify({}),
        }
        output_code = 400

    # removing the imported file after handling
    os.remove(f.filename)

    return jsonify(response_object), output_code