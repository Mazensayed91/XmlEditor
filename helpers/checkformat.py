def check_format(text):
    stored = []
    storing = False
    closing = False
    current_tag = ""
    for i in range(len(text)):
        if text[i] == '<':
            if text[i + 1] == '/':
                closing = True
            storing = True

        elif (text[i] == '>' or text[i] == ' ') and storing:
            if closing:
                if current_tag[1:len(current_tag)] != stored.pop():
                    return i - len(current_tag) + 1
                elif text[i] == ' ':
                    return i - len(current_tag) + 1
            else:
                if text[i-1] == '<':
                    return i-1
                stored.append(current_tag)
            current_tag = ""
            storing = False
            closing = False

        elif storing:
            current_tag = current_tag + text[i]
    if len(stored) == 0:
        return True
    else:
        return False