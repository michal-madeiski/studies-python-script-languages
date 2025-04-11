import math
import core

def fourth_quartile_sentences(text):
    return_sentences_tab = []
    return_sentences = "|"

    for line in text:
        line = line.strip()

        current_sent = ""
        for character in line:
            if character in core.marks:
                current_sent = current_sent + character
                return_sentences_tab = sentences_appender(current_sent, return_sentences_tab)

                current_sent = ""
            else:
                current_sent = current_sent + character
        if current_sent != "":
            return_sentences_tab = sentences_appender(current_sent, return_sentences_tab)

    return_sentences_tab.sort(key=len, reverse=False)
    quartile_index = math.ceil(0.75 * len(return_sentences_tab))
    return_sentences_tab = return_sentences_tab[quartile_index:]
    for sentence in return_sentences_tab:
        return_sentences = return_sentences + sentence + "|"

    return return_sentences

def sentences_appender(curr, ret):
    curr = curr.strip()
    ret.append(curr)
    return ret

if __name__ == '__main__':
    core.output(fourth_quartile_sentences(core.input()))