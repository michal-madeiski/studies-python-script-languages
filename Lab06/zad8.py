from typing import Any
from zad4 import *

class SimpleReporter:
    def analyze(self, series: TimeSeries) -> List[str]:
        return [f"Duck info: station={series.station_code}; mean={series.mean}; stddev={series.stddev}"]


if __name__ == "__main__":
    datess: List[str] = ["01/01/23 12:00", "01/02/23 12:00", "01/03/23 12:00"]
    valuess: List[Optional[float]] = [1.57, 5.93, 5.93]
    tss: TimeSeries = TimeSeries("As(PM10)", "DsOsieczow21", "24g", datess, valuess, "ng/m3")

    validators: List[Any] = [OutlierDetector(1), ZeroSpikeDetector(), ThresholdDetector(3), SimpleReporter()]

    for v in validators:
        print(f"{v.__class__.__name__}: {v.analyze(tss)}")