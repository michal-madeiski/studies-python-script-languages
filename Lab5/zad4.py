import re
import sys
from zad1 import csv_parser
from pathlib import Path

polish_latin = {
    'ą': 'a', 'ć': 'c', 'ę': 'e', 'ł': 'l', 'ń': 'n', 'ó': 'o',
    'ś': 's', 'ź': 'z', 'ż': 'z', 'Ą': 'A', 'Ć': 'C', 'Ę': 'E',
    'Ł': 'L', 'Ń': 'N', 'Ó': 'O', 'Ś': 'S', 'Ź': 'Z', 'Ż': 'Z'
}

def station_analyse(path: Path):
    parsed_csv = csv_parser(path)
    ret_dict = {
        "a": set(),
        "b": set(),
        "c": set(),
        "d": set(),
        "e": True,
        "f": set(),
        "g": set(),
    }

    date_pattern = re.compile(r"^\d{4}-\d{2}-\d{2}$")
    width_length_pattern = re.compile(r"^\d+\.\d{6}$")
    two_part_names_pattern = re.compile(r"^\w+\s*-\s*\w+$")
    three_part_names_pattern = re.compile(r"^\w+\s*-\s*\w+-\s*\w+$")
    ul_al_pattern = re.compile(r"^.*,.*(ul\.|al\.)")

    for element in parsed_csv:
        date_open = element.get("Data uruchomienia", "").strip()
        date_close = element.get("Data zamknięcia", "").strip()
        name = element.get("Nazwa stacji", "").strip()
        code = element.get("Kod stacji", "").strip()
        type = element.get("Typ stacji", "").strip()
        width = element.get("WGS84 λ E", "").strip()
        length = element.get("WGS84 φ N", "").strip()

        if date_pattern.match(date_open):
            ret_dict["a"].add(date_open)
        if date_pattern.match(date_close):
            ret_dict["a"].add(date_close)

        if width_length_pattern.match(width):
            ret_dict["b"].add(width)
        if width_length_pattern.match(length):
            ret_dict["b"].add(length)

        if two_part_names_pattern.match(name):
            ret_dict["c"].add(name)

        if name:
            name.replace(" ", "_")
            name = "".join(polish_latin.get(c, c) for c in name)
            ret_dict["d"].add(name)

        if code.endswith("MOB") and type != "mobilna":
            ret_dict["e"] = False

        if three_part_names_pattern.match(name):
            ret_dict["f"].add(name)

        if ul_al_pattern.match(name):
            ret_dict["g"].add(name)

    return ret_dict

if __name__ == "__main__":
    path = Path(sys.argv[1])
    print(station_analyse(path))