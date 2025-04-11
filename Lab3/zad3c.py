import sys
from zad2a import read_log
from zad3b import log_to_dict

def print_dict_entry_dates(log_dict):
    for uid, entries in log_dict.items():
        print(f"Session: {uid}")

        host_dict = {}

        for entry in entries:
            host = entry["host"]
            method = entry["method"]
            status_code = entry["status_code"]
            ts = entry["ts"]

            if host not in host_dict:
                host_dict[host] = {
                    "requests": 0,
                    "methods": {},
                    "2xx_requests": 0,
                    "first_request": ts,
                    "last_request": ts
                }

            host_dict[host]["requests"] += 1

            if method not in host_dict[host]["methods"]:
                host_dict[host]["methods"][method] = 0
            host_dict[host]["methods"][method] += 1

            if 200 <= status_code <= 299:
                host_dict[host]["2xx_requests"] += 1

            if ts < host_dict[host]["first_request"]:
                host_dict[host]["first_request"] = ts

            if ts > host_dict[host]["last_request"]:
                host_dict[host]["last_request"] = ts

        for host, data in host_dict.items():
            print(f"Host: {host}")
            print(f"Requests: {data['requests']}")

            print(f"First request: {data['first_request'].strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"Last request: {data['last_request'].strftime('%Y-%m-%d %H:%M:%S')}")

            all_requests = data["requests"]
            for method, count in data["methods"].items():
                percent_method = (count / all_requests) * 100 if all_requests > 0 else 0
                print(f"Percentage of {method}: {percent_method:.2f}%")

            percent_2xx = (data['2xx_requests'] / all_requests) * 100 if all_requests > 0 else 0
            print(f"Percentage of 2xx requests: {percent_2xx:.2f} %")
        print("-" * 50)

if __name__ == '__main__':
    print_dict_entry_dates(log_to_dict(read_log(sys.stdin)[:10]))