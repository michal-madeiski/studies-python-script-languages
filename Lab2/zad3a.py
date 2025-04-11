import core

def paragraph_counter(text):
    counter = 0

    for line in text:
        line = line.strip()
        if line == "":
            counter += 1

    return counter

if __name__ == '__main__':
    core.output(paragraph_counter(core.input()))