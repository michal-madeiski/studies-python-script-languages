import core

def longest_sentence_without_two_same_words_in_a_row(text):
    longest_sent = ""

    for line in text:
        current_sent = ""
        line = line.strip()

        for character in line:
            if character in core.marks:
                current_sent = current_sent + character
                current_sent = current_sent.strip()

                if not two_same_words_flag(current_sent):
                    if len(current_sent) > len(longest_sent):
                        longest_sent = current_sent
                current_sent = ""
            else:
                current_sent = current_sent + character
        if current_sent != "":
            current_sent = current_sent.strip()
            if not two_same_words_flag(current_sent):
                if len(current_sent) > len(longest_sent):
                    longest_sent = current_sent


    return longest_sent

def two_same_words_flag(sent):
    flag = False
    prev_word = ""
    current_word = ""

    for c in sent:
        if not c.isspace():
            current_word = current_word + c
        else:
            if prev_word != "" and prev_word[0].lower() == current_word[0].lower():
                flag = True
            prev_word = current_word
            current_word = ""
    if current_word != "":
        if prev_word != "" and prev_word[0].lower() == current_word[0].lower():
            flag = True
    return flag

if __name__ == '__main__':
    core.output(longest_sentence_without_two_same_words_in_a_row(core.input()))