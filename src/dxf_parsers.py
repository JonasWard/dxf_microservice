
import json, ezdxf
import os
import traceback

from ezdxf.document import Drawing
from ezdxf.layouts import Modelspace

# from geometry json to dxf using ezdxf

# json parsers

def opening_json(json_file: str) -> list:
    with open(json_file, 'r') as f:
        jsn = json.load(f)
    return jsn


def json_to_dxf(json_file: str):
    doc = parse_json(json_file)

    dxf_file = os.path.splitext(json_file)[0] + "_export.dxf"
    doc.saveas(dxf_file)


def parse_json(json_file: str) -> Drawing:
    obj_list = opening_json(json_file)

    doc = ezdxf.new('R2007')
    msp = doc.modelspace()

    for obj in obj_list:
        try:
            parse_map[obj["type"]](msp, obj)
        except:
            traceback.print_exc()
            print(obj)

    return doc


def parse_point(msp: Modelspace, obj : dict):
    msp.add_point(obj["vertices"][0], dxfattribs={
        'layer': obj['layer']
    })


def parse_point_collection(msp: Modelspace, obj : dict):
    for pt in obj["vertices"]:
        msp.add_point(obj["vertices"][0], dxfattribs={
        'layer': obj['layer']
    })


def parse_stamp(msp: Modelspace, obj : dict):
    msp.add_circle(obj["vertices"][0], obj["radius"])


def parse_polygon(msp: Modelspace, obj : dict):
    pl = msp.add_polyline2d(obj["vertices"], dxfattribs={
        'layer': obj['layer']
    })

    pl.close()


def parse_polyline(msp: Modelspace, obj : dict):
    if len(obj["vertices"]) == 2:
        start, end = obj["vertices"]
        msp.add_line(start=start, end=end, dxfattribs={
        'layer': obj['layer']
    })
    elif len(obj["vertices"]) > 2:
        msp.add_polyline2d(obj["vertices"], dxfattribs={
        'layer': obj['layer']
    })
    elif len(obj["vertices"]) == 1:
        msp.add_point(obj["vertices"][0], dxfattribs={
        'layer': obj['layer']
    })
    else:
        print("zero length polyline")


def parse_network(msp: Modelspace, obj : dict):
    pass


def parse_snake(msp: Modelspace, obj : dict):
    pass


def parse_block(msp: Modelspace, obj : dict):
    pass


parse_map = {
    "POINTCOLLECTION"   : parse_point_collection,
    "POINT"             : parse_point,
    "POLYLINE"          : parse_polyline,
    "POLYGON"           : parse_polygon,
    "RECTANGLE"         : parse_polygon,
    "STAMP"             : parse_stamp,
    "SNAKE"             : parse_snake,
    "NETWORK"           : parse_network,
    "BLOCK"             : parse_block,
    "NGS"               : parse_block
}


if __name__ == "__main__":
    src_path = "./test_data/"
    # pth = src_path + "circle_line_pl.json"
    path_list = list(os.listdir("./test_data/"))

    for pth in path_list:
        file_extension = os.path.splitext(pth)[1][1:]
        if file_extension == 'json':
            json_to_dxf(src_path+pth)