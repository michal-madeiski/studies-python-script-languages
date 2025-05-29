import sys
from zad2a import read_log

def sort_logs_by_element(log_list, idx):
    if not log_list: return []

    try:
        return sorted(log_list, key=lambda entry: entry[idx])
    except IndexError as e:
        print(f"Sorting failed as index {idx} is out of range: {e}", file=sys.stderr)
        return log_list

if __name__ == "__main__":
    print(sort_logs_by_element(read_log(sys.stdin)[7:10], 1))