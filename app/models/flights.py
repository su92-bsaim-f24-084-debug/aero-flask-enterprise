from .base import db, TimestampMixin, SoftDeleteMixin

class Route(db.Model, TimestampMixin, SoftDeleteMixin):
    __tablename__ = 'routes'
    id = db.Column(db.Integer, primary_key=True)
    origin_airport_id = db.Column(db.Integer, db.ForeignKey('airports.id'), nullable=False)
    destination_airport_id = db.Column(db.Integer, db.ForeignKey('airports.id'), nullable=False)
    distance_km = db.Column(db.Float, nullable=False)
    estimated_flight_minutes = db.Column(db.Integer, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    schedules = db.relationship('FlightSchedule', backref='route', lazy='dynamic')

class FlightSchedule(db.Model, TimestampMixin, SoftDeleteMixin):
    __tablename__ = 'flight_schedules'
    id = db.Column(db.Integer, primary_key=True)
    route_id = db.Column(db.Integer, db.ForeignKey('routes.id'), nullable=False)
    flight_number = db.Column(db.String(10), unique=True, nullable=False)  # e.g., AF-101
    scheduled_departure_time = db.Column(db.Time, nullable=False)
    scheduled_arrival_time = db.Column(db.Time, nullable=False)
    days_of_week = db.Column(db.String(30), default='Daily', nullable=False)  # Daily, Mon/Wed/Fri

    flight_instances = db.relationship('FlightInstance', backref='schedule', lazy='dynamic')

class FlightInstance(db.Model, TimestampMixin, SoftDeleteMixin):
    __tablename__ = 'flight_instances'
    id = db.Column(db.Integer, primary_key=True)
    schedule_id = db.Column(db.Integer, db.ForeignKey('flight_schedules.id'), nullable=False)
    aircraft_id = db.Column(db.Integer, db.ForeignKey('aircrafts.id'), nullable=False)
    departure_gate_id = db.Column(db.Integer, db.ForeignKey('airport_gates.id'), nullable=True)
    arrival_gate_id = db.Column(db.Integer, db.ForeignKey('airport_gates.id'), nullable=True)
    flight_date = db.Column(db.Date, nullable=False)
    actual_departure_time = db.Column(db.DateTime, nullable=True)
    actual_arrival_time = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(30), default='Scheduled', nullable=False)  # Scheduled, Boarding, Departed, Landed, Delayed, Cancelled

    status_histories = db.relationship('FlightStatusHistory', backref='flight_instance', lazy='dynamic')
    delay_logs = db.relationship('FlightDelayLog', backref='flight_instance', lazy='dynamic')
    fuel_logs = db.relationship('FlightFuelLog', backref='flight_instance', lazy='dynamic')
    crew_schedules = db.relationship('CrewSchedule', backref='flight_instance', lazy='dynamic')
    flight_prices = db.relationship('FlightPrice', backref='flight_instance', lazy='dynamic')
    tickets = db.relationship('Ticket', backref='flight_instance', lazy='dynamic')
    seat_reservations = db.relationship('SeatReservation', backref='flight_instance', lazy='dynamic')

class FlightStatusHistory(db.Model, TimestampMixin, SoftDeleteMixin):
    __tablename__ = 'flight_status_histories'
    id = db.Column(db.Integer, primary_key=True)
    flight_instance_id = db.Column(db.Integer, db.ForeignKey('flight_instances.id'), nullable=False)
    old_status = db.Column(db.String(30), nullable=True)
    new_status = db.Column(db.String(30), nullable=False)
    changed_by = db.Column(db.String(80), default='System', nullable=False)
    remarks = db.Column(db.String(255), nullable=True)

class FlightDelayReason(db.Model, TimestampMixin, SoftDeleteMixin):
    __tablename__ = 'flight_delay_reasons'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True, nullable=False)  # WX (Weather), MECH (Mechanical), ATC
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)

    delay_logs = db.relationship('FlightDelayLog', backref='reason', lazy='dynamic')

class FlightDelayLog(db.Model, TimestampMixin, SoftDeleteMixin):
    __tablename__ = 'flight_delay_logs'
    id = db.Column(db.Integer, primary_key=True)
    flight_instance_id = db.Column(db.Integer, db.ForeignKey('flight_instances.id'), nullable=False)
    delay_reason_id = db.Column(db.Integer, db.ForeignKey('flight_delay_reasons.id'), nullable=False)
    delay_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text, nullable=True)

class FlightFuelLog(db.Model, TimestampMixin, SoftDeleteMixin):
    __tablename__ = 'flight_fuel_logs'
    id = db.Column(db.Integer, primary_key=True)
    flight_instance_id = db.Column(db.Integer, db.ForeignKey('flight_instances.id'), nullable=False)
    planned_fuel_kg = db.Column(db.Float, nullable=False)
    actual_fuel_loaded_kg = db.Column(db.Float, nullable=False)
    burned_fuel_kg = db.Column(db.Float, nullable=True)
    captain_signoff = db.Column(db.String(100), nullable=False)
