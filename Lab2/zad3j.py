import core

def sentences_with_min_2_special_words(text):
    return_sentences = "|"

    for line in text:
        line = line.strip()

        current_sent = ""
        for character in line:
            if character in core.marks:
                current_sent = current_sent + character
                return_sentences = special_words_helper(current_sent, return_sentences)

                current_sent = ""
            else:
                current_sent = current_sent + character
        if current_sent != "":
            return_sentences = special_words_helper(current_sent, return_sentences)

    return return_sentences

def special_words_helper(curr, ret):
    curr = curr.strip()
    if int(curr.count("i") > 0) + int(curr.count("oraz") > 0) + int(curr.count("ale") > 0) + int(curr.count("że") > 0) + int(curr.count("lub")) >= 2:
        ret = ret + curr + "|"
    return ret

if __name__ == '__main__':
    core.output(sentences_with_min_2_special_words(core.input()))