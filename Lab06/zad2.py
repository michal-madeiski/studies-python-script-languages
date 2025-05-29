import datetime as dt
import numpy as np

DATE_FORMAT = "%m/%d/%y %H:%M"

class TimeSeries:
    def __init__(self, idx_name, station_code, avrg_time, dates_list, values_list, unit):
        self.idx_name = idx_name
        self.station_code = station_code
        self.avrg_time = avrg_time
        self.dates_list = [dt.datetime.strptime(d, DATE_FORMAT) for d in dates_list]
        self.values_list = values_list
        self.unit = unit

    def __str__(self):
        return f"{self.idx_name}_{self.station_code}_{self.avrg_time}_{self.unit}: {list(zip(self.dates_list, self.values_list))}"

    def __repr__(self):
        return f"{self.station_code}_{self.idx_name}"

    def __getitem__(self, key: int | slice | dt.date | dt.datetime):
        if isinstance(key, (int, slice)):
            dates = self.dates_list[key]
            values = self.values_list[key]
            if isinstance(key, slice):
                return list(zip(dates, values))
            elif isinstance(key, int):
                return dates, values

        elif isinstance(key, (dt.date, dt.datetime)):
            values = self.values_list
            ret_values = []

            for i, d in enumerate(self.dates_list):
                if isinstance(key, dt.datetime):
                    if d == key:
                        ret_values.append(values[i])
                elif isinstance(key, dt.date):
                    if d.date() == key:
                        ret_values.append(values[i])

            if len(ret_values) == 1:
                return ret_values[0]
            else:
                return ret_values

        else:
            raise KeyError("Invalid key type, choose from: 'int', 'slice', 'datetime.datetime', 'datetime.date'")

    #zad3
    @property
    def mean(self):
        no_none_values = [v for v in self.values_list if v is not None]
        if self.values_list:
            return np.mean(no_none_values)
        else:
            return None

    @property
    def stddev(self):
        no_none_values = [v for v in self.values_list if v is not None]
        if self.values_list:
            return np.std(no_none_values)
        else:
            return None
    #zad3


if __name__ == "__main__":
    dates = ["01/01/23 12:00", "01/02/23 12:00", "01/03/23 12:00"]
    values = [1.57, 5.93, 5.93]
    ts = TimeSeries("As(PM10)", "DsOsieczow21", "24g", dates, values, "ng/m3")

    print(f"ts: {ts}")
    print(f"getitem idx: {ts.__getitem__(1)}")
    print(f"getitem slice: {ts.__getitem__(slice(0, 2))}")
    print(f"getitem date: {ts.__getitem__(dt.date(2023, 1, 1))}")
    print(f"getitem datetime: {ts.__getitem__(dt.datetime(2023, 1, 2, 12, 0))}")
    print(f"mean: {ts.mean}")
    print(f"stddev: {ts.stddev}")