import os
import pandas as pd #type: ignore
from typing import Dict, Any
from zad4 import *

class Measurements:
    def __init__(self, dir_path: str) -> None:
        self.dir_path: str = dir_path
        self._files_: List[Dict[str, str]] = self.identify_files()
        self._loaded_files: Dict[str, List[TimeSeries]] = {}

    def identify_files(self) -> List[Dict[str, str]]:
        ret_files: List[Dict[str, str]] = []

        for filename in os.listdir(self.dir_path):
            if filename.endswith(".csv"):
                filename_split = filename[:-4].split("_")
                if len(filename_split) == 3:
                    year = filename_split[0]
                    idx_name = filename_split[1]
                    freq = filename_split[2]
                    ret_files.append({
                        "filename": filename,
                        "year": year,
                        "idx_name": idx_name,
                        "freq": freq,
                    })

        return ret_files

    def lazy_load_file(self, filename: str) -> List[TimeSeries]:
        ts_list: List[TimeSeries] = []

        filepath = os.path.join(self.dir_path, filename)
        df: pd.DataFrame = pd.read_csv(filepath, low_memory=False)

        filename_split = filename[:-4].split("_")
        year = filename_split[0]
        idx_name = filename_split[1]
        freq = filename_split[2]

        dates_list: List[str] = df[df.columns[0]].iloc[5:].astype(str).tolist()

        for station_column in df.columns[1:]:
            values_list: List[Optional[float]] = df[station_column].iloc[5:].astype(float).tolist()

            ts = TimeSeries(
                idx_name=idx_name,
                station_code=df[station_column].iloc[0],
                avrg_time=freq,
                dates_list=dates_list,
                values_list=values_list,
                unit=df[station_column].iloc[4]
            )

            ts_list.append(ts)

        return ts_list

    def __len__(self) -> int:
        count: int = 0
        for f in self._files_:
            filepath = os.path.join(self.dir_path, f["filename"])
            df: pd.DataFrame = pd.read_csv(filepath, nrows=1)
            count += len(df.columns) - 1
        return count

    def __contains__(self, parameter_name: str) -> bool:
        for f in self._files_:
            if f["idx_name"] == parameter_name:
                return True
        return False

    def get_by_parameter(self, param_name: str) -> List[TimeSeries]:
        if param_name in self._loaded_files:
            return self._loaded_files[param_name]

        result: List[TimeSeries] = []
        for f in self._files_:
            if f["idx_name"] == param_name:
                result.extend(self.lazy_load_file(f["filename"]))

        if param_name in self._loaded_files:
            self._loaded_files[param_name].extend(result)
        else:
            self._loaded_files[param_name] = result

        return result

    def get_by_station(self, station_code: str) -> List[TimeSeries]:
        result: List[TimeSeries] = []

        for idx_name in self._loaded_files:
            for ts in self._loaded_files[idx_name]:
                if ts.station_code == station_code:
                    result.append(ts)

        other_files: List[Dict[str, str]] = [f for f in self._files_ if f["idx_name"] not in self._loaded_files]

        for f in other_files:
            f_res: List[TimeSeries] = []
            file_series: List[TimeSeries] = self.lazy_load_file(f["filename"])
            f_idx_name: str = f["idx_name"]

            for ts in file_series:
                if ts.station_code == station_code:
                    f_res.append(ts)
                    result.append(ts)
            if f_idx_name in self._loaded_files:
                self._loaded_files[f_idx_name].extend(f_res)
            else:
                self._loaded_files[f_idx_name] = f_res

        return result

    #zad6
    def detect_all_anomalies(self, validators: List[SeriesValidator], preload: bool = False) -> Dict[TimeSeries, List[Any]]:
        anomalies: Dict[TimeSeries, List[Any]] = {}

        if preload:
            for f in self._files_:
                self.get_by_parameter(f["idx_name"])

        for file in self._loaded_files:
            for ts in self._loaded_files[file]:
                series_anomalies: List[Any] = []
                for validator in validators:
                    series_anomalies.extend(validator.analyze(ts))
                if series_anomalies:
                    anomalies[ts] = series_anomalies

        return anomalies
    #zad6

    def print_loaded(self) -> None:
        print(self._loaded_files)


if __name__ == "__main__":
    #zad7
    measurements = Measurements("../Lab05/measurements/")

    get_by_param = measurements.get_by_parameter("As(PM10)")
    get_by_station = measurements.get_by_station("DsOsieczow21")

    outlier_detector = OutlierDetector(k=5)
    zero_spike_detector = ZeroSpikeDetector()
    threshold_detector = ThresholdDetector(threshold=15)

    validators = [outlier_detector, zero_spike_detector, threshold_detector]

    measurements.print_loaded()
    print(measurements.detect_all_anomalies(validators, preload=False))
    #zad7