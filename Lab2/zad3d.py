import core

def longest_sentence(text):
    longest_sent = ""

    for line in text:
        current_sent = ""
        line = line.strip()

        for character in line:
            if character in core.marks:
                current_sent = current_sent + character
                if len(current_sent) > len(longest_sent):
                    longest_sent = current_sent
                current_sent = ""
            else:
                current_sent = current_sent + character
        if current_sent != "":
            current_sent = current_sent.strip()
            if len(current_sent) > len(longest_sent):
                longest_sent = current_sent

    return longest_sent

if __name__ == '__main__':
    core.output(longest_sentence(core.input()))