import mimetypes
import os
import datetime

import pandas as pd

media_files = ["audio", "video", "image"]
def find_media_files(dir_path):
    ret_files = []
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            file_path = os.path.join(root, file)
            file_type = detect_file_type(file_path)
            if file_type in media_files:
                ret_files.append(file_path)
    return ret_files

def converted_dir():
    return os.environ.get("CONVERTED_DIR", "converted")

def detect_file_type(file_path):
    type, encoding = mimetypes.guess_type(file_path)
    if type:
        if type.startswith("audio"): return "audio"
        elif type.startswith("video"): return "video"
        elif type.startswith("image"): return "image"
    return "unknown"

def conversion_history(original_path, output_format, output_path, used_programme):
    history_file = os.path.join(converted_dir(), "history.csv")
    history_dict = {
        "date&time": datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S"),
        "original_path": original_path,
        "output_format": output_format,
        "output_path": output_path,
        "used_programme": used_programme
    }

    history_df = pd.DataFrame([history_dict])

    if os.path.exists(history_file):
        df = pd.read_csv(history_file)
        df = pd.concat([df, history_df], ignore_index=True)
    else:
        df = history_df

    df.to_csv(history_file, index=False)