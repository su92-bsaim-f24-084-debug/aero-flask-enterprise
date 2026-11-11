from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.models import (
    db, Aircraft, AircraftModel, MaintenanceLog, MaintenanceType
)
from app.forms import AircraftForm, MaintenanceLogForm
from app.utils import login_required, admin_required

bp = Blueprint('fleet', __name__, url_prefix='/fleet')

@bp.route('/')
def index():
    """READ: List all fleet aircraft."""
    show_deleted = request.args.get('show_deleted', '0') == '1'
    if show_deleted:
        aircraft_list = Aircraft.query.order_by(Aircraft.tail_number).all()
    else:
        aircraft_list = Aircraft.query.filter_by(is_deleted=False).order_by(Aircraft.tail_number).all()

    return render_template(
        'fleet/index.html',
        aircrafts=aircraft_list,
        show_deleted=show_deleted
    )

@bp.route('/create', methods=['GET', 'POST'])
@admin_required
def create():
    """CREATE: Add a new aircraft to the fleet."""
    form = AircraftForm()
    models = AircraftModel.query.filter_by(is_deleted=False).all()
    form.model_id.choices = [(m.id, f"{m.model_name} ({m.manufacturer.name})") for m in models]

    if form.validate_on_submit():
        aircraft = Aircraft(
            model_id=form.model_id.data,
            tail_number=form.tail_number.data.strip().upper(),
            serial_number=form.serial_number.data.strip().upper(),
            manufacture_date=form.manufacture_date.data,
            status=form.status.data,
            total_flight_hours=float(form.total_flight_hours.data or 0.0)
        )
        db.session.add(aircraft)
        db.session.commit()

        flash(f"Aircraft {aircraft.tail_number} successfully registered in fleet!", "success")
        return redirect(url_for('fleet.details', id=aircraft.id))

    return render_template('fleet/create.html', form=form)

@bp.route('/<int:id>')
def details(id):
    """READ: View detailed aircraft profile and maintenance records."""
    aircraft = Aircraft.query.get_or_404(id)
    maintenance_records = MaintenanceLog.query.filter_by(
        aircraft_id=id, is_deleted=False
    ).order_by(MaintenanceLog.scheduled_date.desc()).all()

    return render_template('fleet/details.html', aircraft=aircraft, logs=maintenance_records)

@bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@admin_required
def edit(id):
    """UPDATE: Edit aircraft details."""
    aircraft = Aircraft.query.filter_by(id=id, is_deleted=False).first_or_404()
    form = AircraftForm(obj=aircraft)

    models = AircraftModel.query.filter_by(is_deleted=False).all()
    form.model_id.choices = [(m.id, f"{m.model_name} ({m.manufacturer.name})") for m in models]

    if form.validate_on_submit():
        aircraft.model_id = form.model_id.data
        aircraft.tail_number = form.tail_number.data.strip().upper()
        aircraft.serial_number = form.serial_number.data.strip().upper()
        aircraft.manufacture_date = form.manufacture_date.data
        aircraft.status = form.status.data
        aircraft.total_flight_hours = float(form.total_flight_hours.data or 0.0)
        db.session.commit()

        flash(f"Aircraft {aircraft.tail_number} updated successfully.", "success")
        return redirect(url_for('fleet.details', id=aircraft.id))

    return render_template('fleet/edit.html', form=form, aircraft=aircraft)

@bp.route('/<int:id>/delete', methods=['POST'])
@admin_required
def delete(id):
    """DELETE: Soft-delete an aircraft from active operational status."""
    aircraft = Aircraft.query.filter_by(id=id, is_deleted=False).first_or_404()
    aircraft.status = 'Retired'
    aircraft.soft_delete()

    flash(f"Aircraft {aircraft.tail_number} has been soft-deleted (archived).", "warning")
    return redirect(url_for('fleet.index'))

@bp.route('/<int:id>/restore', methods=['POST'])
@admin_required
def restore(id):
    """RESTORE: Re-activate a soft-deleted aircraft."""
    aircraft = Aircraft.query.get_or_404(id)
    aircraft.restore()
    aircraft.status = 'Active'
    db.session.commit()

    flash(f"Aircraft {aircraft.tail_number} restored to active status.", "success")
    return redirect(url_for('fleet.details', id=aircraft.id))

@bp.route('/maintenance')
def maintenance():
    """READ: List all maintenance inspections."""
    logs = MaintenanceLog.query.filter_by(is_deleted=False).order_by(MaintenanceLog.scheduled_date.desc()).all()
    return render_template('fleet/maintenance.html', logs=logs)

@bp.route('/maintenance/new', methods=['GET', 'POST'])
@admin_required
def new_maintenance():
    """CREATE: Schedule new maintenance inspection."""
    form = MaintenanceLogForm()
    aircrafts = Aircraft.query.filter_by(is_deleted=False).all()
    form.aircraft_id.choices = [(a.id, f"{a.tail_number} - {a.model.model_name}") for a in aircrafts]

    mtypes = MaintenanceType.query.filter_by(is_deleted=False).all()
    form.maintenance_type_id.choices = [(t.id, f"{t.code} ({t.name})") for t in mtypes]

    if form.validate_on_submit():
        log = MaintenanceLog(
            aircraft_id=form.aircraft_id.data,
            maintenance_type_id=form.maintenance_type_id.data,
            scheduled_date=form.scheduled_date.data,
            completed_date=form.completed_date.data,
            lead_technician=form.lead_technician.data.strip(),
            status=form.status.data,
            cost_estimate=form.cost_estimate.data or 0.00,
            notes=form.notes.data
        )
        db.session.add(log)
        db.session.commit()

        flash("Maintenance inspection scheduled successfully.", "success")
        return redirect(url_for('fleet.maintenance'))

    return render_template('fleet/new_maintenance.html', form=form)
