import json
import ezdxf
from dxf_parsers import *

default_types = [
    'POINT',
    'LINE',
    'POLYLINE',
    'LWPOLYLINE',
    'CIRCLE'
]

dxf_to_json_mapping = {
    '0' : ['LINE'],
    '1.SectieLijnHard' : ['LINE'],
    '0.Uitlijning' : ['LINE', 'POLYLINE', 'LWPOLYLINE']
}

def opening_dxf(dxf_file):
    doc = ezdxf.readfile(dxf_file)
    return doc.modelspace()

def dxf_line(ln):
    pass

def polyline_to_json(pl):
    pass

def dxf_to_json(dxf_file):
    pass

def construct_layer_map(dxf_layers):
    local_type_dict = dict(dxf_to_json_mapping)

    for layer in dxf_layers:
        try:
            local_type_dict[layer.dxf.name]
        except:
            local_type_dict[layer.dxf.name] = default_types

    return local_type_dict

def deconstruct_msp(dxf_msp):
    layer_type_dict = construct_layer_map(dxf_msp.doc.layers)

    other_layers = set()
    missing_layer_type_dict = {}

    for e in dxf_msp:
        try:
            if e.dxftype() in layer_type_dict[e.dxf.layer]:
                pass
                # print(e.dxftype())
            else:
                try:
                    missing_layer_type_dict[e.dxf.layer].add(e.dxftype())
                except:
                    missing_layer_type_dict[e.dxf.layer] = set()
                    missing_layer_type_dict[e.dxf.layer].add(e.dxftype())
        except:
            other_layers.add(e.dxf.layer)

    print(other_layers)
    print(layer_type_dict)
    print(missing_layer_type_dict)

def dxf_check(map_dict, layer_name, entity_type):
    if layer_name in map_dict:
        return entity_type in map_dict[layer_name]
    else:
        return False

if __name__ == "__main__":
    dxf_msp = opening_dxf("./test_data/1-100_ModelTest.dxf")
    deconstruct_msp(dxf_msp)

    dxf_msp_2 = opening_dxf("./test_data/2021_05_10-tiles.dxf")
    deconstruct_msp(dxf_msp_2)