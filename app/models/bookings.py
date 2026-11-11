from .base import db, TimestampMixin, SoftDeleteMixin

class FareClass(db.Model, TimestampMixin, SoftDeleteMixin):
    __tablename__ = 'fare_classes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)  # Saver, Value, Flex, SuperFlex
    code = db.Column(db.String(10), unique=True, nullable=False)  # ECO-SAV, BIZ-FLX
    is_refundable = db.Column(db.Boolean, default=False, nullable=False)
    change_fee = db.Column(db.Numeric(10, 2), default=50.00, nullable=False)
    miles_earning_rate = db.Column(db.Float, default=1.0, nullable=False)

    flight_prices = db.relationship('FlightPrice', backref='fare_class', lazy='dynamic')
    tickets = db.relationship('Ticket', backref='fare_class', lazy='dynamic')

class FlightPrice(db.Model, TimestampMixin, SoftDeleteMixin):
    __tablename__ = 'flight_prices'
    id = db.Column(db.Integer, primary_key=True)
    flight_instance_id = db.Column(db.Integer, db.ForeignKey('flight_instances.id'), nullable=False)
    cabin_class_id = db.Column(db.Integer, db.ForeignKey('cabin_classes.id'), nullable=False)
    fare_class_id = db.Column(db.Integer, db.ForeignKey('fare_classes.id'), nullable=False)
    base_fare = db.Column(db.Numeric(10, 2), nullable=False)
    tax_amount = db.Column(db.Numeric(10, 2), nullable=False)
    available_seats = db.Column(db.Integer, nullable=False)

class Booking(db.Model, TimestampMixin, SoftDeleteMixin):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    booking_reference = db.Column(db.String(8), unique=True, nullable=False, index=True)  # PNR (e.g. AER872)
    booking_date = db.Column(db.DateTime, nullable=False)
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)
    booking_status = db.Column(db.String(30), default='Confirmed', nullable=False)  # Confirmed, Cancelled, Completed
    payment_status = db.Column(db.String(30), default='Pending', nullable=False)    # Pending, Paid, Refunded

    passengers = db.relationship('Passenger', backref='booking', lazy='dynamic')
    tickets = db.relationship('Ticket', backref='booking', lazy='dynamic')
    payment_transactions = db.relationship('PaymentTransaction', backref='booking', lazy='dynamic')
    ancillary_orders = db.relationship('AncillaryOrder', backref='booking', lazy='dynamic')
    refunds = db.relationship('RefundRecord', backref='booking', lazy='dynamic')

class Ticket(db.Model, TimestampMixin, SoftDeleteMixin):
    __tablename__ = 'tickets'
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.id'), nullable=False)
    flight_instance_id = db.Column(db.Integer, db.ForeignKey('flight_instances.id'), nullable=False)
    passenger_id = db.Column(db.Integer, db.ForeignKey('passengers.id'), nullable=False)
    fare_class_id = db.Column(db.Integer, db.ForeignKey('fare_classes.id'), nullable=False)
    ticket_number = db.Column(db.String(20), unique=True, nullable=False, index=True)
    fare_paid = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.String(30), default='Issued', nullable=False)  # Issued, CheckedIn, Boarded, Cancelled, Refunded

    seat_reservation = db.relationship('SeatReservation', backref='ticket', uselist=False)
    boarding_pass = db.relationship('BoardingPass', backref='ticket', uselist=False)
    meal_requests = db.relationship('PassengerMealRequest', backref='ticket', lazy='dynamic')
    baggage_items = db.relationship('BaggageItem', backref='ticket', lazy='dynamic')

class SeatReservation(db.Model, TimestampMixin, SoftDeleteMixin):
    __tablename__ = 'seat_reservations'
    id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey('tickets.id'), unique=True, nullable=False)
    flight_instance_id = db.Column(db.Integer, db.ForeignKey('flight_instances.id'), nullable=False)
    seat_id = db.Column(db.Integer, db.ForeignKey('aircraft_seats.id'), nullable=False)
    reserved_at = db.Column(db.DateTime, nullable=False)

class BoardingPass(db.Model, TimestampMixin, SoftDeleteMixin):
    __tablename__ = 'boarding_passes'
    id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey('tickets.id'), unique=True, nullable=False)
    sequence_number = db.Column(db.Integer, nullable=False)
    boarding_group = db.Column(db.String(5), nullable=False)  # A, B, C, D
    gate_number = db.Column(db.String(20), nullable=True)
    boarding_time = db.Column(db.DateTime, nullable=False)
    barcode_hash = db.Column(db.String(64), unique=True, nullable=False)
    has_boarded = db.Column(db.Boolean, default=False, nullable=False)
