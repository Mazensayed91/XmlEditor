import re


def minify_xml(xml):
    return re.sub(">[\\s\r\n]*<", "><", xml)
