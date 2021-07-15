from utils import *
from helpers.minify import minify_xml


class XmlToJson:

    def __init__(self, xml):
        # self.index = 0
        self.xml = xml
        self.json = {}

    def clean(self):
        xml_minified = minify_xml(self.xml)
        self.xml = remove_comments(xml_minified)
        self.xml = remove_intro(self.xml)

    def xml_to_json(self):
        self.clean()
        self.xml_json(self.json)
        return self.json

    def xml_json(self, json, t_name=None):
        # Base case
        if len(self.xml) == 0:
            return
        # added try as re.search function gives error if failed to find any text (happens after taking the final opening tag)
        try:
            opening_tag_name = re.search('<[^/]+?.*?>', self.xml).group()
        except:
            opening_tag_name = self.xml
        closing_tag_name = re.search(r'</.*?>', self.xml).group()
        closing_tag_name = re.search(r'</.*?>', self.xml).group()

        opening_tag_index = self.xml.index(opening_tag_name) + len(opening_tag_name)
        closing_tag_index = self.xml.index(closing_tag_name) + len(closing_tag_name)

        # Check if the current found tag is a closing tag to the current tag's dictionary we are in
        if (closing_tag_index == len(closing_tag_name)) and (closing_tag_name[2:-1] == t_name):
            self.xml = self.xml[len(closing_tag_name):]
            return

        # Separate attributes and save it to a new dictionary with a key of it's open tag name
        if opening_tag_index < closing_tag_index:
            self.xml = self.xml[opening_tag_index:]
            tag_attrs_list = opening_tag_name.split(' ')
            tag_name = tag_attrs_list[0][1:].replace('>', '')

            # Concatenate broken attributes
            element = len(tag_attrs_list) - 1
            while element:
                if "=" not in tag_attrs_list[element]:
                    tag_attrs_list[element - 1] = ' '.join(tag_attrs_list[element - 1:])
                    tag_attrs_list.pop(element)
                element -= 1

            # Check if the opening tag has any attributes
            if len(tag_attrs_list) > 1:
                attrs_dict = {'@' + item.split('=')[0]: item.split('=')[1].replace('>', '')[1:-1]
                              for item in tag_attrs_list[1:]}
            else:
                attrs_dict = {}

            # Check if the current opening tag is already on the dictionary
            if tag_name in json:
                if type(json[tag_name]) is dict:
                    value = json[tag_name]
                    json[tag_name] = [value]
                    json[tag_name].append(attrs_dict)
                else:
                    json[tag_name].append(attrs_dict)
            else:
                json[tag_name] = attrs_dict

            # check if the tag contains text (add it in a key named #text)
            if self.xml[0] != '<':
                first_tag_index = self.xml.index('<')
                text_value = self.xml[0:first_tag_index]
                self.xml = self.xml[first_tag_index:]
                if type(json[tag_name]) == dict:
                    json[tag_name]['#text'] = text_value
                else:
                    json[tag_name][-1]['#text'] = text_value

            # recursion depends on the current key data type as it could be dictionary or list
            if type(json[tag_name]) == dict:
                self.xml_json(json[tag_name], tag_name)
            else:
                self.xml_json(json[tag_name][-1], tag_name)

        self.xml_json(json, t_name)
