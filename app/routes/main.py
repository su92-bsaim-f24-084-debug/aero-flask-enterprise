from flask import Blueprint, render_template, current_app
from app.models import Airport, Route, FlightInstance, Aircraft, Booking, db

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    """Landing homepage showcasing airline metrics and quick flight search."""
    airports = Airport.query.filter_by(is_deleted=False).all()
    upcoming_flights = FlightInstance.query.filter_by(is_deleted=False).limit(6).all()
    active_aircraft_count = Aircraft.query.filter_by(is_deleted=False, status='Active').count()
    routes_count = Route.query.filter_by(is_deleted=False, is_active=True).count()
    bookings_count = Booking.query.filter_by(is_deleted=False).count()

    return render_template(
        'main/index.html',
        airports=airports,
        upcoming_flights=upcoming_flights,
        aircraft_count=active_aircraft_count,
        routes_count=routes_count,
        bookings_count=bookings_count
    )

@bp.route('/about')
def about():
    """System overview and architecture documentation."""
    # Count all models
    from app.models import __all__ as model_names
    total_models = len(model_names) - 3  # minus db, TimestampMixin, SoftDeleteMixin
    return render_template('main/about.html', total_models=total_models)

@bp.route('/contact')
def contact():
    """Customer care and support information."""
    return render_template('main/contact.html')
