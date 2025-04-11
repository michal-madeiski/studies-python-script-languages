import sys
import utils
from datetime import datetime

def read_log(file):
    logs = []
    errors = []
    for line in file:
        line = line.strip().split('\t')
        if line == "":
            continue
        try:
            ts = datetime.fromtimestamp(float(line[utils.orig_idx["ts"]]))
            uid = line[utils.orig_idx["uid"]]
            orig_h = line[utils.orig_idx["orig_h"]]
            orig_p = int(line[utils.orig_idx["orig_p"]])
            resp_h = line[utils.orig_idx["resp_h"]]
            resp_p = int(line[utils.orig_idx["resp_p"]])
            method = line[utils.orig_idx["method"]]
            host = line[utils.orig_idx["host"]]
            uri = line[utils.orig_idx["uri"]]
            status_code = int(line[utils.orig_idx["status_code"]])

            entry = (ts, uid, orig_h, orig_p, resp_h, resp_p, method, host, uri, status_code)
            logs.append(entry)
        except Exception as e:
            #print(f"Error({e}) during reading log in line: {line}", file=sys.stderr)
            continue
    return logs

if __name__ == '__main__':
    print(read_log(sys.stdin)[:1])