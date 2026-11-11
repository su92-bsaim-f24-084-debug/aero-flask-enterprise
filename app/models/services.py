from .base import db, TimestampMixin, SoftDeleteMixin

class BaggagePolicy(db.Model, TimestampMixin, SoftDeleteMixin):
    __tablename__ = 'baggage_policies'
    id = db.Column(db.Integer, primary_key=True)
    cabin_class_id = db.Column(db.Integer, db.ForeignKey('cabin_classes.id'), nullable=False)
    max_free_pieces = db.Column(db.Integer, default=1, nullable=False)
    max_weight_kg_per_piece = db.Column(db.Float, default=23.0, nullable=False)
    excess_charge_per_kg = db.Column(db.Numeric(10, 2), default=15.00, nullable=False)

class BaggageItem(db.Model, TimestampMixin, SoftDeleteMixin):
    __tablename__ = 'baggage_items'
    id = db.Column(db.Integer, primary_key=True)
    passenger_id = db.Column(db.Integer, db.ForeignKey('passengers.id'), nullable=False)
    ticket_id = db.Column(db.Integer, db.ForeignKey('tickets.id'), nullable=False)
    tag_number = db.Column(db.String(30), unique=True, nullable=False, index=True)
    weight_kg = db.Column(db.Float, nullable=False)
    is_excess = db.Column(db.Boolean, default=False, nullable=False)
    excess_fee = db.Column(db.Numeric(10, 2), default=0.00, nullable=False)
    status = db.Column(db.String(30), default='CheckedIn', nullable=False)  # CheckedIn, Loaded, Transferred, Claimed, Lost

class MealOption(db.Model, TimestampMixin, SoftDeleteMixin):
    __tablename__ = 'meal_options'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), unique=True, nullable=False)  # VGML (Vegetarian), HNML (Halal), KSML (Kosher)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=True)
    is_vegetarian = db.Column(db.Boolean, default=False, nullable=False)
    allergens = db.Column(db.String(150), nullable=True)

    requests = db.relationship('PassengerMealRequest', backref='meal_option', lazy='dynamic')

class PassengerMealRequest(db.Model, TimestampMixin, SoftDeleteMixin):
    __tablename__ = 'passenger_meal_requests'
    id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey('tickets.id'), nullable=False)
    meal_option_id = db.Column(db.Integer, db.ForeignKey('meal_options.id'), nullable=False)
    special_notes = db.Column(db.String(255), nullable=True)

class AncillaryService(db.Model, TimestampMixin, SoftDeleteMixin):
    __tablename__ = 'ancillary_services'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)  # In-Flight Wi-Fi, Priority Boarding, Airport Lounge
    category = db.Column(db.String(50), nullable=False)            # Comfort, Connectivity, Lounge, FastTrack
    price = db.Column(db.Numeric(10, 2), nullable=False)
    description = db.Column(db.Text, nullable=True)

    orders = db.relationship('AncillaryOrder', backref='service', lazy='dynamic')

class AncillaryOrder(db.Model, TimestampMixin, SoftDeleteMixin):
    __tablename__ = 'ancillary_orders'
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('ancillary_services.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1, nullable=False)
    subtotal = db.Column(db.Numeric(10, 2), nullable=False)
