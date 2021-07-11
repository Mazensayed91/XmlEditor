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
"""
test1 = XML()
texts2 = "<root><li><s>values</s></li></root>"
texts = "<root><folder><title>Folder One</title><item><title>Item One</title></item><item><title>Item Two</title></item>
<item><title>Item Three</title></item><folder><title>Folder Two</title><item><title>Item Four</title></item><item><title
>Item Five</title></item><item><title>Item Six</title></item></folder></folder><folder><title>Folder Three</title><item>
<title>Item Six</title></item><item><title>Item Seven</title></item><item><title>Item Eight</title></item></folder>
</root>"
test1.open(texts)

print(test1.checkFormat())
"""

