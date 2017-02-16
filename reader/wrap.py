def text_wrap(text, width):
    clear = text.split()
    count = 0
    s = []
    newline = False
    prev = None

    for word in clear:
        if count + len(word) + 1 <= width:
            if newline:
                count += len(prev) + 1
                newline = False
            count += len(word) + 1
            s.append(word + ' ')
        else:
            s.append('\n')
            s.append(word + ' ')
            count = 0
            prev = word
            newline = True
    return ''.join(s)
