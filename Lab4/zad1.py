import os
import sys

def env_vars_all():
    env_vars = os.environ
    filters = sys.argv[1:]
    filtered_env_vars = {}

    if len(filters) > 0:
        for key, value in env_vars.items():
            for filter in filters:
                if filter in key:
                    filtered_env_vars[key] = value
                    break
    else:
        filtered_env_vars = env_vars

    for key in sorted(filtered_env_vars):
        print(f"{key}: {filtered_env_vars[key]}")

if __name__ == "__main__":
    env_vars_all()