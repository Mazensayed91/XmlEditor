import re
from utils import *
from helpers.minify import minify_xml
from pandas.io.json import json_normalize


class XmlToJson:

    def __init__(self, xml):
        self.index = 0
        self.xml = xml
        self.json = {}

    def clean(self):
        xml_minified = minify_xml(self.xml)
        xml_comments_removed = remove_comments(xml_minified)
        self.xml = xml_comments_removed

    def xml_to_json(self):
        self.clean()
        self.xml_json(self.json)

    def xml_json(self, json, t_name=None):

        if len(self.xml) == 0:
            return
        opening_tag_name = re.search(r'<.*?>', self.xml).group()
        closing_tag_name = re.search(r'</.*?>', self.xml).group()

        opening_tag_index = self.xml.index(opening_tag_name) + len(opening_tag_name)
        closing_tag_index = self.xml.index(closing_tag_name) + len(closing_tag_name)

        if (closing_tag_index == len(closing_tag_name)) and (closing_tag_name[2:-1] == t_name):
            self.xml = self.xml[len(closing_tag_name):]
            return

        if opening_tag_index < closing_tag_index:
            self.xml = self.xml[opening_tag_index:]
            tag_attrs_list = opening_tag_name.split(' ')
            tag_name = tag_attrs_list[0][1:].replace('>', '')

            if len(tag_attrs_list) > 1:
                self.index += len(opening_tag_name)
                attrs_dict = {'@'+item.split('=')[0]: item.split('=')[1].replace('>', '')[1:-1]
                              for item in tag_attrs_list[1:]}

            else:
                self.index += len(opening_tag_name)
                attrs_dict = {}

            if tag_name in json:
                value = json[tag_name]
                if ~isinstance(value, list):
                    json[tag_name] = [value]
                json[tag_name].append(attrs_dict)
            else:
                json[tag_name] = attrs_dict

            if self.xml[0] != '<':  # Indicate text value
                first_tag_index = self.xml.index('<')
                text_value = self.xml[0:first_tag_index]
                self.xml = self.xml[first_tag_index:]
                if type(json[tag_name]) != list:
                    json[tag_name]['#text'] = text_value
                else:
                    json[tag_name][-1]['#text'] = text_value

            self.xml_json(json[tag_name], tag_name)

        self.xml_json(json, t_name)


xml = """<span>sometextutal!!<a class="url" href="http://www.web2con.com/">text<span class="summary"></span><abbr class="dtstart" title="2005-10-05"></abbr><abbr class="dtend" title="2005-10-08"></abbr><span class="location">sometextual2</span></a></span>"""
# xml = """<li></li><ui></ui><l></l><li></li>"""
obj = XmlToJson(xml)
obj.xml_to_json()
print(obj.json)
