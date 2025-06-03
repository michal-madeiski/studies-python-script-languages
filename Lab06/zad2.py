import datetime as dt
import numpy as np
from typing import Optional, Union, List, Tuple

DATE_FORMAT = "%m/%d/%y %H:%M"

class TimeSeries:
    dates_list: List[dt.datetime]
    values_list: List[Optional[float]]

    def __init__(
            self,
            idx_name: str,
            station_code: str,
            avrg_time: str,
            dates_list: List[str],
            values_list: List[Optional[float]],
            unit: str
    ) -> None:
        self.idx_name = idx_name
        self.station_code = station_code
        self.avrg_time = avrg_time
        self.dates_list = [dt.datetime.strptime(d, DATE_FORMAT) for d in dates_list]
        self.values_list = values_list
        self.unit = unit

    def __str__(self) -> str:
        return f"{self.idx_name}_{self.station_code}_{self.avrg_time}_{self.unit}: {list(zip(self.dates_list, self.values_list))}"

    def __repr__(self) -> str:
        return f"{self.station_code}_{self.idx_name}"

    def __getitem__(self, key: int | slice | dt.date | dt.datetime) -> Union[
        Tuple[dt.datetime, Optional[float]],
        List[Tuple[dt.datetime, Optional[float]]],
        Optional[float],
        List[Optional[float]]
    ]:
        if isinstance(key, (int, slice)):
            if isinstance(key, slice):
                dates: List[dt.datetime] = self.dates_list[key]
                values: List[Optional[float]] = self.values_list[key]
                return list(zip(dates, values))
            elif isinstance(key, int):
                date: dt.datetime = self.dates_list[key]
                value: Optional[float] = self.values_list[key]
                return (date, value)

        elif isinstance(key, (dt.date, dt.datetime)):
            values = self.values_list
            ret_values: List[Optional[float]] = []

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
    def mean(self) -> Optional[float]:
        no_none_values = [v for v in self.values_list if v is not None]
        if self.values_list:
            return float(np.mean(no_none_values))
        return None

    @property
    def stddev(self) -> Optional[float]:
        no_none_values = [v for v in self.values_list if v is not None]
        if self.values_list:
            return float(np.std(no_none_values))
        return None
    #zad3


if __name__ == "__main__":
    dates = ["01/01/23 12:00", "01/02/23 12:00", "01/03/23 12:00"]
    values: List[Optional[float]] = [1.57, 5.93, 5.93]
    ts = TimeSeries("As(PM10)", "DsOsieczow21", "24g", dates, values, "ng/m3")

    print(f"ts: {ts}")
    print(f"getitem idx: {ts.__getitem__(1)}")
    print(f"getitem slice: {ts.__getitem__(slice(0, 2))}")
    print(f"getitem date: {ts.__getitem__(dt.date(2023, 1, 1))}")
    print(f"getitem datetime: {ts.__getitem__(dt.datetime(2023, 1, 2, 12, 0))}")
    print(f"mean: {ts.mean}")
    print(f"stddev: {ts.stddev}")