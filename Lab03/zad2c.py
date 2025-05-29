import sys
import ipaddress
import utils
from zad2a import read_log

def get_entries_by_addr(log_list, ip):
    if not log_list: return []
    ret_list = []

    try:
        ipaddress.ip_address(ip)
        for log in log_list:
            if log[utils.entry_idx["orig_h"]] == ip or log[utils.entry_idx["resp_h"]] == ip or log[utils.entry_idx["host"]] == ip:
                ret_list.append(log)
        return ret_list
    except ValueError as e:
        print(f"Filtration by ip address failed as ip address {ip} is invalid: {e}", file=sys.stderr)
        return []

if __name__ == "__main__":
    print(get_entries_by_addr(read_log(sys.stdin)[:3], "192.168.202.80"))