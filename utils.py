import re
import json
import io

def remove_comments(xml):

    xml_modified = re.sub(r'<!--[\w\s]+-->', '', xml)
    return xml_modified

def remove_intro(xml):

    xml_modified = re.sub(r'<\?[\w\s]+\?>', '', xml)
    return xml_modified

def to_json(json_dictionary, path='xml'):
    with open(path+'.json', 'w') as f:
        json.dump(json_dictionary, f)


def read_xml(path):
    with open(path, 'r') as f:
        data = f.read()
    return data

def write_xml(path, data):
    with io.open(path, 'w', encoding='ascii') as f:
        f.write(data)
