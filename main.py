from imports import *


class XML:
    def __init__(self):
        self.text = ""

    def open(self):
        pass

    def save(self):
        pass

    def save_as(self):
        pass

    def prettify(self):
        pass

    def xml_to_json(self):
        pass

    def compress(self):
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

test1 = XML()
texts2 = "<root><li><s>values</s></li></root>"
test1.text = text2

print(test1.checkFormat())


