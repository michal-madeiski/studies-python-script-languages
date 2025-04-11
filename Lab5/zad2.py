import re
import sys
from pathlib import Path

def group_measurement_files_by_key(path: Path):
    ret_dict = {}

    pattern = re.compile(r"^(\d+)_(\S+)_(\w+)\.csv$")

    for file in path.iterdir():
        if file.is_file():
            match = pattern.match(file.name)
            if match:
                key = match.groups()
                #ret_dict[key] = os.path.abspath(file)
                ret_dict[key] = file
    return ret_dict

if __name__ == "__main__":
    path = Path(sys.argv[1])
    print(group_measurement_files_by_key(path))