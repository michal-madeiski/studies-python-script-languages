class Station:
    def __init__(self, nr, station_code, international_code, name, old_station_code,
                 start_date, end_date, station_type, area_type, station_kind, voivode,
                 city, addr, geo_height, geo_width):
        self.nr = nr
        self.station_code = station_code
        self.international_code = international_code
        self.name = name
        self.old_station_code = old_station_code
        self.start_date = start_date
        self.end_date = end_date
        self.station_type = station_type
        self.area_type = area_type
        self.station_kind = station_kind
        self.voivode = voivode
        self.city = city
        self.addr = addr
        self.geo_height = geo_height
        self.geo_width = geo_width

    def __str__(self):
        return f"{self.station_code} - {self.name}: {self.city}, {self.addr}"

    def __repr__(self):
        return f"""Station(nr={self.nr!r}, station_code={self.station_code!r}, international_code={self.international_code!r}, 
        name={self.name!r}, old_station_code={self.old_station_code!r}, start_date={self.start_date!r}, 
        end_date={self.end_date!r}, station_type={self.station_type!r}, area_type={self.area_type!r},
        station_kind={self.station_kind!r}, voivode={self.voivode!r}, city={self.city!r}, addr={self.addr!r},
        geo_height={self.geo_height!r}, geo_width={self.geo_width!r})"""

    def __eq__(self, other):
        if isinstance(other, Station):
            return self.station_code == other.station_code
        return False


if __name__ == "__main__":
    stat1 = Station(1, "DSBialka", None, "Białka", None, "1990-01-03",
                    "2005-12-31", "przemysłowa", "podmiejski", "kontenerowa stacjonarna",
                    "DOLNOŚLĄSKIE", "Białka", None, 51.197783, 16.117390)
    stat2 = Station(2, "DSBialka", None, "Białka", None, "1990-01-03",
                    "2005-12-31", "przemysłowa", "podmiejski", "kontenerowa stacjonarna",
                    "DOLNOŚLĄSKIE", "Białka", None, 51.197783, 16.117390)

    print(f"str: {stat1.__str__()}")
    print(f"repr: {stat1.__repr__()}")
    print(f"eq: {stat1.__eq__(stat2)}")