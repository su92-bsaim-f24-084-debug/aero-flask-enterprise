from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, BooleanField, SubmitField, SelectField,
    DecimalField, IntegerField, DateField, TimeField, TextAreaField, HiddenField
)
from wtforms.validators import (
    DataRequired, Email, Length, EqualTo, ValidationError, NumberRange, Optional
)
from app.models import User, Airport

class LoginForm(FlaskForm):
    """Server-side validated login form."""
    username_or_email = StringField('Username or Email', validators=[
        DataRequired(message="Username or Email is required."),
        Length(min=3, max=120, message="Identifier must be between 3 and 120 characters.")
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message="Password is required.")
    ])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegisterForm(FlaskForm):
    """Server-side validated user registration form."""
    username = StringField('Username', validators=[
        DataRequired(message="Username is required."),
        Length(min=3, max=30, message="Username must be between 3 and 30 characters.")
    ])
    email = StringField('Email Address', validators=[
        DataRequired(message="Email is required."),
        Email(message="Please provide a valid email address.")
    ])
    first_name = StringField('First Name', validators=[
        DataRequired(message="First name is required."),
        Length(min=2, max=50)
    ])
    last_name = StringField('Last Name', validators=[
        DataRequired(message="Last name is required."),
        Length(min=2, max=50)
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message="Password is required."),
        Length(min=6, message="Password must be at least 6 characters.")
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(message="Please confirm your password."),
        EqualTo('password', message="Passwords must match.")
    ])
    submit = SubmitField('Create Account')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data, is_deleted=False).first():
            raise ValidationError("This username is already taken. Please choose another.")

    def validate_email(self, field):
        if User.query.filter_by(email=field.data.lower(), is_deleted=False).first():
            raise ValidationError("An account with this email address already exists.")

class ProfileForm(FlaskForm):
    """Profile editing form."""
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=50)])
    phone_number = StringField('Phone Number', validators=[Optional(), Length(max=25)])
    nationality = StringField('Nationality', validators=[Optional(), Length(max=50)])
    passport_number = StringField('Passport Number', validators=[Optional(), Length(max=30)])
    submit = SubmitField('Update Profile')

class FlightSearchForm(FlaskForm):
    """Flight search and booking query form."""
    origin_id = SelectField('From (Origin)', coerce=int, validators=[DataRequired()])
    destination_id = SelectField('To (Destination)', coerce=int, validators=[DataRequired()])
    flight_date = DateField('Travel Date', validators=[DataRequired()])
    cabin_class_id = SelectField('Cabin Class', coerce=int, validators=[DataRequired()])
    passengers_count = IntegerField('Passengers', default=1, validators=[
        DataRequired(), NumberRange(min=1, max=9, message="Passengers must be between 1 and 9.")
    ])
    submit = SubmitField('Search Flights')

    def validate_destination_id(self, field):
        if self.origin_id.data and field.data == self.origin_id.data:
            raise ValidationError("Origin and destination airports cannot be the same.")

class BookingPassengerForm(FlaskForm):
    """Form to capture passenger details during booking."""
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=50)])
    gender = SelectField('Gender', choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], validators=[DataRequired()])
    date_of_birth = DateField('Date of Birth', validators=[DataRequired()])
    passport_number = StringField('Passport Number', validators=[DataRequired(), Length(min=5, max=30)])
    nationality = StringField('Nationality', validators=[DataRequired(), Length(min=2, max=50)])
    emergency_name = StringField('Emergency Contact Name', validators=[DataRequired()])
    emergency_phone = StringField('Emergency Phone Number', validators=[DataRequired()])
    emergency_relation = StringField('Relationship', validators=[DataRequired()])
    fare_class_id = SelectField('Fare Option', coerce=int, validators=[DataRequired()])
    promo_code = StringField('Promo / Discount Code', validators=[Optional()])
    submit = SubmitField('Proceed to Confirmation')

class AircraftForm(FlaskForm):
    """CRUD form for fleet aircraft."""
    model_id = SelectField('Aircraft Model', coerce=int, validators=[DataRequired()])
    tail_number = StringField('Tail Number (Registration)', validators=[DataRequired(), Length(min=3, max=15)])
    serial_number = StringField('Manufacturer Serial Number', validators=[DataRequired(), Length(min=3, max=30)])
    manufacture_date = DateField('Manufacture Date', validators=[DataRequired()])
    status = SelectField('Operational Status', choices=[
        ('Active', 'Active'), ('Maintenance', 'Maintenance'), ('Grounded', 'Grounded'), ('Retired', 'Retired')
    ], validators=[DataRequired()])
    total_flight_hours = DecimalField('Total Flight Hours', default=0.0, validators=[NumberRange(min=0)])
    submit = SubmitField('Save Aircraft')

class AirportForm(FlaskForm):
    """CRUD form for airports."""
    city_id = SelectField('City', coerce=int, validators=[DataRequired()])
    name = StringField('Airport Name', validators=[DataRequired(), Length(min=3, max=120)])
    iata_code = StringField('IATA Code (3 letters)', validators=[DataRequired(), Length(min=3, max=3)])
    icao_code = StringField('ICAO Code (4 letters)', validators=[DataRequired(), Length(min=4, max=4)])
    latitude = DecimalField('Latitude', validators=[DataRequired(), NumberRange(min=-90, max=90)])
    longitude = DecimalField('Longitude', validators=[DataRequired(), NumberRange(min=-180, max=180)])
    elevation_ft = IntegerField('Elevation (ft)', validators=[Optional()])
    submit = SubmitField('Save Airport')

class RouteForm(FlaskForm):
    """CRUD form for airline routes."""
    origin_airport_id = SelectField('Origin Airport', coerce=int, validators=[DataRequired()])
    destination_airport_id = SelectField('Destination Airport', coerce=int, validators=[DataRequired()])
    distance_km = DecimalField('Distance (km)', validators=[DataRequired(), NumberRange(min=10)])
    estimated_flight_minutes = IntegerField('Flight Duration (minutes)', validators=[DataRequired(), NumberRange(min=10)])
    is_active = BooleanField('Route Active', default=True)
    submit = SubmitField('Save Route')

    def validate_destination_airport_id(self, field):
        if self.origin_airport_id.data and field.data == self.origin_airport_id.data:
            raise ValidationError("Origin and destination cannot be identical.")

class FlightScheduleForm(FlaskForm):
    """CRUD form for flight schedules."""
    route_id = SelectField('Route', coerce=int, validators=[DataRequired()])
    flight_number = StringField('Flight Number (e.g. AF-204)', validators=[DataRequired(), Length(min=3, max=10)])
    scheduled_departure_time = TimeField('Departure Time (UTC)', validators=[DataRequired()])
    scheduled_arrival_time = TimeField('Arrival Time (UTC)', validators=[DataRequired()])
    days_of_week = SelectField('Frequency', choices=[
        ('Daily', 'Daily'), ('Mon/Wed/Fri', 'Mon/Wed/Fri'), ('Tue/Thu/Sat', 'Tue/Thu/Sat'), ('Weekends', 'Weekends')
    ], validators=[DataRequired()])
    submit = SubmitField('Save Schedule')

class MaintenanceLogForm(FlaskForm):
    """CRUD form for aircraft maintenance records."""
    aircraft_id = SelectField('Aircraft', coerce=int, validators=[DataRequired()])
    maintenance_type_id = SelectField('Maintenance Type', coerce=int, validators=[DataRequired()])
    scheduled_date = DateField('Scheduled Date', validators=[DataRequired()])
    completed_date = DateField('Completed Date', validators=[Optional()])
    lead_technician = StringField('Lead Technician', validators=[DataRequired(), Length(min=2, max=80)])
    status = SelectField('Status', choices=[
        ('Scheduled', 'Scheduled'), ('In Progress', 'In Progress'), ('Completed', 'Completed'), ('Signed Off', 'Signed Off')
    ], validators=[DataRequired()])
    cost_estimate = DecimalField('Estimated Cost ($)', default=0.00, validators=[Optional()])
    notes = TextAreaField('Technician Notes', validators=[Optional()])
    submit = SubmitField('Save Maintenance Log')

class PromoCodeForm(FlaskForm):
    """CRUD form for promotional discount codes."""
    code = StringField('Promo Code', validators=[DataRequired(), Length(min=3, max=20)])
    discount_percentage = IntegerField('Discount (%)', validators=[DataRequired(), NumberRange(min=1, max=100)])
    max_discount_amount = DecimalField('Max Discount ($)', validators=[Optional(), NumberRange(min=1)])
    valid_from = DateField('Valid From', validators=[DataRequired()])
    valid_to = DateField('Valid To', validators=[DataRequired()])
    usage_limit = IntegerField('Usage Limit', default=100, validators=[DataRequired(), NumberRange(min=1)])
    is_active = BooleanField('Active', default=True)
    submit = SubmitField('Save Promo Code')
