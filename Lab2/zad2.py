import core
import re

def normalize_text(text):
    in_preamble = True
    in_publication_info = False
    preamble_empty_line_counter = 0
    preamble_line_counter = 0
    preamble_text = ''
    final_text = ''

    for line in text:
        line = line.strip()
        line = re.sub(r'\s+', ' ', line)

        if in_preamble:
            preamble_line_counter += 1
            preamble_text += line + '\n'
            if line == "":
                preamble_empty_line_counter += 1
            else:
                preamble_empty_line_counter = 0

            if preamble_line_counter == 10:
                in_preamble = False
                if preamble_empty_line_counter >= 2:
                    continue
                else:
                    final_text += preamble_text

            continue

        if line.startswith("-----"):
            in_publication_info = True
            continue

        if in_publication_info:
            continue

        final_text += line + '\n'

    return final_text

if __name__ == '__main__':
    core.output(normalize_text(core.input()))