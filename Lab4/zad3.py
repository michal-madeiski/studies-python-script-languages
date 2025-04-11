import sys

def tail():
    num_of_end_lines = 10
    file = None
    follow_flag = False

    if len(sys.argv) > 1:
        if sys.argv[1].startswith("--lines="):
            num_of_end_lines = sys.argv[1].split("=")[1]
            if not num_of_end_lines.isnumeric() or (num_of_end_lines.isnumeric() and int(num_of_end_lines) <= 0):
                raise ValueError("Number of end lines must be a positive integer.")
            else:
                num_of_end_lines = int(num_of_end_lines)
                if len(sys.argv) > 3 and sys.argv[2] == "--follow":
                    follow_flag = True
                    file = sys.argv[3]
                elif len(sys.argv) > 2:
                    file = sys.argv[2]
        elif sys.argv[1] == "--follow":
            follow_flag = True
            if len(sys.argv) > 2:
                file = sys.argv[2]
        else:
            file = sys.argv[1]

    if file is None:
        lines = sys.stdin.readlines()
    else:
        try:
            with open(file, 'r', encoding="utf-8") as f:
                lines = f.readlines()
        except FileNotFoundError:
            print(f"File '{file}' not found.")
            sys.exit(1)

    end_lines = lines[-num_of_end_lines:] if len(lines) > num_of_end_lines else lines
    for line in end_lines:
        print(line, end="")

    if follow_flag:
        try:
            with open(file, "r") as f:
                f.seek(0, 2)
                while True:
                    line = f.readline()
                    if line:
                        print(line, end="")
        except KeyboardInterrupt:
            print("Following stopped.")
            sys.exit(0)


if __name__ == "__main__":
    tail()