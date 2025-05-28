import csv
import sys
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from sqlalchemy import create_engine
from models import Rental, Station

def get_station_id(session, station_name):
    station = session.query(Station).filter(Station.station_name == station_name).first()
    if not station:
        station = Station(station_name=station_name)
        session.add(station)
        session.flush()
    return station.station_id

def load_data(csv_file, db_name):
    engine = create_engine(f"sqlite:///{db_name}.sqlite3", echo=False)
    Session = sessionmaker(bind=engine)
    session = Session()

    with open(csv_file, encoding="utf-8") as file:
        reader = csv.DictReader(file)

        prev_rental_id = None
        for row in reader:
            rental_id = row["UID wynajmu"]
            if rental_id == prev_rental_id:
                continue

            rental = Rental(
                rental_id=rental_id,
                bike_number=row["Numer roweru"],
                start_time=datetime.strptime(row["Data wynajmu"], "%Y-%m-%d %H:%M:%S"),
                end_time=datetime.strptime(row["Data zwrotu"], "%Y-%m-%d %H:%M:%S"),
                rental_station_id=get_station_id(session, row["Stacja wynajmu"]),
                return_station_id=get_station_id(session, row["Stacja zwrotu"]),
                time_in_minutes=row["Czas trwania"]
            )

            prev_rental_id = rental_id
            session.add(rental)
        session.commit()
    session.close()

def print_db(db_name):
    engine = create_engine(f"sqlite:///{db_name}.sqlite3", echo=False)
    Session = sessionmaker(bind=engine)
    session = Session()

    stations = session.query(Station).all()
    for station in stations:
        print(station)

    # rentals = session.query(Rental).all()
    # for rental in rentals:
    #     print(rental)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: load_data.py <csv_file> <db_name>")
        sys.exit(1)
    csv_file = sys.argv[1]
    db_name = sys.argv[2]
    load_data(csv_file=csv_file, db_name=db_name)
    print_db(db_name=db_name)