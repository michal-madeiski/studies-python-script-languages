import os
import sys

path_items = os.getenv("PATH", "").split(os.pathsep)

def list_dirs():
    for item in path_items:
        if os.path.isdir(item):
            print(item)

def list_exec_files():
    for item in path_items:
        if os.path.isdir(item):
            print(f"{item}: ")
            files = [f for f in os.listdir(item) if os.access(os.path.join(item, f), os.X_OK)]
            for f in files:
                print(f)
        print("-" * 100)

def listing():
    if len(sys.argv) == 2 and sys.argv[1] == "-l":
        list_dirs()
    elif len(sys.argv) == 2 and sys.argv[1] == "-e":
        list_exec_files()
    else:
        print("Command is incorrect. Correct usage: python zad2.py [-l] / [-e].")


if __name__ == "__main__":
    listing()