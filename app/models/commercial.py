from .base import db, TimestampMixin, SoftDeleteMixin

class PaymentMethod(db.Model, TimestampMixin, SoftDeleteMixin):
    __tablename__ = 'payment_methods'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    method_type = db.Column(db.String(30), nullable=False)  # CreditCard, DebitCard, PayPal, ApplePay
    card_brand = db.Column(db.String(30), nullable=True)    # Visa, MasterCard, Amex
    last_four = db.Column(db.String(4), nullable=False)
    expiry_month = db.Column(db.Integer, nullable=False)
    expiry_year = db.Column(db.Integer, nullable=False)
    is_default = db.Column(db.Boolean, default=False, nullable=False)

    transactions = db.relationship('PaymentTransaction', backref='payment_method', lazy='dynamic')

class PaymentTransaction(db.Model, TimestampMixin, SoftDeleteMixin):
    __tablename__ = 'payment_transactions'
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.id'), nullable=False)
    payment_method_id = db.Column(db.Integer, db.ForeignKey('payment_methods.id'), nullable=True)
    transaction_reference = db.Column(db.String(64), unique=True, nullable=False, index=True)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    currency = db.Column(db.String(3), default='USD', nullable=False)
    status = db.Column(db.String(30), default='Completed', nullable=False)  # Pending, Completed, Failed, Refunded

    refunds = db.relationship('RefundRecord', backref='payment_transaction', lazy='dynamic')

class RefundRecord(db.Model, TimestampMixin, SoftDeleteMixin):
    __tablename__ = 'refund_records'
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.id'), nullable=False)
    payment_transaction_id = db.Column(db.Integer, db.ForeignKey('payment_transactions.id'), nullable=False)
    refund_amount = db.Column(db.Numeric(10, 2), nullable=False)
    cancellation_fee = db.Column(db.Numeric(10, 2), default=0.00, nullable=False)
    reason = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(30), default='Processed', nullable=False)  # Requested, Approved, Processed, Rejected

class PromoCode(db.Model, TimestampMixin, SoftDeleteMixin):
    __tablename__ = 'promo_codes'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True, nullable=False, index=True)
    discount_percentage = db.Column(db.Integer, nullable=False)  # e.g., 10 for 10%
    max_discount_amount = db.Column(db.Numeric(10, 2), nullable=True)
    valid_from = db.Column(db.Date, nullable=False)
    valid_to = db.Column(db.Date, nullable=False)
    usage_limit = db.Column(db.Integer, default=100, nullable=False)
    used_count = db.Column(db.Integer, default=0, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

class LoyaltyProgram(db.Model, TimestampMixin, SoftDeleteMixin):
    __tablename__ = 'loyalty_programs'
    id = db.Column(db.Integer, primary_key=True)
    tier_name = db.Column(db.String(50), unique=True, nullable=False)  # Bronze, Silver, Gold, Platinum
    min_points_required = db.Column(db.Integer, nullable=False)
    points_multiplier = db.Column(db.Float, default=1.0, nullable=False)
    priority_boarding = db.Column(db.Boolean, default=False, nullable=False)
    lounge_access = db.Column(db.Boolean, default=False, nullable=False)
    extra_baggage_kg = db.Column(db.Float, default=0.0, nullable=False)

    members = db.relationship('LoyaltyMember', backref='program', lazy='dynamic')

class LoyaltyMember(db.Model, TimestampMixin, SoftDeleteMixin):
    __tablename__ = 'loyalty_members'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    loyalty_program_id = db.Column(db.Integer, db.ForeignKey('loyalty_programs.id'), nullable=False)
    membership_number = db.Column(db.String(30), unique=True, nullable=False, index=True)
    points_balance = db.Column(db.Integer, default=0, nullable=False)
    lifetime_miles = db.Column(db.Integer, default=0, nullable=False)
