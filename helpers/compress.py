import re


def min_compress(xml):
    return re.sub("</.*?>", "&", xml)
