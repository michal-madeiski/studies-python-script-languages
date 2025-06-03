import abc
from typing import List, Optional, Literal
from Lab06.zad2 import TimeSeries

class SeriesValidator(abc.ABC):
    @abc.abstractmethod
    def analyze(self, series: TimeSeries) -> List[str]:
        pass

class OutlierDetector(SeriesValidator):
    def __init__(self, k: float) -> None:
        self.k = k

    def analyze(self, series: TimeSeries) -> List[str]:
        anomalies: List[str] = []
        mean: Optional[float] = series.mean
        stddev: Optional[float] = series.stddev

        if mean is None or stddev is None:
            return anomalies

        no_none_values: List[float] = [v for v in series.values_list if v is not None]
        for i, v in enumerate(no_none_values):
            if abs(v - mean) > self.k * stddev:
                anomalies.append(f"Outlier ({self.k}*stddev from mean) detected at index {i}: {v}")

        return anomalies

class ZeroSpikeDetector(SeriesValidator):
    def analyze(self, series: TimeSeries) -> List[str]:
        anomalies: List[str] = []
        values: List[Optional[float]] = series.values_list
        counter: int = 0

        for i, v in enumerate(values):
            if v is None or v == 0:
                counter += 1
                if counter >= 3:
                    anomalies.append(f"Zero spike detected starting at index {i - 2}: three consecutive zeros/nones")
            else:
                counter = 0

        return anomalies

class ThresholdDetector(SeriesValidator):
    def __init__(self, threshold: float) -> None:
        self.threshold = threshold

    def analyze(self, series: TimeSeries) -> List[str]:
        anomalies: List[str] = []
        values: List[float] = [v for v in series.values_list if v is not None]

        for i, v in enumerate(values):
            if v > self.threshold:
                anomalies.append(f"Threshold ({self.threshold}) exceeded at index {i}: {v}")

        return anomalies

class CompositeValidator(SeriesValidator):
    def __init__(self, validators: List[SeriesValidator], mode: Literal["OR", "AND"] = "OR") -> None:
        self.validators = validators
        self.mode = mode

    def analyze(self, series: TimeSeries) -> List[str]:
        all_anomalies: List[List[str]] = []
        for validator in self.validators:
            anomalies: List[str] = validator.analyze(series)
            if anomalies:
                all_anomalies.append(anomalies)

        all_anomalies_flat = [elem for anomaly in all_anomalies for elem in anomaly]

        if self.mode == "OR": #correct if minimum one validator detected anomalies
            return all_anomalies_flat

        if self.mode == "AND": #correct if all validators detected anomalies
            if len(all_anomalies) == len(self.validators):
                return all_anomalies_flat
            else:
                return []


if __name__ == "__main__":
    dates = ["01/01/23 12:00", "01/02/23 12:00", "01/03/23 12:00"]
    #dates = ["01/01/23 12:00", "01/02/23 12:00", "01/03/23 12:00", "01/04/23 12:00", "01/05/23 12:00", "01/06/23 12:00"]
    values: List[Optional[float]] = [1.57, 5.93, 5.93]
    #values = [1.57, 5.93, 5.93, None, 0, 0.00]
    ts = TimeSeries("As(PM10)", "DsOsieczow21", "24g", dates, values, "ng/m3")

    od = OutlierDetector(1)
    print(f"outlier: {od.analyze(ts)}")

    zs = ZeroSpikeDetector()
    print(f"zerospike: {zs.analyze(ts)}")

    th = ThresholdDetector(3)
    print(f"threshold: {th.analyze(ts)}")

    cvOR = CompositeValidator([od, zs, th], mode="OR")
    print(f"composite OR: {cvOR.analyze(ts)}")

    cvAND = CompositeValidator([od, zs, th], mode="AND")
    print(f"composite AND: {cvAND.analyze(ts)}")