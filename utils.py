import re
import json
import io

def remove_comments(xml):

    xml_modified = re.sub(r'<!--[\w\s]+-->', '', xml)
    return xml_modified

def remove_intro(xml):

    xml_modified = re.sub(r'<\?[\w\s]+\?>', '', xml)
    return xml

def to_json(json_dictionary, path='xml'):
    with open(path+'.json', 'w') as f:
        json.dump(json_dictionary, f)


def read_xml(path):
    with io.open(path, 'r', encoding='utf-8') as f:
        data = f.read()
    print(data[39])
    return data


def write_xml(path, data):
    with io.open(path, 'w', encoding='utf-8') as f:
        f.write(data)
