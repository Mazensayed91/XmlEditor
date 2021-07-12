import re
import json


def remove_comments(xml):

    xml_modified = re.sub(r'<!--[\w\s]+-->', '', xml)
    return xml_modified


def to_json(json_dictionary):
    with open('xml.json', 'w') as f:
        json.dump(json_dictionary, f)
