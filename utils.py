import re
import json


def remove_comments(xml):

    xml_modified = re.sub(r'<!--[\w\s]+-->', '', xml)
    return xml_modified


def to_json(json_dictionary, name='xml'):
    with open(name+'json', 'w') as f:
        json.dump(json_dictionary, f)


def read_xml(path):
    with open(path, 'r') as f:
        data = f.read()
    return data
