import core

def first_sentence_with_subsentence(text):
    return_sentence = ""
    sentence_found = False

    for line in text:
        current_sent = ""
        line = line.strip()

        for character in line:
            if character in core.marks:
                current_sent = current_sent + character
                current_sent = current_sent.strip()
                if not sentence_found and current_sent.count(',') >= 2:
                    return_sentence = current_sent
                    sentence_found = True
                current_sent = ""
            else:
                current_sent = current_sent + character
        if current_sent != "":
            if not sentence_found and current_sent.count(',') >= 2:
                return_sentence = current_sent
                sentence_found = True

    return return_sentence

if __name__ == '__main__':
    core.output(first_sentence_with_subsentence(core.input()))