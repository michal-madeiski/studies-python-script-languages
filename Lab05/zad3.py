import sys
import re
from pathlib import Path
from zad1 import csv_parser

def get_addresses(path: Path, city):
    ret_list = []
    parsed_csv = csv_parser(path)
    for element in parsed_csv:
        el_city = element.get("Miejscowość", "").strip()
        city = city.strip()
        if el_city.lower() == city.lower():
            voivode = element.get("Województwo", "").strip()
            address = element.get("Adres", "").strip()

            pattern = re.compile(r"^(.+?)(\d\S*)?$")

            match = re.match(pattern, address)
            #print(match)
            if match:
                street = match.group(1).strip()
                number = match.group(2)
                ret_list.append((voivode, city, street if street else None, number if number else None))
    return ret_list

if __name__ == "__main__":
    path = Path(sys.argv[1])
    city = sys.argv[2]
    print(get_addresses(path, city))