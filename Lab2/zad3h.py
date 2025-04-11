import core

def only_special_marks_sentences(text):
    return_sentences = "|"

    for line in text:
        current_sent = ""
        line = line.strip()

        for character in line:
            if character in core.marks:
                current_sent = current_sent + character
                current_sent = current_sent.strip()
                if current_sent[-1] in "!?":
                    return_sentences = return_sentences + current_sent + "|"
                current_sent = ""
            else:
                current_sent = current_sent + character

    return return_sentences

if __name__ == '__main__':
    core.output(only_special_marks_sentences(core.input()))