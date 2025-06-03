import pytest
import numpy as np
import pandas as pd
import datetime as dt
from typing import Optional, List
from Lab06.zad1 import Station
from Lab06.zad2 import TimeSeries
from Lab06.zad4 import OutlierDetector, ZeroSpikeDetector, ThresholdDetector
from Lab06.zad5 import Measurements

# a - Station __eq__ test
@pytest.fixture
def station_sample():
    return {
        "nr": 1,
        "station_code": "ABC123",
        "international_code": None,
        "name": "Stacja Testowa",
        "old_station_code": None,
        "start_date": "2000-01-01",
        "end_date": "2010-01-01",
        "station_type": "XYZ",
        "area_type": "miejski",
        "station_kind": "kontenerowa",
        "voivode": "MAZOWIECKIE",
        "city": "Warszawa",
        "addr": "ul. Testowa 1",
        "geo_height": 52.2297,
        "geo_width": 21.0122,
    }

def test_eq_same_station_code(station_sample):
    station1 = Station(**station_sample)
    station2 = Station(**station_sample)
    assert station1.__eq__(station2)

def test_eq_different_station_code(station_sample):
    station1 = Station(**station_sample)
    station_sample["station_code"] = "XYZ789"
    station2 = Station(**station_sample)
    assert not station1.__eq__(station2)
# a - Station __eq__ test

# b - TimeSeries __getitem__ test
@pytest.fixture
def timeseries_sample():
    dates = ["01/01/23 12:00", "01/02/23 12:00", "01/03/23 12:00"]
    values: List[Optional[float]] = [1.57, 5.93, 5.93]
    return TimeSeries("As(PM10)", "DsOsieczow21", "24g", dates, values, "ng/m3")

def test_getitem_by_index(timeseries_sample):
    date, value = timeseries_sample.__getitem__(1)
    assert date == dt.datetime(2023, 1, 2, 12, 0)
    assert value == 5.93

def test_getitem_by_slice(timeseries_sample):
    result = timeseries_sample.__getitem__(slice(0, 2))
    assert len(result) == 2
    assert result[0][0] == dt.datetime(2023, 1, 1, 12, 0)
    assert result[1][1] == 5.93

def test_getitem_by_existing_date(timeseries_sample):
    result = timeseries_sample.__getitem__(dt.date(2023, 1, 1))
    assert result == 1.57

def test_getitem_by_non_existing_date(timeseries_sample):
    result = timeseries_sample.__getitem__(dt.date(2025, 1, 1))
    assert result == []

def test_getitem_by_existing_datetime(timeseries_sample):
    result = timeseries_sample.__getitem__(dt.datetime(2023, 1, 3, 12, 0))
    assert result == 5.93

def test_getitem_by_non_existing_datetime(timeseries_sample):
    result = timeseries_sample.__getitem__(dt.datetime(2025, 1, 3, 12, 0))
    assert result == []
# b - TimeSeries __getitem__ test

# c - TimeSeries mean and stddev test
@pytest.fixture
def timeseries_sample_with_none():
    dates = ["01/01/23 12:00", "01/02/23 12:00", "01/03/23 12:00", "01/04/23 12:00"]
    values: List[Optional[float]] = [1.0, None, 3.0, None]
    return TimeSeries("As(PM10)", "DsOsieczow21", "24g", dates, values, "ng/m3")

def test_mean(timeseries_sample):
    expected_mean = (1.57 + 5.93 + 5.93) / 3
    assert timeseries_sample.mean == pytest.approx(expected_mean)

def test_stddev(timeseries_sample):
    expected_std = float(np.std([1.57, 5.93, 5.93]))
    assert timeseries_sample.stddev == pytest.approx(expected_std)

def test_mean_with_none(timeseries_sample_with_none):
    expected_mean = (1.0 + 3.0) / 2
    assert timeseries_sample_with_none.mean == pytest.approx(expected_mean)

def test_stddev_with_none(timeseries_sample_with_none):
    expected_std = float(np.std([1.0, 3.0]))
    assert timeseries_sample_with_none.stddev == pytest.approx(expected_std)
# c - TimeSeries mean and stddev test

# d - OutlierDetector test
@pytest.fixture
def timeseries_with_outlier():
    dates = ["01/01/23 12:00", "01/02/23 12:00", "01/03/23 12:00"]
    values: List[Optional[float]] = [1.0, 100.0, 2.0]
    return TimeSeries("As(PM10)", "DsOsieczow21", "24g", dates, values, "ng/m3")

def test_outlier_detector(timeseries_with_outlier):
    od = OutlierDetector(k=1)
    anomalies = od.analyze(timeseries_with_outlier)
    assert any("Outlier" in a for a in anomalies)
    assert any("index 1" in a for a in anomalies)
# d - OutlierDetector test

# e - ZeroSpikeDetector test
@pytest.fixture
def timeseries_with_zero_spike():
    dates = ["01/01/23 12:00", "01/02/23 12:00", "01/03/23 12:00", "01/04/23 12:00", "01/05/23 12:00"]
    values: List[Optional[float]] = [1.0, 0.0, None, 0.0, 5.0]
    return TimeSeries("As(PM10)", "DsOsieczow21", "24g", dates, values, "ng/m3")

def test_zero_spike_detector(timeseries_with_zero_spike):
    zs = ZeroSpikeDetector()
    anomalies = zs.analyze(timeseries_with_zero_spike)
    assert any("Zero spike detected" in a for a in anomalies)
    assert any("index 1" in a for a in anomalies)
# e - ZeroSpikeDetector test

# f - ThresholdDetector test
@pytest.fixture
def timeseries_with_threshold():
    dates = ["01/01/23 12:00", "01/02/23 12:00", "01/03/23 12:00"]
    values: List[Optional[float]] = [2.0, 4.5, 1.0]
    return TimeSeries("As(PM10)", "DsOsieczow21", "24g", dates, values, "ng/m3")

def test_threshold_detector(timeseries_with_threshold):
    th = ThresholdDetector(threshold=3)
    anomalies = th.analyze(timeseries_with_threshold)
    assert any("Threshold" in a for a in anomalies)
    assert any("index 1" in a for a in anomalies)
# f - ThresholdDetector test

# g - Measurements detect_all_anomalies test
@pytest.fixture
def csv_sample(tmp_path):
    content = {
        "Data": ["", "", "", "", "", "01/01/23 12:00", "01/02/23 12:00", "01/03/23 12:00"],
        "station1": ["DsTest", "", "", "", "ng/m3", 1.0, 100.0, 2.0]
    }
    path = tmp_path / "2023_As(PM10)_24g.csv"
    pd.DataFrame(content).to_csv(path, index=False)
    return tmp_path

@pytest.mark.parametrize("validator", [
    OutlierDetector(k=1),
    ZeroSpikeDetector(),
    ThresholdDetector(threshold=10),
])
def test_detect_all_anomalies(validator, csv_sample):
    measurements = Measurements(str(csv_sample))
    measurements.get_by_parameter("As(PM10)")

    results = measurements.detect_all_anomalies([validator], preload=False)

    for ts, messages in results.items():
        assert callable(getattr(ts, "__getitem__", None))
        assert getattr(ts, "mean", None) is not None
        assert getattr(ts, "stddev", None) is not None

        try:
            for msg in messages:
                assert "detected" in msg or "exceeded" in msg
        except TypeError:
            pytest.fail("messages is not iterable")
# g - Measurements detect_all_anomalies test