import sys
from zad3a import entry_to_dict
from zad2a import read_log

def log_to_dict(log):
    log_dict = {}

    for entry in log:
        entry_dict = entry_to_dict(entry)
        uid = entry_dict["uid"]
        if uid not in log_dict:
            log_dict[uid] = []
        log_dict[uid].append(entry_dict)
    return log_dict

if __name__ == '__main__':
    print(log_to_dict(read_log(sys.stdin)[:10]))