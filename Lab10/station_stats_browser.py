import os
import sys
from PySide6.QtWidgets import (QApplication, QLineEdit, QLabel, QVBoxLayout, QWidget, QFormLayout, QComboBox)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from style import style
from models import Rental, Station

os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = os.path.join(sys.prefix, "Lib", "site-packages", "PySide6", "plugins", "platforms")

class StationStatsBrowser(QWidget):
    def __init__(self, db_name):
        super().__init__()
        self.resize(800, 250)
        self.setWindowIcon(QIcon("station_icon.png"))
        self.setWindowTitle("Statystyki stacji rowerowych")

        engine = create_engine(f"sqlite:///{db_name}.sqlite3", echo=False)
        Session = sessionmaker(bind=engine)
        self.session = Session()

        self.stations_combo_box = QComboBox()
        self.load_stations()

        # name: name of station
        self.name = QLineEdit(""); self.name.setReadOnly(True); self.name.setProperty("class", "station_info")
        # a: avg time of ride (station is rental station)
        self.a = QLineEdit(""); self.a.setReadOnly(True); self.a.setProperty("class", "station_info")
        # b: avg time of ride (station is return station)
        self.b = QLineEdit(""); self.b.setReadOnly(True); self.b.setProperty("class", "station_info")
        # c: number of different bikes parked at station
        self.c = QLineEdit(""); self.c.setReadOnly(True); self.c.setProperty("class", "station_info")
        # d: min time(H:M) of rental
        self.d = QLineEdit(""); self.d.setReadOnly(True); self.d.setProperty("class", "station_info")
        # e: max time(H:M) of rental
        self.e = QLineEdit(""); self.e.setReadOnly(True); self.e.setProperty("class", "station_info")

        self.stations_combo_box.currentTextChanged.connect(self.show_stats)
        self.setStyleSheet(style)
        self.create_gui()

    def create_gui(self):
        main_layout = QVBoxLayout()

        # info_layout
        info_layout = QVBoxLayout()

        info_label = QLabel("Wybierz stację z listy"); info_label.setAlignment(Qt.AlignCenter)
        info_layout.addWidget(info_label)
        info_layout.addWidget(self.stations_combo_box)
        # info_layout

        # stats_layout
        stats_layout = QFormLayout()

        name_label = QLabel("Nazwa stacji: "); name_label.setProperty("class", "station_info")
        stats_layout.addRow(name_label, self.name)

        a_label = QLabel("Śr. czas przejazdu (start na stacji): "); a_label.setProperty("class", "station_info")
        stats_layout.addRow(a_label, self.a)

        b_label = QLabel("Śr. czas przejazdu (koniec na stacji): "); b_label.setProperty("class", "station_info")
        stats_layout.addRow(b_label, self.b)

        c_label = QLabel("Liczba różnych rowerów parkowanych na stacji: "); c_label.setProperty("class", "station_info")
        stats_layout.addRow(c_label, self.c)

        d_label = QLabel("Najwcześniejsza godzina wypożyczenia: "); d_label.setProperty("class", "station_info")
        stats_layout.addRow(d_label, self.d)

        e_label = QLabel("Najpóźniejsza godzina wypożyczenia: "); e_label.setProperty("class", "station_info")
        stats_layout.addRow(e_label, self.e)
        # stats_layout

        main_layout.addLayout(info_layout)
        main_layout.addLayout(stats_layout)

        self.setLayout(main_layout)

    def load_stations(self):
        stations = self.session.query(Station).order_by(Station.station_name).all()
        for i, station in enumerate(stations):
            self.stations_combo_box.addItem(str(station.station_name), str(station.station_id))
        self.stations_combo_box.setCurrentIndex(-1)

    def show_stats(self):
        station_id = self.stations_combo_box.currentData()
        a = self.session.query(func.avg(Rental.time_in_minutes)).filter(Rental.rental_station_id == station_id).scalar()
        b = self.session.query(func.avg(Rental.time_in_minutes)).filter(Rental.return_station_id == station_id).scalar()
        c = self.session.query(func.count(func.distinct(Rental.bike_number))).filter(Rental.return_station_id == station_id).scalar()
        d = self.session.query(func.min(func.strftime("%H:%M", Rental.start_time))).filter(Rental.rental_station_id == station_id).scalar()
        e = self.session.query(func.max(func.strftime("%H:%M", Rental.start_time))).filter(Rental.rental_station_id == station_id).scalar()

        self.name.setText(self.stations_combo_box.currentText())
        self.a.setText(f"{a:.2f}") if a is not None else self.a.setText("Brak danych")
        self.b.setText(f"{b:.2f}") if b is not None else self.b.setText("Brak danych")
        self.c.setText(str(c))
        self.d.setText(str(d)) if d is not None else self.d.setText("Brak danych")
        self.e.setText(str(e)) if e is not None else self.e.setText("Brak danych")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    browser = StationStatsBrowser(db_name="bikes")
    browser.show()
    sys.exit(app.exec())