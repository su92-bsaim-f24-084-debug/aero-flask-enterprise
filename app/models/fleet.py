from .base import db, TimestampMixin, SoftDeleteMixin

class AircraftManufacturer(db.Model, TimestampMixin, SoftDeleteMixin):
    __tablename__ = 'aircraft_manufacturers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    country = db.Column(db.String(80), nullable=False)
    founded_year = db.Column(db.Integer, nullable=True)
    website = db.Column(db.String(200), nullable=True)

    models = db.relationship('AircraftModel', backref='manufacturer', lazy='dynamic')

class AircraftModel(db.Model, TimestampMixin, SoftDeleteMixin):
    __tablename__ = 'aircraft_models'
    id = db.Column(db.Integer, primary_key=True)
    manufacturer_id = db.Column(db.Integer, db.ForeignKey('aircraft_manufacturers.id'), nullable=False)
    model_name = db.Column(db.String(80), nullable=False, unique=True)
    engine_type = db.Column(db.String(50), nullable=False)
    max_range_km = db.Column(db.Integer, nullable=False)
    cruise_speed_kmh = db.Column(db.Integer, nullable=False)
    seating_capacity = db.Column(db.Integer, nullable=False, default=180)

    aircrafts = db.relationship('Aircraft', backref='model', lazy='dynamic')
    seat_layouts = db.relationship('AircraftSeatLayout', backref='model', lazy='dynamic')

class Aircraft(db.Model, TimestampMixin, SoftDeleteMixin):
    __tablename__ = 'aircrafts'
    id = db.Column(db.Integer, primary_key=True)
    model_id = db.Column(db.Integer, db.ForeignKey('aircraft_models.id'), nullable=False)
    tail_number = db.Column(db.String(20), unique=True, nullable=False)
    serial_number = db.Column(db.String(50), unique=True, nullable=False)
    manufacture_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(30), default='Active', nullable=False)  # Active, Maintenance, Grounded, Retired
    total_flight_hours = db.Column(db.Float, default=0.0, nullable=False)

    seats = db.relationship('AircraftSeat', backref='aircraft', lazy='dynamic')
    maintenance_logs = db.relationship('MaintenanceLog', backref='aircraft', lazy='dynamic')
    flight_instances = db.relationship('FlightInstance', backref='assigned_aircraft', lazy='dynamic')

class CabinClass(db.Model, TimestampMixin, SoftDeleteMixin):
    __tablename__ = 'cabin_classes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)  # Economy, Premium Economy, Business, First
    code = db.Column(db.String(5), unique=True, nullable=False)   # Y, W, J, F
    description = db.Column(db.Text, nullable=True)

    seats = db.relationship('AircraftSeat', backref='cabin_class', lazy='dynamic')
    seat_layouts = db.relationship('AircraftSeatLayout', backref='cabin_class', lazy='dynamic')
    baggage_policies = db.relationship('BaggagePolicy', backref='cabin_class', lazy='dynamic')

class AircraftSeatLayout(db.Model, TimestampMixin, SoftDeleteMixin):
    __tablename__ = 'aircraft_seat_layouts'
    id = db.Column(db.Integer, primary_key=True)
    model_id = db.Column(db.Integer, db.ForeignKey('aircraft_models.id'), nullable=False)
    cabin_class_id = db.Column(db.Integer, db.ForeignKey('cabin_classes.id'), nullable=False)
    total_seats = db.Column(db.Integer, nullable=False)
    rows_count = db.Column(db.Integer, nullable=False)
    seats_per_row = db.Column(db.Integer, nullable=False)

class AircraftSeat(db.Model, TimestampMixin, SoftDeleteMixin):
    __tablename__ = 'aircraft_seats'
    id = db.Column(db.Integer, primary_key=True)
    aircraft_id = db.Column(db.Integer, db.ForeignKey('aircrafts.id'), nullable=False)
    cabin_class_id = db.Column(db.Integer, db.ForeignKey('cabin_classes.id'), nullable=False)
    seat_number = db.Column(db.String(10), nullable=False)  # e.g., 12A, 14F
    row_number = db.Column(db.Integer, nullable=False)
    column_letter = db.Column(db.String(2), nullable=False)
    is_exit_row = db.Column(db.Boolean, default=False)
    is_window = db.Column(db.Boolean, default=False)
    is_aisle = db.Column(db.Boolean, default=False)

    reservations = db.relationship('SeatReservation', backref='seat', lazy='dynamic')

class MaintenanceType(db.Model, TimestampMixin, SoftDeleteMixin):
    __tablename__ = 'maintenance_types'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True, nullable=False)  # A-CHECK, B-CHECK, C-CHECK, D-CHECK
    name = db.Column(db.String(100), nullable=False)
    interval_days = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=True)

    logs = db.relationship('MaintenanceLog', backref='maintenance_type', lazy='dynamic')

class MaintenanceLog(db.Model, TimestampMixin, SoftDeleteMixin):
    __tablename__ = 'maintenance_logs'
    id = db.Column(db.Integer, primary_key=True)
    aircraft_id = db.Column(db.Integer, db.ForeignKey('aircrafts.id'), nullable=False)
    maintenance_type_id = db.Column(db.Integer, db.ForeignKey('maintenance_types.id'), nullable=False)
    scheduled_date = db.Column(db.Date, nullable=False)
    completed_date = db.Column(db.Date, nullable=True)
    lead_technician = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(30), default='Scheduled', nullable=False)  # Scheduled, In Progress, Completed, Signed Off
    cost_estimate = db.Column(db.Numeric(10, 2), default=0.00)
    notes = db.Column(db.Text, nullable=True)

    part_replacements = db.relationship('PartReplacementLog', backref='maintenance_log', lazy='dynamic')

class AircraftPart(db.Model, TimestampMixin, SoftDeleteMixin):
    __tablename__ = 'aircraft_parts'
    id = db.Column(db.Integer, primary_key=True)
    part_number = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    category = db.Column(db.String(60), nullable=False)  # Avionics, Engine, Hydraulics, Landing Gear
    stock_quantity = db.Column(db.Integer, default=0, nullable=False)
    unit_cost = db.Column(db.Numeric(10, 2), nullable=False)

    replacement_logs = db.relationship('PartReplacementLog', backref='part', lazy='dynamic')

class PartReplacementLog(db.Model, TimestampMixin, SoftDeleteMixin):
    __tablename__ = 'part_replacement_logs'
    id = db.Column(db.Integer, primary_key=True)
    maintenance_log_id = db.Column(db.Integer, db.ForeignKey('maintenance_logs.id'), nullable=False)
    part_id = db.Column(db.Integer, db.ForeignKey('aircraft_parts.id'), nullable=False)
    quantity_replaced = db.Column(db.Integer, default=1, nullable=False)
    replaced_date = db.Column(db.Date, nullable=False)
    technician_notes = db.Column(db.Text, nullable=True)
