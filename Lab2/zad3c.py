import core

def sentences_with_proper_name_percent(text):
    sentences_counter = 0
    sentences_with_proper_name_counter = 0

    for line in text:
        line = line.strip()
        new_sentence = True
        is_big_letter = False

        for character in line:
            if character in core.marks:
                new_sentence = True
                is_big_letter = False
                sentences_counter += 1
            else:
                if new_sentence and character.isupper():
                    new_sentence = False
                elif character.isupper() and not is_big_letter:
                    is_big_letter = True
                    sentences_with_proper_name_counter += 1

    if sentences_counter == 0:
        return "There are no sentences in the text."
    percent = str((sentences_with_proper_name_counter / sentences_counter * 100)) + '%'
    return percent

if __name__ == '__main__':
    core.output(sentences_with_proper_name_percent(core.input()))