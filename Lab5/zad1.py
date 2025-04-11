import csv
import sys

station_data_file = "stacje.csv"

def transpose(reader):
    rows = list(reader)
    transposed = zip(*rows)
    return [list(row) for row in transposed]

def csv_parser(file, delimiter=",", encoding="utf-8"):
    with open(file, encoding=encoding) as csvfile:
        dict_reader = csv.DictReader(csvfile, delimiter=delimiter)
        if file != station_data_file:
            dict_list = []
            reader = transpose(csv.reader(csvfile, delimiter=delimiter))
            for col in reader[1:]:
                temp_dict = {}
                for i in range(len(reader[0])):
                    temp_dict[reader[0][i]] = col[i]
                dict_list.append(temp_dict)
            return dict_list
        return list(dict_reader)

if __name__ == "__main__":
    file = sys.argv[1]
    delimiter = sys.argv[2] if len(sys.argv) > 2 else ","
    encoding = sys.argv[3] if len(sys.argv) > 3 else "utf-8"
    print(csv_parser(file, delimiter, encoding))