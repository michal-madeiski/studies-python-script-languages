from datetime import datetime
from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, DeclarativeBase, relationship
from sqlalchemy.testing.schema import mapped_column

class Base(DeclarativeBase):
    pass

class Rental(Base):
    __tablename__ = "Rentals"
    rental_id: Mapped[str] = mapped_column(String(50), primary_key=True)
    bike_number: Mapped[str] = mapped_column(String(50))
    start_time: Mapped[datetime] = mapped_column(DateTime)
    end_time: Mapped[datetime] = mapped_column(DateTime)
    time_in_minutes: Mapped[int] =mapped_column()

    # foreign_keys
    rental_station_id: Mapped[int] = mapped_column(ForeignKey("Stations.station_id"))
    return_station_id: Mapped[int] = mapped_column(ForeignKey("Stations.station_id"))
    # foreign_keys

    # relationships
    station_start: Mapped["Station"] = relationship(back_populates="rentals_start", foreign_keys=[rental_station_id])
    station_end: Mapped["Station"] = relationship(back_populates="rentals_end", foreign_keys=[return_station_id])
    # relationships

    def __repr__(self):
        return f"Rental(rental_id={self.rental_id!r}, bike_number={self.bike_number!r}, start_time={self.start_time!r}, end_time={self.end_time!r}, rental_station_id={self.rental_station_id!r}, return_station_id={self.return_station_id!r}, time_in_minutes={self.time_in_minutes!r})"

class Station(Base):
    __tablename__ = "Stations"
    station_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    station_name: Mapped[str] = mapped_column(String(100), nullable=False)

    # relationships
    rentals_start: Mapped[list["Rental"]] = relationship(back_populates="station_start", foreign_keys="Rental.rental_station_id")
    rentals_end: Mapped[list["Rental"]] = relationship(back_populates="station_end", foreign_keys="Rental.return_station_id")
    # relationships

    def __repr__(self):
        return f"Station(station_id={self.station_id!r}, station_name={self.station_name!r})"