import core

def first_20_sentences(text):
    return_sentences = "|"
    sentences_counter = 0

    for line in text:
        line = line.strip()

        current_sent = ""
        for character in line:
            if character in core.marks:
                current_sent = current_sent + character
                current_sent = current_sent.strip()
                if sentences_counter < 20:
                    return_sentences = return_sentences + current_sent + "|"
                    sentences_counter = sentences_counter + 1
                current_sent = ""
            else:
                current_sent = current_sent + character
        if current_sent != "":
            current_sent = current_sent.strip()
            if sentences_counter < 20:
                return_sentences = return_sentences + current_sent + "|"
                sentences_counter = sentences_counter + 1

    return return_sentences

if __name__ == '__main__':
    core.output(first_20_sentences(core.input()))