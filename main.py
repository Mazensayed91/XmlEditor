class XML:
    def __init__(self):
        self.text = ""

    def open(self):
        pass

    def save(self):
        pass

    def saveAs(self):
        pass

    def Prettify(self):
        pass

    def toJson(self):
        pass

    def compress(self):
        pass

    def minimize(self):
        pass

    def checkFormat(self):
        """
        The method returns true if format is correct, false if a key is missing, or a specific index of the incorrect
        key if found
        """
        stored = []
        storing = False
        closing = False
        current_tag = ""
        for i in range(len(self.text)):
            if self.text[i] == '<':
                if self.text[i + 1] == '/':
                    closing = True
                storing = True

            elif self.text[i] == '>' or self.text[i] == ' ':
                if closing:
                    if current_tag[1:len(current_tag)] != stored.pop():
                        return i
                else:
                    stored.append(current_tag)
                current_tag = ""
                storing = False
                closing = False

            elif storing:
                current_tag = current_tag + self.text[i]
        if len(stored) == 0:
            return True
        else:
            return False


# check for format test
"""
test1 = XML()
texts2 = "<root><li><s>values</s></li></root>"
texts = "<root><folder><title>Folder One</title><item><title>Item One</title></item><item><title>Item Two</title></item><item><title>Item Three</title></item><folder><title>Folder Two</title><item><title>Item Four</title></item><item><title>Item Five</title></item><item><title>Item Six</title></item></folder></folder><folder><title>Folder Three</title><item><title>Item Six</title></item><item><title>Item Seven</title></item><item><title>Item Eight</title></item></folder></root>"
test1.open(texts)

print(test1.checkFormat())
"""

