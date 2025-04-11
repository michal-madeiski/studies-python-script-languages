import sys
from zad2a import read_log
def entry_to_dict(entry):
    dict_entry = {
        'ts': entry[0],
        'uid': entry[1],
        'orig_h': entry[2],
        'orig_p': entry[3],
        'resp_h': entry[4],
        'resp_p': entry[5],
        'method': entry[6],
        'host': entry[7],
        'uri': entry[8],
        'status_code': entry[9]
    }
    return dict_entry

if __name__ == '__main__':
    print(entry_to_dict(read_log(sys.stdin)[0]))