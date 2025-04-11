import core

def lexical_order_sentences(text):
    return_sentences = "|"
    for line in text:
        current_sent = ""
        line = line.strip()

        for character in line:
            if character in core.marks:
                current_sent = current_sent + character
                current_sent = current_sent.strip()

                if lexical_order_flag(current_sent):
                    return_sentences = return_sentences + current_sent + "|"
                current_sent = ""
            else:
                current_sent = current_sent + character
        if current_sent != "":
            current_sent = current_sent.strip()
            if lexical_order_flag(current_sent):
                return_sentences = return_sentences + current_sent + "|"

    return return_sentences

def lexical_order_flag(sent):
    flag = True
    prev_word = ""
    current_word = ""

    for c in sent:
        if not c.isspace():
            current_word = current_word + c
        else:
            if prev_word != "" and prev_word[0].lower() > current_word[0].lower():
                flag = False
            prev_word = current_word
            current_word = ""
    if current_word != "":
        if prev_word != "" and prev_word[0].lower() > current_word[0].lower():
            flag = False
    return flag

if __name__ == '__main__':
    core.output(lexical_order_sentences(core.input()))