import datetime
import os
import subprocess
import sys
from utils import find_media_files, detect_file_type, converted_dir, conversion_history

def media_converter(dir_path, output_format):
    files = find_media_files(dir_path)
    dir = converted_dir()
    os.makedirs(dir, exist_ok=True)

    for file in files:
        file_type = detect_file_type(file)
        file_name = os.path.basename(file)
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        output_file = os.path.join(dir, f"{timestamp}-{file_name}.{output_format}")

        if file_type == "image":
            sub_proc_command = ["D:\\Programy i IDE - od 01.10.2024\\ImageMagick-7.1.1\\magick.exe",
                                "convert",
                                file,
                                output_file]
            used_programme = "ImageMagcik"
        elif file_type == "audio" or file_type == "video":
            sub_proc_command = ["D:\\Programy i IDE - od 01.10.2024\\FFmpeg\\ffmpeg.exe",
                                "-loglevel",
                                "quiet",
                                "-i",
                                file,
                                output_file]
            used_programme = "FFmpeg"
        else:
            continue

        try:
            subprocess.run(sub_proc_command, check=True)
            conversion_history(file, output_format, output_file, used_programme)
            print(f"{file} -> {output_file}")
        except subprocess.CalledProcessError as e:
            print(f"Exception while converting {file_name}: {e}")
            continue

if __name__ == "__main__":
    if len(sys.argv) > 2:
        media_converter(sys.argv[1], sys.argv[2])
    else:
        print("Command is incorrect. Correct usage: python media_convert.py <directory> <output_format>.")