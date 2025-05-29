import argparse
import sys
import random
import logging
import pandas as pd
from pathlib import Path
from datetime import datetime
from zad1 import csv_parser
from zad2 import group_measurement_files_by_key

#logger config
logging.basicConfig(encoding="uf8", level=logging.DEBUG)
logger = logging.getLogger("__name__")
formatter_out = logging.Formatter("%(asctime)s%(levelname)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S ")
formatter_err = logging.Formatter("%(asctime)s!%(levelname)s!: %(message)s", datefmt="%Y-%m-%d %H:%M:%S ")
logger.propagate = False

stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.DEBUG)
stdout_handler.addFilter(lambda log: log.levelno < logging.ERROR)
stdout_handler.setFormatter(formatter_out)

stderr_handler = logging.StreamHandler(sys.stderr)
stderr_handler.setLevel(logging.ERROR)
stderr_handler.setFormatter(formatter_err)

logger.addHandler(stdout_handler)
logger.addHandler(stderr_handler)
#logger config

#const strings
station_const = "stacje.csv"
code_const = "Kod stacji"
addr_const = "Adres"
name_const = "Nazwa stacji"
#const strings

def find_measurement_file(measurements_dict, size, freq):
    for key, val in measurements_dict.items():
        year, k_size, k_freq = key
        if k_size == size and k_freq == freq:
            return val
    logger.warning(f"Station with size of measurement: {size} and frequency: {freq} does not exist in given file")
    return None

def df_stations(path: Path, size, freq):
    try:
        dict_measurements = group_measurement_files_by_key(path)
        measurement_file = find_measurement_file(dict_measurements, size, freq)

        if measurement_file is None:
            return None
        try:
            logger.info(f"File opened: {measurement_file}")
            with open(measurement_file, "rb") as f:
                data = f.read()
                logger.debug(f"Bytes read: {len(data)}")
            logger.info(f"File closed: {measurement_file}")

            df = pd.read_csv(measurement_file, skiprows=[0, 2, 3, 4, 5])
            df.rename(columns={code_const: "Data"}, inplace=True)
            df.set_index("Data", inplace=True)

            return df
        except FileNotFoundError:
            logger.error(f"File: {measurement_file} does not exist")
            return None
    except FileNotFoundError:
        logger.error(f"Path: {path} is incorrect")
        return None

def random_station(df: pd.DataFrame, start, end):
    # Inicjalizacja pustego słownika do przechowywania wyników
    station_list = []

    for station in df.columns:
        # Sprawdzanie, które daty mają pomiar (czyli różne od NaN)
        valid_dates = df.index[df[station].notna()].tolist()
        min_date = min(valid_dates)
        max_date = max(valid_dates)

        min_date_to_form = datetime.strptime(min_date, '%m/%d/%y %H:%M')
        max_date_to_form = datetime.strptime(max_date, '%m/%d/%y %H:%M')

        formatted_min_date = min_date_to_form.strftime('%Y-%m-%d')
        formatted_max_date = max_date_to_form.strftime('%Y-%m-%d')

        if formatted_min_date >= start and formatted_max_date <= end:
            station_list.append((station, formatted_min_date, formatted_max_date))

    if len(station_list) == 0:
        logger.warning("No measurements in given date range")
        return None
    rd = random.randint(0, len(station_list) - 1)
    station_code = station_list[rd][0]

    all_station_list = csv_parser(station_const)
    for stat in all_station_list:
        if stat.get(code_const) == station_code:
            return stat.get(name_const), stat.get(addr_const)

def given_station_stats(df: pd.DataFrame, station, start, end):
    start = datetime.strptime(start, "%Y-%m-%d")
    end = datetime.strptime(end, "%Y-%m-%d")

    formatted_start = start.strftime("%m/%d/%Y 00:00")
    formatted_end = end.strftime("%m/%d/%Y 23:59")

    df = df.loc[formatted_start:formatted_end]

    for stat in df.columns:
        if stat == station:
            return df[station].mean(), df[station].std()
    logger.warning(f"Name of station: {station} does not match given arguments")
    return None, None

def parse_arguments():
    parser = argparse.ArgumentParser(description="Script for analyze measurement data from CSV files.")

    parser.add_argument("path", type=str, help="Path to the directory with measurement files.")
    parser.add_argument("measurement_size", type=str, help="Size of measurement (PM2.5, PM10, NO, etc.).")
    parser.add_argument("frequency", type=str, choices=["1g", "24g"], help="Frequency of measurement.")
    parser.add_argument("start_date", type=str, help="Start date: YYYY-MM-DD.")
    parser.add_argument("end_date", type=str, help="End date: YYYY-MM-DD.")

    subparsers = parser.add_subparsers(dest="subcommand", help="Subcommands of script.")

    subparsers.add_parser("rand", help="Name and address of random station from given: measurement size, frequency, date range.")

    stats_parser = subparsers.add_parser("stats", help="Average and standard deviation of given station.")
    stats_parser.add_argument("station", type=str, help="Name of the station.")

    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()

    path = Path(args.path)
    size = args.measurement_size
    freq = args.frequency
    start = args.start_date
    end = args.end_date

    df = df_stations(path, size, freq)
    if df is None:
        logger.warning("Failed to load measurement data")

    else:
        if args.subcommand == "rand":
            info = random_station(df, start, end)
            if info is not None:
                print(f"station: {info[0]}; address: {info[1]}")

        elif args.subcommand == "stats":
            if args.station is None:
                logger.warning("Name of station is required")

            else:
                station = args.station
                mean, std = given_station_stats(df, station, start, end)
                if (mean, std) != (None, None):
                    print(f"station: {station}; mean = {mean}; standard deviation = {std}")

        else:
            logger.warning("Subcommand is required (rand/stats)")