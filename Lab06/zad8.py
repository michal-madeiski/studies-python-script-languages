from zad4 import *

class SimpleReporter:
    def analyze(self, series: TimeSeries):
        return [f"Duck info: station={series.station_code}; mean={series.mean}; stddev={series.stddev}"]


if __name__ == "__main__":
    dates = ["01/01/23 12:00", "01/02/23 12:00", "01/03/23 12:00"]
    values = [1.57, 5.93, 5.93]
    ts = TimeSeries("As(PM10)", "DsOsieczow21", "24g", dates, values, "ng/m3")

    validators = [OutlierDetector(1), ZeroSpikeDetector(), ThresholdDetector(3), SimpleReporter()]

    for v in validators:
        print(f"{v.__class__.__name__}: {v.analyze(ts)}")