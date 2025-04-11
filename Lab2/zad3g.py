import core

def max_four_words_sentences(text):
    return_sentences = "|"

    for line in text:
        line = line.strip()

        current_sent = ""
        for character in line:
            if character in core.marks:
                current_sent = current_sent + character
                return_sentences = four_words_helper(current_sent, return_sentences)

                current_sent = ""
            else:
                current_sent = current_sent + character
        if current_sent != "":
            return_sentences = four_words_helper(current_sent, return_sentences)

    return return_sentences

def four_words_helper(curr, ret):
    curr = curr.strip()
    word_counter = 1
    for c in curr:
        if c.isspace():
            word_counter = word_counter + 1
    if "—" in curr:
        word_counter = word_counter - 1
    if word_counter <= 4:
        if len(curr) > 2:
            ret = ret + curr + "|"
        elif curr[0].isalnum():
            ret = ret + curr + "|"
    return ret

if __name__ == '__main__':
    core.output(max_four_words_sentences(core.input()))