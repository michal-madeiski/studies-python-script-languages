import collections
import os
import subprocess
import sys
import pandas as pd

text_stats_script = "zad4abc.py"
temp_dict = {
    "num_of_vals": 8,
    "file_path": 0,
    "char_count_idx": 1,
    "word_count_idx": 2,
    "line_count_idx": 3,
    "most_common_char_idx": 4,
    "most_common_char_count_idx": 5,
    "most_common_word_idx": 6,
    "most_common_word_count_idx": 7,
}

def dir_stats(dir_path):
    try:
        dir = os.listdir(dir_path)
    except NotADirectoryError:
        print("f {dir_path} is not a directory.")
        sys.exit(1)
    except FileNotFoundError:
        print(f"Directory {dir_path} not found.")
        sys.exit(1)

    files = []
    total_char_count = 0
    total_word_count = 0
    total_line_count = 0

    char_dict = collections.Counter()
    word_dict = collections.Counter()

    for file in dir:
        file_path = os.path.join(dir_path, file)
        if os.path.isfile(file_path):
            try:
                res = subprocess.run(
                    ["python", text_stats_script],
                    input=file_path,
                    text=True, #byte is default
                    capture_output=True
                )

                output = [line for line in res.stdout.strip().split("\n") if line.strip()]
                if output:
                    values = output[1].split(",") #0 is column names
                    if len(values) == temp_dict["num_of_vals"]:

                        files.append({
                            "file_path": values[temp_dict["file_path"]],
                            "char_count": values[temp_dict["char_count_idx"]],
                            "word_count": values[temp_dict["word_count_idx"]],
                            "line_count": values[temp_dict["line_count_idx"]],
                            "most_common_char": values[temp_dict["most_common_char_idx"]],
                            "most_common_char_count": values[temp_dict["most_common_char_count_idx"]],
                            "most_common_word": values[temp_dict["most_common_word_idx"]],
                            "most_common_word_count": values[temp_dict["most_common_word_count_idx"]],
                        })

                        total_char_count += int(values[temp_dict["char_count_idx"]])
                        total_word_count += int(values[temp_dict["word_count_idx"]])
                        total_line_count += int(values[temp_dict["line_count_idx"]])

                        char_dict[values[temp_dict["most_common_char_idx"]]] += int(values[temp_dict["most_common_char_count_idx"]])
                        word_dict[values[temp_dict["most_common_word_idx"]]] += int(values[temp_dict["most_common_word_count_idx"]])
            except subprocess.CalledProcessError as e:
                print(f"Exception while processing {file_path}: {e}")
                continue

    most_common_char = char_dict.most_common(1)[0] if char_dict else None
    most_common_word = word_dict.most_common(1)[0] if word_dict else None

    df = pd.DataFrame([{
        "file_count": len(files),
        "total_chars": total_char_count,
        "total_words": total_word_count,
        "total_lines": total_line_count,
        "most_common_char": most_common_char[0],
        "most_common_char_idx": most_common_char[1],
        "most_common_word": most_common_word[0],
        "most_common_word_idx": most_common_word[1],
    }])

    df.to_csv(sys.stdout, index=False)
    df.to_csv("outputs/zad4d_output.csv", index=False)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        dir_stats(sys.argv[1])
    else:
        print("Command is incorrect. Correct usage: python zad4d.py <directory>.")