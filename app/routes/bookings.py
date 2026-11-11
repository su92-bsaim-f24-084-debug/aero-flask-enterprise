import uuid
from datetime import datetime
from decimal import Decimal
from flask import Blueprint, render_template, redirect, url_for, flash, request, g
from app.models import (
    db, Booking, Ticket, Passenger, EmergencyContact, FlightInstance,
    FareClass, FlightPrice, BoardingPass, PromoCode, PaymentTransaction
)
from app.forms import BookingPassengerForm
from app.utils import login_required

bp = Blueprint('bookings', __name__, url_prefix='/bookings')

@bp.route('/new/<int:flight_id>', methods=['GET', 'POST'])
@login_required
def create(flight_id):
    """Create a new booking and issue e-ticket with server-side validation and PRG pattern."""
    flight = FlightInstance.query.filter_by(id=flight_id, is_deleted=False).first_or_404()
    fare_classes = FareClass.query.filter_by(is_deleted=False).all()

    form = BookingPassengerForm()
    form.fare_class_id.choices = [(fc.id, f"{fc.name} - Changes: ${fc.change_fee}") for fc in fare_classes]

    if form.validate_on_submit():
        selected_fare_class = FareClass.query.get(form.fare_class_id.data)
        
        # Calculate base price from flight prices or default
        flight_price = FlightPrice.query.filter_by(
            flight_instance_id=flight.id,
            fare_class_id=selected_fare_class.id,
            is_deleted=False
        ).first()

        base_fare = flight_price.base_fare if flight_price else Decimal('250.00')
        tax = flight_price.tax_amount if flight_price else Decimal('35.00')
        total_price = base_fare + tax

        # Check Promo Code
        discount = Decimal('0.00')
        if form.promo_code.data:
            promo = PromoCode.query.filter_by(
                code=form.promo_code.data.strip().upper(),
                is_active=True,
                is_deleted=False
            ).first()
            if promo and promo.used_count < promo.usage_limit:
                discount = (total_price * Decimal(promo.discount_percentage)) / Decimal('100.00')
                if promo.max_discount_amount and discount > promo.max_discount_amount:
                    discount = promo.max_discount_amount
                promo.used_count += 1
                flash(f"Promo code {promo.code} applied! Saved ${discount:.2f}", "success")
            else:
                flash("Invalid or expired promo code.", "warning")

        final_total = max(Decimal('10.00'), total_price - discount)

        # Generate unique PNR (6 chars)
        pnr = f"AER{uuid.uuid4().hex[:5].upper()}"

        # 1. Create Booking Record
        booking = Booking(
            user_id=g.user.id,
            booking_reference=pnr,
            booking_date=datetime.utcnow(),
            total_amount=final_total,
            booking_status='Confirmed',
            payment_status='Paid'
        )
        db.session.add(booking)
        db.session.flush()

        # 2. Create Passenger Record
        passenger = Passenger(
            booking_id=booking.id,
            user_id=g.user.id,
            first_name=form.first_name.data.strip(),
            last_name=form.last_name.data.strip(),
            gender=form.gender.data,
            date_of_birth=form.date_of_birth.data,
            passport_number=form.passport_number.data.strip().upper(),
            nationality=form.nationality.data.strip()
        )
        db.session.add(passenger)
        db.session.flush()

        # 3. Create Emergency Contact
        emergency = EmergencyContact(
            passenger_id=passenger.id,
            full_name=form.emergency_name.data.strip(),
            phone_number=form.emergency_phone.data.strip(),
            relationship=form.emergency_relation.data.strip()
        )
        db.session.add(emergency)

        # 4. Issue Ticket
        ticket_number = f"065-{uuid.uuid4().int % 10000000000:010d}"
        ticket = Ticket(
            booking_id=booking.id,
            flight_instance_id=flight.id,
            passenger_id=passenger.id,
            fare_class_id=selected_fare_class.id,
            ticket_number=ticket_number,
            fare_paid=final_total,
            status='Issued'
        )
        db.session.add(ticket)

        # 5. Record Payment Transaction
        tx = PaymentTransaction(
            booking_id=booking.id,
            transaction_reference=f"TXN-{uuid.uuid4().hex[:12].upper()}",
            amount=final_total,
            currency='USD',
            status='Completed'
        )
        db.session.add(tx)

        db.session.commit()

        flash(f"Booking confirmed! Your PNR reference is {booking.booking_reference}.", "success")
        return redirect(url_for('bookings.view', id=booking.id))

    return render_template('bookings/new.html', flight=flight, form=form)

@bp.route('/<int:id>')
@login_required
def view(id):
    """Read booking details and e-ticket."""
    booking = Booking.query.filter_by(id=id, is_deleted=False).first_or_404()
    if booking.user_id != g.user.id and not g.user.is_admin():
        flash("Access unauthorized.", "danger")
        return redirect(url_for('bookings.my_bookings'))

    return render_template('bookings/view.html', booking=booking)

@bp.route('/my-bookings')
@login_required
def my_bookings():
    """List bookings for the authenticated user."""
    user_bookings = Booking.query.filter_by(
        user_id=g.user.id,
        is_deleted=False
    ).order_by(Booking.booking_date.desc()).all()
    return render_template('bookings/my_bookings.html', bookings=user_bookings)

@bp.route('/<int:id>/cancel', methods=['POST'])
@login_required
def cancel(id):
    """Soft delete / cancel a booking with audit tracking."""
    booking = Booking.query.filter_by(id=id, is_deleted=False).first_or_404()
    if booking.user_id != g.user.id and not g.user.is_admin():
        flash("Access unauthorized.", "danger")
        return redirect(url_for('bookings.my_bookings'))

    # Soft delete the booking and related tickets
    booking.booking_status = 'Cancelled'
    booking.soft_delete()

    for ticket in booking.tickets:
        ticket.status = 'Cancelled'
        ticket.soft_delete()

    flash(f"Booking {booking.booking_reference} has been successfully cancelled (soft-deleted).", "info")
    return redirect(url_for('bookings.my_bookings'))

@bp.route('/checkin/<int:ticket_id>', methods=['POST'])
@login_required
def checkin(ticket_id):
    """Online check-in: generate boarding pass and barcode."""
    ticket = Ticket.query.filter_by(id=ticket_id, is_deleted=False).first_or_404()
    if ticket.booking.user_id != g.user.id and not g.user.is_admin():
        flash("Unauthorized check-in attempt.", "danger")
        return redirect(url_for('bookings.my_bookings'))

    if ticket.boarding_pass:
        flash("Boarding pass already issued.", "info")
        return redirect(url_for('bookings.view', id=ticket.booking_id))

    # Generate boarding pass
    bp_record = BoardingPass(
        ticket_id=ticket.id,
        sequence_number=101 + ticket.id,
        boarding_group='B',
        gate_number=ticket.flight_instance.departure_gate.gate_number if ticket.flight_instance.departure_gate else 'TBD',
        boarding_time=ticket.flight_instance.flight_date,
        barcode_hash=uuid.uuid4().hex
    )
    ticket.status = 'CheckedIn'
    db.session.add(bp_record)
    db.session.commit()

    flash("Check-in successful! Your digital boarding pass has been generated.", "success")
    return redirect(url_for('bookings.view', id=ticket.booking_id))
