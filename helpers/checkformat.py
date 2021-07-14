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

