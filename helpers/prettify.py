import re


def prettify_xml(xml):
    xml2 = ""
    counter = -1
    edit_flag = False
    prev_close = False
    for i in range(len(xml)):
        if xml[i] == '<' and xml[i + 1] not in ['!', '/']:
            counter += 1
            edit_flag = True
            prev_close = False
        elif xml[i] == '<' and xml[i + 1] == '/':
            if not prev_close:
                counter -= 1
            if xml[i-1] == '>':
                edit_flag = True
            prev_close = True
        elif xml[i] == '/' and xml[i+1] == '>':
            counter -= 1
        if edit_flag:
            if xml2 != "":
                 xml2 += '\n'
            for j in range(counter):
                xml2 += '\t'
            edit_flag = False
            if prev_close:
                counter -= 1
        xml2 += xml[i]

    return xml2