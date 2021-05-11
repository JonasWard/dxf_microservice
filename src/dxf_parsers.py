object_prototype = {
    "vertices": [],
    "name": None,
    "type": "STAMP",
    "reference_objects": None,
    "radius": 1.,
    "invalidities": [],
    "uuid": None,
    "layer": "0",
    "connections": None
}


def new_object(layer_name: str = None, uuid: str = None) -> dict:
    """Method that create a new object based of the prototype dictionary
    input:
    layer_name : string (default: None) - if input invalid sets layer to 'default'
    uuid :       string (default: None)
    return:
    new dict"""

    n_dict = dict(object_prototype)
    if layer_name is None or isinstance(layer_name, str):
        n_dict["layer_name"] = "default"
    else:
        n_dict["layer_name"] = layer_name

    n_dict["uuid"] = uuid

    return n_dict


def parse_point(pt, layer_name: str = None, uuid: str = None) -> dict:
    loc_obj = new_object(layer_name, uuid)
    return loc_obj


def parse_circle(c, layer_name: str = None, uuid: str = None) -> dict:
    loc_obj = new_object(layer_name, uuid)
    return loc_obj


def parse_line(ln, layer_name: str = None, uuid: str = None) -> dict:
    loc_obj = new_object(layer_name, uuid)
    return loc_obj


def parse_polyline(pl, layer_name: str = None, uuid: str = None) -> dict:
    loc_obj = new_object(layer_name, uuid)
    return loc_obj


def parse_block(blck, layer_name: str = None, uuid: str = None) -> dict:
    loc_obj = new_object(layer_name, uuid)
    return loc_obj


def parse_spline(spl, layer_name: str = None, uuid: str = None) -> dict:
    loc_obj = new_object(layer_name, uuid)
    return loc_obj
