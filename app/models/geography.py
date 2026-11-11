from .base import db, TimestampMixin, SoftDeleteMixin

class Country(db.Model, TimestampMixin, SoftDeleteMixin):
    __tablename__ = 'countries'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    iso_code = db.Column(db.String(3), unique=True, nullable=False)
    continent = db.Column(db.String(50), nullable=False)

    cities = db.relationship('City', backref='country', lazy='dynamic')

class City(db.Model, TimestampMixin, SoftDeleteMixin):
    __tablename__ = 'cities'
    id = db.Column(db.Integer, primary_key=True)
    country_id = db.Column(db.Integer, db.ForeignKey('countries.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    timezone = db.Column(db.String(50), nullable=False, default='UTC')

    airports = db.relationship('Airport', backref='city', lazy='dynamic')

class Airport(db.Model, TimestampMixin, SoftDeleteMixin):
    __tablename__ = 'airports'
    id = db.Column(db.Integer, primary_key=True)
    city_id = db.Column(db.Integer, db.ForeignKey('cities.id'), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    iata_code = db.Column(db.String(3), unique=True, nullable=False)
    icao_code = db.Column(db.String(4), unique=True, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    elevation_ft = db.Column(db.Integer, nullable=True)

    terminals = db.relationship('AirportTerminal', backref='airport', lazy='dynamic')
    runways = db.relationship('AirportRunway', backref='airport', lazy='dynamic')
    departing_routes = db.relationship('Route', foreign_keys='Route.origin_airport_id', backref='origin_airport', lazy='dynamic')
    arriving_routes = db.relationship('Route', foreign_keys='Route.destination_airport_id', backref='destination_airport', lazy='dynamic')

class AirportTerminal(db.Model, TimestampMixin, SoftDeleteMixin):
    __tablename__ = 'airport_terminals'
    id = db.Column(db.Integer, primary_key=True)
    airport_id = db.Column(db.Integer, db.ForeignKey('airports.id'), nullable=False)
    terminal_code = db.Column(db.String(20), nullable=False)  # T1, T2, Concourse A
    name = db.Column(db.String(100), nullable=False)

    gates = db.relationship('AirportGate', backref='terminal', lazy='dynamic')

class AirportGate(db.Model, TimestampMixin, SoftDeleteMixin):
    __tablename__ = 'airport_gates'
    id = db.Column(db.Integer, primary_key=True)
    terminal_id = db.Column(db.Integer, db.ForeignKey('airport_terminals.id'), nullable=False)
    gate_number = db.Column(db.String(20), nullable=False)  # A12, B5
    gate_type = db.Column(db.String(30), default='Domestic', nullable=False)  # Domestic, International, Regional

    departing_flight_instances = db.relationship('FlightInstance', foreign_keys='FlightInstance.departure_gate_id', backref='departure_gate', lazy='dynamic')
    arriving_flight_instances = db.relationship('FlightInstance', foreign_keys='FlightInstance.arrival_gate_id', backref='arrival_gate', lazy='dynamic')

class AirportRunway(db.Model, TimestampMixin, SoftDeleteMixin):
    __tablename__ = 'airport_runways'
    id = db.Column(db.Integer, primary_key=True)
    airport_id = db.Column(db.Integer, db.ForeignKey('airports.id'), nullable=False)
    runway_identifier = db.Column(db.String(10), nullable=False)  # e.g., 09L/27R
    length_ft = db.Column(db.Integer, nullable=False)
    surface_type = db.Column(db.String(50), default='Asphalt', nullable=False)
