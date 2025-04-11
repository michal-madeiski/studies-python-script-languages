import sys
import utils
from zad2a import read_log

def get_failed_reads(log_list, num_of_lists):
    if not log_list: return []
    ret_list_4XX = []
    ret_list_5XX = []

    try:
        for log in log_list:
            code = int(log[utils.entry_idx["status_code"]])
            if 400 <= code <= 499:
                ret_list_4XX.append(log)
            if 500 <= code <= 599:
                ret_list_5XX.append(log)
        if num_of_lists == 1:
            return ret_list_4XX + ret_list_5XX
        else:
            return ret_list_4XX, ret_list_5XX
    except ValueError as e:
        print("Filtration by status code failed...")
        return e
if __name__ == "__main__":
    print(get_failed_reads(read_log(sys.stdin)[:3], 1))