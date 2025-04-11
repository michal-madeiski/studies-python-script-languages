import core

def character_counter(text):
    counter = 0

    for line in text:
        line = line.strip()
        for character in line:
            if not character.isspace():
                counter += 1

    return counter

if __name__ == '__main__':
    core.output(character_counter(core.input()))