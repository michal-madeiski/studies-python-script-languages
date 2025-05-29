import collections
import io
import re
import sys
import pandas as pd

sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding="utf-8")
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

def text_stats(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            file = f.read()
    except FileNotFoundError:
        print(f"File '{file}' not found.")
        sys.exit(1)

    text = file.splitlines()
    words = re.split(r"\W+", file)
    char_count = len(file)
    word_count = len(words)
    line_count = len(text)

    char_dict = collections.Counter(file.replace("\n", ""))
    word_dict = collections.Counter(words)

    most_common_char = char_dict.most_common(1)[0] if char_dict else None
    most_common_word = word_dict.most_common(1)[0] if word_dict else None

    df = pd.DataFrame([{
        "file_path": file_path,
        "char_count": char_count,
        "word_count": word_count,
        "line_count": line_count,
        "most_common_char": most_common_char[0],
        "most_common_char_count": most_common_char[1],
        "most_common_word": most_common_word[0],
        "most_common_word_count": most_common_word[1],
    }])

    df.to_csv(sys.stdout, index=False)
    df.to_csv("outputs/zad4abc_output.csv", index=False)

if __name__ == "__main__":
    file_path = sys.stdin.read().strip() #use echo
    text_stats(file_path)