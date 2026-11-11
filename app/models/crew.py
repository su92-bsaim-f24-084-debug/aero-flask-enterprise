from .base import db, TimestampMixin, SoftDeleteMixin

class Department(db.Model, TimestampMixin, SoftDeleteMixin):
    __tablename__ = 'departments'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)

    roles = db.relationship('EmployeeRole', backref='department', lazy='dynamic')

class EmployeeRole(db.Model, TimestampMixin, SoftDeleteMixin):
    __tablename__ = 'employee_roles'
    id = db.Column(db.Integer, primary_key=True)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    access_level = db.Column(db.String(30), default='Staff', nullable=False)  # Admin, FlightCrew, GroundOps, Support

    employees = db.relationship('Employee', backref='role', lazy='dynamic')

class Employee(db.Model, TimestampMixin, SoftDeleteMixin):
    __tablename__ = 'employees'
    id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('employee_roles.id'), nullable=False)
    employee_code = db.Column(db.String(20), unique=True, nullable=False)
    first_name = db.Column(db.String(60), nullable=False)
    last_name = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(30), nullable=False)
    hire_date = db.Column(db.Date, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    pilot_certifications = db.relationship('PilotCertification', backref='employee', lazy='dynamic')
    crew_schedules = db.relationship('CrewSchedule', backref='employee', lazy='dynamic')
    duty_hour_logs = db.relationship('DutyHourLog', backref='employee', lazy='dynamic')

class PilotCertification(db.Model, TimestampMixin, SoftDeleteMixin):
    __tablename__ = 'pilot_certifications'
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    aircraft_model_id = db.Column(db.Integer, db.ForeignKey('aircraft_models.id'), nullable=False)
    license_number = db.Column(db.String(50), unique=True, nullable=False)
    issued_date = db.Column(db.Date, nullable=False)
    expiry_date = db.Column(db.Date, nullable=False)
    is_current = db.Column(db.Boolean, default=True, nullable=False)

class CrewSchedule(db.Model, TimestampMixin, SoftDeleteMixin):
    __tablename__ = 'crew_schedules'
    id = db.Column(db.Integer, primary_key=True)
    flight_instance_id = db.Column(db.Integer, db.ForeignKey('flight_instances.id'), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    duty_role = db.Column(db.String(50), nullable=False)  # Captain, First Officer, Purser, Flight Attendant
    report_time = db.Column(db.DateTime, nullable=False)

class DutyHourLog(db.Model, TimestampMixin, SoftDeleteMixin):
    __tablename__ = 'duty_hour_logs'
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    flight_instance_id = db.Column(db.Integer, db.ForeignKey('flight_instances.id'), nullable=False)
    duty_start = db.Column(db.DateTime, nullable=False)
    duty_end = db.Column(db.DateTime, nullable=False)
    flight_hours = db.Column(db.Float, nullable=False)
    rest_hours_before = db.Column(db.Float, nullable=False)
