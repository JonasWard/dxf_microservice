import json, ezdxf
import math
import os
import traceback

from ezdxf.entities import Spline
from ezdxf.layouts import Modelspace
from ezdxf.entities.dxfgfx import DXFGraphic
from ezdxf.math import Vec3

# from dxf to geometry json using ezdxf

# DXF parsers

# data in geotype
object_prototype = {
    "vertices": [],
    "name": None,
    "type": "STAMP",
    "reference_objects": None,
    "radius": None,
    "invalidities": [],
    "uuid": None,
    "layer": "0",
    "connections": None
}

# just for reference: the geom types in the geo library
geom_types = [
    "NONE",
    "POINTCOLLECTION",  # point collection
    "POINT",            # standard point
    "POLYLINE",         # open polyline
    "POLYGON",          # closed polyline
    "RECTANGLE",        # same as polygon, yet rectangle
    "STAMP",            # centroid based: location with a radius or a polygon
    "SNAKE",            # (open) polyline which is buffered
    "NETWORK",          # multilinestring that represents a connected graph, otherwise the same as the snake type
    "BLOCK",            # centroid based: bbox rectangle with a name
    "NGS",              # nested geometry structure: data container with polygon, can also contain multiple other NGSs
]


def new_object(geom_type: str, layer_name: str = None, uuid: str = None) -> dict:
    """Method that create a new object based of the prototype dictionary
    input:
        layer_name : string (default: None) - if input invalid sets layer to 'default'
        uuid :       string (default: None)
    return:
        new_object dict"""

    n_dict = dict(object_prototype)
    if layer_name is None or not(isinstance(layer_name, str)):
        n_dict["layer"] = "default"
    else:
        n_dict["layer"] = layer_name

    n_dict["type"] = geom_type
    n_dict["uuid"] = uuid

    return n_dict


def parse_vertices(vs) -> list:
    """function that unpacks list of vertices"""
    v_unpacked = []

    if isinstance(vs, list):
        for v in vs:
            v_unpacked.extend(parse_vertices(v))
    elif isinstance(vs, Vec3):
        v_unpacked.append([vs.x, vs.y])
    elif vs.DXFTYPE == 'VERTEX' or vs.DXFTYPE == 'POINT':
        v_unpacked.append([vs.dxf.location.x, vs.dxf.location.y])
    else:
        print("Vertex of type: {}".format(type(vs)))

    return v_unpacked


def parse_point(pt) -> dict:
    loc_obj = new_object('POINT', pt.dxf.layer, str(pt.uuid))
    loc_obj["vertices"]=parse_vertices(pt)
    return loc_obj


def parse_circle(c) -> dict:
    loc_obj = new_object('STAMP', c.dxf.layer, str(c.uuid))
    loc_obj["vertices"] = parse_vertices(c.dxf.center)
    loc_obj["radius"] = c.dxf.radius
    return loc_obj


def parse_line(ln) -> dict:
    loc_obj = new_object('POLYLINE', ln.dxf.layer, str(ln.uuid))
    loc_obj["vertices"] = parse_vertices([ln.dxf.start, ln.dxf.end])
    return loc_obj


def parse_polyline(pl) -> dict:
    closed = False
    if pl.is_closed:
        loc_obj = new_object('POLYGON', pl.dxf.layer, str(pl.uuid))
    else:
        loc_obj = new_object('POLYLINE', pl.dxf.layer, str(pl.uuid))

    loc_obj["vertices"] = parse_vertices(pl.vertices)
    return loc_obj


def parse_blocks(blcks: list) -> list:
    block_list = {}

    for insert in blcks:
        try:
            block_list[insert.dxf.name]["vertices"].extend(parse_vertices(insert.dxf.insert))
        except:
            loc_obj = new_object('BLOCK', insert.dxf.layer, str(insert.uuid))
            loc_obj["name"] = insert.dxf.name
            loc_obj["vertices"] = parse_vertices(insert.dxf.insert)
            block = insert.doc.blocks.get(insert.dxf.name)
            loc_geometries = list(insert.virtual_entities())

            loc_obj["geometries"] = deconstruct_entity_list(loc_geometries)

            block_list[loc_obj["name"]] = loc_obj
    return list(block_list.values())


def parse_spline(spl) -> dict:
    correction_tolerance = .1

    if spl.dxf.dxftype == 'SPLINE':
        vs = list(spl.flattening(correction_tolerance, 1))
    else:
        vs = []

    if spl.closed:
        loc_obj = new_object('POLYGON', spl.dxf.layer, str(spl.uuid))
    else:
        loc_obj = new_object('POLYLINE', spl.dxf.layer, str(spl.uuid))

    loc_obj["vertices"] = parse_vertices(vs)
    return loc_obj


# how to interpret what data in geom type
# keys: dxf types, value: geom_type
geom_mapping = {
    'POINT'     : parse_point,
    'LINE'      : parse_line,
    'CIRCLE'    : parse_circle,
    'POLYLINE'  : parse_polyline,
    'LWPOLYLINE': parse_polyline,
    'SPLINE'    : parse_spline
}

default_types = [
    'POINT',
    'LINE',
    'POLYLINE',
    'LWPOLYLINE',
    'CIRCLE',
    'SPLINE'
]

dxf_to_json_mapping = {
}

# file handling


def opening_dxf(dxf_file: str) -> Modelspace:
    doc = ezdxf.readfile(dxf_file)
    return doc.modelspace()


def entity_parsing(e: DXFGraphic):
    """function that parses all the dxf geometries as defined in geom_mapping
    dict in the dxf_parsers file
    input:
        e :         dxf_entity
    retrun:
        obj_dict :  new obj_dict"""
    return geom_mapping[e.dxftype()](e)


def dxf_to_json(dxf_file: str):
    """function that takes a path string pointing to a dxf and returns a json"""
    dxf_msp = opening_dxf(dxf_file)
    objs = deconstruct_msp(dxf_msp)

    # print(os.path.splitext(dxf_file))
    json_path = os.path.splitext(dxf_file)[0] + ".json"
    print(json_path)

    with open(json_path, 'w') as outfile:
        json.dump(objs, fp=outfile)


def construct_layer_map(dxf_layers) -> dict:
    local_type_dict = dict(dxf_to_json_mapping)

    for layer in dxf_layers:
        if not(isinstance(layer, str)):
            l_name = layer.dxf.name
        else:
            l_name = layer

        try:
            local_type_dict[l_name]
        except:
            local_type_dict[l_name] = default_types

    return local_type_dict


def parse_entities(entities: list, layer_type_dict: dict) -> list:
    other_layers = set()
    missing_layer_type_dict = {}

    geom_list = []
    insert_list = []

    for e in entities:
        try:
            if e.dxftype() in layer_type_dict[e.dxf.layer]:
                try:
                    geom_list.append(entity_parsing(e))
                except:
                    traceback.print_exc()

            elif e.dxftype() == 'INSERT':
                insert_list.append(e)

            else:
                try:
                    missing_layer_type_dict[e.dxf.layer].add(e.dxftype())
                except:
                    missing_layer_type_dict[e.dxf.layer] = set()
                    missing_layer_type_dict[e.dxf.layer].add(e.dxftype())
        except:
            other_layers.add(e.dxf.layer)
    try:
        geom_list.extend(parse_blocks(insert_list))
    except:
        traceback.print_exc()

    # print(other_layers)
    # print(layer_type_dict)
    # print(missing_layer_type_dict)

    all_types = set()
    for values in layer_type_dict.values():
        for v in values:
            all_types.add(v)

    for values in missing_layer_type_dict.values():
        for v in values:
            all_types.add(v)

    print("all layer types: {}".format(", ".join(all_types)))

    return geom_list


def deconstruct_msp(dxf_msp: Modelspace) -> list:
    layer_type_dict = construct_layer_map(dxf_msp.doc.layers)

    return parse_entities(list(dxf_msp), layer_type_dict)


def deconstruct_entity_list(entities: list) -> list:
    layer_type_dict = construct_layer_map([e.dxf.layer for e in entities])

    return parse_entities(entities, layer_type_dict)


def dxf_check(map_dict: dict, layer_name: str, entity_type: str) -> bool:
    if layer_name in map_dict:
        return entity_type in map_dict[layer_name]
    else:
        return False


if __name__ == "__main__":

    src_path = "./test_data/"
    global_all_types = set()

    path_list = list(os.listdir("./test_data/"))

    # pth = src_path + "circle_line_pl.dxf"
    # print("==== {} ====".format(pth))
    # # msp = opening_dxf(pth)
    # # all_types = deconstruct_msp(msp)
    #
    # dxf_to_json(pth)
    #
    # pth = src_path + "block_exported_2.dxf"
    # # print("==== {} ====".format(pth))
    # dxf_to_json(pth)

    for pth in path_list:
        file_extension = os.path.splitext(pth)[1][1:]
        if file_extension == 'dxf':
            dxf_to_json(src_path+pth)