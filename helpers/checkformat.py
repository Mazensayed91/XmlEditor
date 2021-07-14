import re


def fix_errors(text):
    text = ''.join([text[0:2], re.sub('<\?.*\?>', '', text[2:])])
    correct_xml = ""
    stored = []
    storing = False
    closing = False
    closing_bracket_missing = False
    current_tag = ""
    escape_char = False
    for i in range(len(text)):
        if text[i] == '<':
            if closing_bracket_missing:
                # Open tag missing closing bracket
                correct_xml += '>'
            if text[i + 1] == '/':
                closing = True
            elif text[i + 1] in ['?', '!']:
                closing_bracket_missing = True
                correct_xml += text[i]
                continue
            closing_bracket_missing = True
            storing = True

        elif (text[i] == '>' or text[i] == ' ') and storing:
            if closing:
                if len(stored) > 1:
                    last_tag = stored.pop()
                    if current_tag[1:len(current_tag)] != last_tag:
                        # closing tag different from the open tag
                        correct_xml = ''.join([correct_xml[:-len(current_tag)-1] + '</' + last_tag])
                    if text[i] == ' ':
                        # closing tag contain space
                        escape_char = True
                else:
                    correct_xml = correct_xml[:-len(current_tag) - 1]
                    correct_xml += ('<' + current_tag[1:] + '>' + '<' + current_tag)
                current_tag = ""
                storing = False
                closing = False
            else:
                if text[i - 1] == '<':
                    # open tag starting with space or has no name {"<>" or "< tag>"}
                    if text[i] == '>':
                        correct_xml = correct_xml[:-1]
                        escape_char = True
                    elif text[i] == ' ':
                        escape_char = True
                else:
                    stored.append(current_tag)
                    current_tag = ""
                    storing = False
                    closing = False

        elif storing:
            current_tag = current_tag + text[i]

        if text[i] == '>':
            if text[i-1] == '/':   # self closing tag
                if text[i-2] == '<':
                    # close tag has no name {"</>"}
                    correct_xml = correct_xml[:-2]
                    escape_char = True
                stored.pop()
            if closing_bracket_missing:
                closing_bracket_missing = False
            else:
                # extra closing bracket
                escape_char = True
        if not escape_char:
            correct_xml += text[i]
        escape_char = False
    # remaining not closed tags
    if len(stored) != 0:
        for tag in reversed(stored):
            correct_xml = correct_xml + '</' + tag + '>'
    return correct_xml


def check_format(text):
    stored = []
    storing = False
    closing = False
    closing_bracket_missing = False
    current_tag = ""
    i = 0
    for i in range(len(text)):
        if text[i] == '<':
            if closing_bracket_missing:
                # Open tag missing closing bracket
                return i
            if text[i + 1] == '/':
                closing = True
            elif text[i + 1] in ['?', '!']:
                closing_bracket_missing = True
                continue
            closing_bracket_missing = True
            storing = True

        elif (text[i] == '>' or text[i] == ' ') and storing:
            if closing:
                if current_tag[1:len(current_tag)] != stored.pop():
                    # closing tag different from the open tag
                    return i - len(current_tag) + 1
                elif text[i] == ' ':
                    # closing tag contain space
                    return i - len(current_tag) + 1
            else:
                if text[i - 1] == '<':
                    # open tag starting with space or has no name {"<>" or "< tag>"}
                    return i - 1
                stored.append(current_tag)
            current_tag = ""
            storing = False
            closing = False

        elif storing:
            current_tag = current_tag + text[i]

        if text[i] == '>':
            if text[i-1] == '/':   # self closing tag
                if text[i-2] == '<':
                    # close tag has no name {"<\>"}
                    return i-2
                stored.pop()
            if closing_bracket_missing:
                closing_bracket_missing = False
            else:
                # extra closing bracket
                return i
    # remaining not closed tags
    if len(stored) == 0:
        return True
    else:
        return i

