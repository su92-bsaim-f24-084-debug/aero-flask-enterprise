from werkzeug.security import generate_password_hash, check_password_hash
from .base import db, TimestampMixin, SoftDeleteMixin

class User(db.Model, TimestampMixin, SoftDeleteMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='customer', nullable=False)  # admin, staff, customer
    is_active_account = db.Column(db.Boolean, default=True, nullable=False)

    profile = db.relationship('UserProfile', backref='user', uselist=False)
    bookings = db.relationship('Booking', backref='user', lazy='dynamic')
    loyalty_member = db.relationship('LoyaltyMember', backref='user', uselist=False)
    payment_methods = db.relationship('PaymentMethod', backref='user', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        return self.role == 'admin'

    def is_staff(self):
        return self.role in ['admin', 'staff']

class UserProfile(db.Model, TimestampMixin, SoftDeleteMixin):
    __tablename__ = 'user_profiles'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    first_name = db.Column(db.String(60), nullable=False)
    last_name = db.Column(db.String(60), nullable=False)
    phone_number = db.Column(db.String(30), nullable=True)
    date_of_birth = db.Column(db.Date, nullable=True)
    gender = db.Column(db.String(20), nullable=True)
    nationality = db.Column(db.String(60), nullable=True)
    passport_number = db.Column(db.String(40), nullable=True)
    passport_expiry = db.Column(db.Date, nullable=True)

class Passenger(db.Model, TimestampMixin, SoftDeleteMixin):
    __tablename__ = 'passengers'
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    first_name = db.Column(db.String(60), nullable=False)
    last_name = db.Column(db.String(60), nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    passport_number = db.Column(db.String(40), nullable=False)
    nationality = db.Column(db.String(60), nullable=False)

    emergency_contacts = db.relationship('EmergencyContact', backref='passenger', lazy='dynamic')
    tickets = db.relationship('Ticket', backref='passenger', lazy='dynamic')
    baggage_items = db.relationship('BaggageItem', backref='passenger', lazy='dynamic')

class EmergencyContact(db.Model, TimestampMixin, SoftDeleteMixin):
    __tablename__ = 'emergency_contacts'
    id = db.Column(db.Integer, primary_key=True)
    passenger_id = db.Column(db.Integer, db.ForeignKey('passengers.id'), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    relationship = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(120), nullable=True)
