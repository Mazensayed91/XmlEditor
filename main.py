from imports import *
import struct
import io
# import endecrypt


class XML:
    def __init__(self):
        self.text = ""
        self.path = ""

    def open(self, path):
        self.path = path
        self.text = read_xml(path)

    def save(self):
        write_xml(self.path, self.text)

    def save_as(self, path, option):
        if option == 'Compressed':
            write_xml(path, self.compress())
        elif option == 'JSON':
            to_json(self.xml_to_json(), path)
        else:
            write_xml(path, self.text)

    def prettify(self):
        self.text = prettify_xml(self.text)

    def xml_to_json(self):

        obj = XmlToJson(self.text)
        return obj.xml_to_json()

    def fix_errors(self):
        self.text = fix_errors(self.text)

    def compress(self):
        return encode(self.text)
        
    def decompress(self):
        pass

    def minimize(self):
        """
        @rtype:   str
        @return:  the xml file but minimized by removing spaces, new lines and tabs.
        """
        return minify_xml(self.text)

    def check_format(self):
        """
        The method returns true if format is correct, false if a key is missing, or a specific index of the incorrect
        key if found
        """
        return check_format(self.text)



# check for format test

XML1 = XML()
XML1.open("data.adj.xml")
XML1.minimize()
XML1.save_as("test.bin",'Compressed')
write_xml("test2_bin.txt", decode("test.bin"))



