from datetime import datetime, date
from flask import Blueprint, render_template, request, flash, redirect, url_for
from app.models import (
    FlightInstance, FlightSchedule, Route, Airport, CabinClass, FlightPrice
)
from app.forms import FlightSearchForm

bp = Blueprint('flights', __name__, url_prefix='/flights')

@bp.route('/search', methods=['GET', 'POST'])
def search():
    """Flight search and availability engine."""
    form = FlightSearchForm()
    
    # Populate airport select fields
    airports = Airport.query.filter_by(is_deleted=False).order_by(Airport.city_id).all()
    airport_choices = [(a.id, f"{a.iata_code} - {a.name} ({a.city.name})") for a in airports]
    form.origin_id.choices = airport_choices
    form.destination_id.choices = airport_choices

    cabin_classes = CabinClass.query.filter_by(is_deleted=False).all()
    form.cabin_class_id.choices = [(c.id, f"{c.name} ({c.code})") for c in cabin_classes]

    flights = []
    has_searched = False

    if request.method == 'GET' and request.args.get('origin_id'):
        # Handle GET search from homepage form
        form.origin_id.data = int(request.args.get('origin_id'))
        form.destination_id.data = int(request.args.get('destination_id'))
        if request.args.get('flight_date'):
            try:
                form.flight_date.data = datetime.strptime(request.args.get('flight_date'), '%Y-%m-%d').date()
            except ValueError:
                form.flight_date.data = date.today()
        else:
            form.flight_date.data = date.today()
        form.cabin_class_id.data = cabin_classes[0].id if cabin_classes else 1

    if form.validate_on_submit() or (request.method == 'GET' and request.args.get('origin_id')):
        has_searched = True
        origin_id = form.origin_id.data
        dest_id = form.destination_id.data
        travel_date = form.flight_date.data or date.today()

        # Query routes connecting origin and destination
        matching_routes = Route.query.filter_by(
            origin_airport_id=origin_id,
            destination_airport_id=dest_id,
            is_active=True,
            is_deleted=False
        ).all()

        route_ids = [r.id for r in matching_routes]
        if route_ids:
            # Query active flight instances
            flights = FlightInstance.query.join(FlightSchedule).filter(
                FlightSchedule.route_id.in_(route_ids),
                FlightInstance.flight_date >= travel_date,
                FlightInstance.is_deleted == False
            ).order_by(FlightInstance.flight_date, FlightSchedule.scheduled_departure_time).all()

    return render_template(
        'flights/search.html',
        form=form,
        flights=flights,
        has_searched=has_searched
    )

@bp.route('/<int:id>')
def details(id):
    """View detailed flight instance, seat availability, prices, and route info."""
    flight = FlightInstance.query.filter_by(id=id, is_deleted=False).first_or_404()
    prices = FlightPrice.query.filter_by(flight_instance_id=id, is_deleted=False).all()
    return render_template('flights/details.html', flight=flight, prices=prices)

@bp.route('/schedules')
def schedules():
    """List all scheduled routes and timings."""
    all_schedules = FlightSchedule.query.filter_by(is_deleted=False).all()
    return render_template('flights/schedules.html', schedules=all_schedules)
