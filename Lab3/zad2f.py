import sys
import utils
from zad2a import read_log

def get_entries_by_extension(log_list, ext):
    if not log_list: return []
    ret_list = []

    for log in log_list:
        uri = log[utils.entry_idx["uri"]]
        if uri.endswith(f".{ext}"):
            ret_list.append(log)
    return ret_list
if __name__ == "__main__":
    print(get_entries_by_extension(read_log(sys.stdin), "java"))