import sys
import utils
from zad2a import read_log

def get_entries_by_code(log_list, code):
    if not log_list: return []
    ret_list = []

    try:
        code = int(code)
        for log in log_list:
            if log[utils.entry_idx["status_code"]] == code:
                ret_list.append(log)
        return ret_list
    except ValueError as e:
        print("Filtration by status code failed...")
        return e
if __name__ == "__main__":
    print(get_entries_by_code(read_log(sys.stdin)[:3], "404"))