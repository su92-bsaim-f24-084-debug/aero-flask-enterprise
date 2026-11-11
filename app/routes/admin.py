from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.models import (
    db, Airport, City, Route, PromoCode, User, Booking, FlightInstance, Aircraft,
    __all__ as all_model_symbols
)
import app.models as models_module
from app.forms import AirportForm, RouteForm, PromoCodeForm
from app.utils import admin_required

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route('/dashboard')
@admin_required
def dashboard():
    """Admin KPI overview."""
    total_users = User.query.filter_by(is_deleted=False).count()
    total_bookings = Booking.query.filter_by(is_deleted=False).count()
    total_flights = FlightInstance.query.filter_by(is_deleted=False).count()
    total_fleet = Aircraft.query.filter_by(is_deleted=False).count()
    soft_deleted_bookings = Booking.query.filter_by(is_deleted=True).count()
    soft_deleted_aircraft = Aircraft.query.filter_by(is_deleted=True).count()

    recent_bookings = Booking.query.order_by(Booking.created_at.desc()).limit(5).all()

    return render_template(
        'admin/dashboard.html',
        total_users=total_users,
        total_bookings=total_bookings,
        total_flights=total_flights,
        total_fleet=total_fleet,
        soft_deleted_bookings=soft_deleted_bookings,
        soft_deleted_aircraft=soft_deleted_aircraft,
        recent_bookings=recent_bookings
    )

# ================= AIRPORTS CRUD =================

@bp.route('/airports')
@admin_required
def airports():
    """READ: Airports list."""
    show_deleted = request.args.get('show_deleted', '0') == '1'
    if show_deleted:
        items = Airport.query.all()
    else:
        items = Airport.query.filter_by(is_deleted=False).all()
    return render_template('admin/airports.html', airports=items, show_deleted=show_deleted)

@bp.route('/airports/create', methods=['GET', 'POST'])
@admin_required
def create_airport():
    """CREATE: Airport."""
    form = AirportForm()
    cities = City.query.filter_by(is_deleted=False).order_by(City.name).all()
    form.city_id.choices = [(c.id, f"{c.name} ({c.country.name})") for c in cities]

    if form.validate_on_submit():
        airport = Airport(
            city_id=form.city_id.data,
            name=form.name.data.strip(),
            iata_code=form.iata_code.data.strip().upper(),
            icao_code=form.icao_code.data.strip().upper(),
            latitude=float(form.latitude.data),
            longitude=float(form.longitude.data),
            elevation_ft=form.elevation_ft.data
        )
        db.session.add(airport)
        db.session.commit()
        flash(f"Airport {airport.iata_code} created successfully.", "success")
        return redirect(url_for('admin.airports'))

    return render_template('admin/create_airport.html', form=form)

@bp.route('/airports/<int:id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_airport(id):
    """UPDATE: Airport."""
    airport = Airport.query.filter_by(id=id, is_deleted=False).first_or_404()
    form = AirportForm(obj=airport)
    cities = City.query.filter_by(is_deleted=False).order_by(City.name).all()
    form.city_id.choices = [(c.id, f"{c.name} ({c.country.name})") for c in cities]

    if form.validate_on_submit():
        airport.city_id = form.city_id.data
        airport.name = form.name.data.strip()
        airport.iata_code = form.iata_code.data.strip().upper()
        airport.icao_code = form.icao_code.data.strip().upper()
        airport.latitude = float(form.latitude.data)
        airport.longitude = float(form.longitude.data)
        airport.elevation_ft = form.elevation_ft.data
        db.session.commit()
        flash(f"Airport {airport.iata_code} updated successfully.", "success")
        return redirect(url_for('admin.airports'))

    return render_template('admin/edit_airport.html', form=form, airport=airport)

@bp.route('/airports/<int:id>/delete', methods=['POST'])
@admin_required
def delete_airport(id):
    """DELETE: Soft delete airport."""
    airport = Airport.query.filter_by(id=id, is_deleted=False).first_or_404()
    airport.soft_delete()
    flash(f"Airport {airport.iata_code} soft-deleted.", "info")
    return redirect(url_for('admin.airports'))

# ================= ROUTES CRUD =================

@bp.route('/routes')
@admin_required
def routes():
    """READ: Routes list."""
    routes_list = Route.query.filter_by(is_deleted=False).all()
    return render_template('admin/routes.html', routes=routes_list)

@bp.route('/routes/create', methods=['GET', 'POST'])
@admin_required
def create_route():
    """CREATE: Route."""
    form = RouteForm()
    airports = Airport.query.filter_by(is_deleted=False).all()
    choices = [(a.id, f"{a.iata_code} - {a.name}") for a in airports]
    form.origin_airport_id.choices = choices
    form.destination_airport_id.choices = choices

    if form.validate_on_submit():
        route = Route(
            origin_airport_id=form.origin_airport_id.data,
            destination_airport_id=form.destination_airport_id.data,
            distance_km=float(form.distance_km.data),
            estimated_flight_minutes=form.estimated_flight_minutes.data,
            is_active=form.is_active.data
        )
        db.session.add(route)
        db.session.commit()
        flash("Flight route created successfully.", "success")
        return redirect(url_for('admin.routes'))

    return render_template('admin/create_route.html', form=form)

@bp.route('/routes/<int:id>/delete', methods=['POST'])
@admin_required
def delete_route(id):
    """DELETE: Soft delete route."""
    route = Route.query.filter_by(id=id, is_deleted=False).first_or_404()
    route.soft_delete()
    flash("Route soft-deleted.", "info")
    return redirect(url_for('admin.routes'))

# ================= PROMOS CRUD =================

@bp.route('/promos')
@admin_required
def promos():
    """READ: Promo codes."""
    promos_list = PromoCode.query.filter_by(is_deleted=False).all()
    return render_template('admin/promos.html', promos=promos_list)

@bp.route('/promos/create', methods=['GET', 'POST'])
@admin_required
def create_promo():
    """CREATE: Promo code."""
    form = PromoCodeForm()
    if form.validate_on_submit():
        promo = PromoCode(
            code=form.code.data.strip().upper(),
            discount_percentage=form.discount_percentage.data,
            max_discount_amount=form.max_discount_amount.data,
            valid_from=form.valid_from.data,
            valid_to=form.valid_to.data,
            usage_limit=form.usage_limit.data,
            is_active=form.is_active.data
        )
        db.session.add(promo)
        db.session.commit()
        flash(f"Promo code {promo.code} created.", "success")
        return redirect(url_for('admin.promos'))

    return render_template('admin/create_promo.html', form=form)

@bp.route('/promos/<int:id>/delete', methods=['POST'])
@admin_required
def delete_promo(id):
    """DELETE: Soft delete promo code."""
    promo = PromoCode.query.filter_by(id=id, is_deleted=False).first_or_404()
    promo.soft_delete()
    flash(f"Promo {promo.code} soft-deleted.", "info")
    return redirect(url_for('admin.promos'))

# ================= 51-MODEL SCHEMA EXPLORER =================

@bp.route('/schema-browser')
@admin_required
def schema_browser():
    """Visual inspector for all 51 models, record counts, active vs soft-deleted."""
    schema_stats = []
    excluded = {'db', 'TimestampMixin', 'SoftDeleteMixin'}

    for model_name in sorted(all_model_symbols):
        if model_name in excluded:
            continue
        cls = getattr(models_module, model_name, None)
        if cls and hasattr(cls, '__tablename__'):
            try:
                total_count = cls.query.count()
                active_count = cls.query.filter_by(is_deleted=False).count() if hasattr(cls, 'is_deleted') else total_count
                soft_deleted_count = total_count - active_count
                table_name = cls.__tablename__
                fields = [c.name for c in cls.__table__.columns]
                schema_stats.append({
                    'model': model_name,
                    'table': table_name,
                    'total': total_count,
                    'active': active_count,
                    'soft_deleted': soft_deleted_count,
                    'columns_count': len(fields),
                    'columns': fields[:6]
                })
            except Exception:
                pass

    return render_template('admin/schema_browser.html', models=schema_stats)
