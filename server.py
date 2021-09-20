# -*- coding: utf-8 -*-
"""
dxf to json microservice
"""

import socketserver
from api.importing_dxf.dxf_to_json import dxf_to_json
from communication_codes import *


class TCPHandler(socketserver.BaseRequestHandler):
    """ Class for handling TCP Requests

    This Class handles every tcp request from Client
    https://docs.python.org/3/library/socketserver.html
    """

    HANDLE_MAP = {
        IMPORT_DXF:     "import_dxf",
        IMPORT_HCD_DXF: "import_hcd_dxf",
        EXPORT_DXF:     "export_dxf",
        EXPORT_HCD_DXF: "export_hcd_dxf"
    }

    def __init__(self, request, client_address, server):
        super().__init__(request, client_address, server)

        version = "0.1"

    def _sending_data(self, file_name):
        pass

    def _receiving_data(self, file_name):
        received = str(self.recv(1024), "utf-8")

    def import_dxf(self, file_name):
        dxf_to_json(file_name)
        return

    def import_hcd_dxf(self, file_name):
        dxf_to_json(file_name)
        return 0, None

    def send_response(self, command_id, output_json):
        print("[INFO] Command ", command_id)
        self.request.sendall(output_json.encode())

    def export_dxf(self, _):
        output_json = self.create_output_json(KEEP_ALIVE, NO_ERROR)
        self.send_response(KEEP_ALIVE, output_json)

    def export_hcd_dxf(self, json_dict):
        self.send_response(NEW_PROJECT, output_json)