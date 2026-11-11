import os
import sys
from datetime import datetime, date, time, timedelta
from decimal import Decimal
import uuid

# Ensure application context can be loaded
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import create_app
from app.models import (
    db, Country, City, Airport, AirportTerminal, AirportGate, AirportRunway,
    AircraftManufacturer, AircraftModel, Aircraft, CabinClass, AircraftSeatLayout,
    AircraftSeat, MaintenanceType, MaintenanceLog, AircraftPart,
    Route, FlightSchedule, FlightInstance, FlightPrice, FareClass,
    Department, EmployeeRole, Employee,
    User, UserProfile, Passenger, EmergencyContact, Booking, Ticket, BoardingPass,
    BaggagePolicy, MealOption, AncillaryService,
    PaymentMethod, PaymentTransaction, PromoCode, LoyaltyProgram, LoyaltyMember
)

app = create_app('development')

def seed_database():
    """Populates the database with realistic sample airline operations data."""
    with app.app_context():
        print("Creating all tables across 51 models...")
        db.create_all()
        print("Database tables initialized successfully!")

        # 1. Countries
        if Country.query.count() == 0:
            print("Seeding Countries & Cities...")
            c_us = Country(name="United States", iso_code="USA", continent="North America")
            c_uk = Country(name="United Kingdom", iso_code="GBR", continent="Europe")
            c_fr = Country(name="France", iso_code="FRA", continent="Europe")
            c_ae = Country(name="United Arab Emirates", iso_code="ARE", continent="Asia")
            c_jp = Country(name="Japan", iso_code="JPN", continent="Asia")
            c_pk = Country(name="Pakistan", iso_code="PAK", continent="Asia")
            db.session.add_all([c_us, c_uk, c_fr, c_ae, c_jp, c_pk])
            db.session.flush()

            # 2. Cities
            city_nyc = City(country_id=c_us.id, name="New York", timezone="America/New_York")
            city_lon = City(country_id=c_uk.id, name="London", timezone="Europe/London")
            city_par = City(country_id=c_fr.id, name="Paris", timezone="Europe/Paris")
            city_dxb = City(country_id=c_ae.id, name="Dubai", timezone="Asia/Dubai")
            city_tyo = City(country_id=c_jp.id, name="Tokyo", timezone="Asia/Tokyo")
            city_lhe = City(country_id=c_pk.id, name="Lahore", timezone="Asia/Karachi")
            db.session.add_all([city_nyc, city_lon, city_par, city_dxb, city_tyo, city_lhe])
            db.session.flush()

            # 3. Airports
            print("Seeding Airports, Terminals & Gates...")
            apt_jfk = Airport(city_id=city_nyc.id, name="John F. Kennedy International", iata_code="JFK", icao_code="KJFK", latitude=40.6413, longitude=-73.7781, elevation_ft=13)
            apt_lhr = Airport(city_id=city_lon.id, name="London Heathrow", iata_code="LHR", icao_code="EGLL", latitude=51.4700, longitude=-0.4543, elevation_ft=83)
            apt_cdg = Airport(city_id=city_par.id, name="Paris Charles de Gaulle", iata_code="CDG", icao_code="LFPG", latitude=49.0097, longitude=2.5479, elevation_ft=392)
            apt_dxb = Airport(city_id=city_dxb.id, name="Dubai International", iata_code="DXB", icao_code="OMDB", latitude=25.2532, longitude=55.3657, elevation_ft=62)
            apt_hnd = Airport(city_id=city_tyo.id, name="Tokyo Haneda", iata_code="HND", icao_code="RJTT", latitude=35.5494, longitude=139.7798, elevation_ft=35)
            apt_lhe = Airport(city_id=city_lhe.id, name="Allama Iqbal International", iata_code="LHE", icao_code="OPLA", latitude=31.5216, longitude=74.4036, elevation_ft=712)
            db.session.add_all([apt_jfk, apt_lhr, apt_cdg, apt_dxb, apt_hnd, apt_lhe])
            db.session.flush()

            # Terminals & Gates for JFK & LHR
            t1 = AirportTerminal(airport_id=apt_jfk.id, terminal_code="T4", name="Terminal 4 International")
            t2 = AirportTerminal(airport_id=apt_lhr.id, terminal_code="T5", name="Terminal 5 Grand Concourse")
            db.session.add_all([t1, t2])
            db.session.flush()

            g1 = AirportGate(terminal_id=t1.id, gate_number="B24", gate_type="International")
            g2 = AirportGate(terminal_id=t2.id, gate_number="A10", gate_type="International")
            db.session.add_all([g1, g2])

            # Runways
            rw1 = AirportRunway(airport_id=apt_jfk.id, runway_identifier="04L/22R", length_ft=12079, surface_type="Concrete")
            rw2 = AirportRunway(airport_id=apt_lhr.id, runway_identifier="09L/27R", length_ft=12802, surface_type="Asphalt")
            db.session.add_all([rw1, rw2])

            # 4. Fleet & Aircraft
            print("Seeding Aircraft Manufacturers, Models, and Fleet...")
            mfg_boeing = AircraftManufacturer(name="The Boeing Company", country="USA", founded_year=1916, website="https://boeing.com")
            mfg_airbus = AircraftManufacturer(name="Airbus SAS", country="France", founded_year=1970, website="https://airbus.com")
            db.session.add_all([mfg_boeing, mfg_airbus])
            db.session.flush()

            model_787 = AircraftModel(manufacturer_id=mfg_boeing.id, model_name="Boeing 787-9 Dreamliner", engine_type="Turbofan GEnx", max_range_km=14140, cruise_speed_kmh=903, seating_capacity=296)
            model_350 = AircraftModel(manufacturer_id=mfg_airbus.id, model_name="Airbus A350-900", engine_type="Rolls-Royce Trent XWB", max_range_km=15000, cruise_speed_kmh=903, seating_capacity=315)
            model_320 = AircraftModel(manufacturer_id=mfg_airbus.id, model_name="Airbus A320neo", engine_type="CFM LEAP-1A", max_range_km=6300, cruise_speed_kmh=828, seating_capacity=180)
            db.session.add_all([model_787, model_350, model_320])
            db.session.flush()

            ac1 = Aircraft(model_id=model_787.id, tail_number="N-787AF", serial_number="MSN-38901", manufacture_date=date(2022, 5, 14), status="Active", total_flight_hours=3250.5)
            ac2 = Aircraft(model_id=model_350.id, tail_number="F-350AF", serial_number="MSN-49120", manufacture_date=date(2023, 2, 20), status="Active", total_flight_hours=1840.0)
            ac3 = Aircraft(model_id=model_320.id, tail_number="AP-320AF", serial_number="MSN-51203", manufacture_date=date(2021, 9, 10), status="Active", total_flight_hours=5120.2)
            db.session.add_all([ac1, ac2, ac3])
            db.session.flush()

            # Cabin Classes
            c_eco = CabinClass(name="Economy", code="Y", description="Standard comfortable seating with in-flight entertainment.")
            c_peco = CabinClass(name="Premium Economy", code="W", description="Extra legroom, priority boarding, and enhanced dining.")
            c_biz = CabinClass(name="Business Class", code="J", description="Lie-flat seats, direct aisle access, and gourmet dining.")
            c_first = CabinClass(name="First Class", code="F", description="Private luxury suites and premium champagne service.")
            db.session.add_all([c_eco, c_peco, c_biz, c_first])
            db.session.flush()

            # Aircraft Seats (Sample batch for ac1)
            for row in range(1, 6):
                for col in ['A', 'B', 'C', 'D', 'E', 'F']:
                    c_id = c_biz.id if row <= 2 else c_eco.id
                    seat = AircraftSeat(
                        aircraft_id=ac1.id,
                        cabin_class_id=c_id,
                        seat_number=f"{row}{col}",
                        row_number=row,
                        column_letter=col,
                        is_window=(col in ['A', 'F']),
                        is_aisle=(col in ['C', 'D']),
                        is_exit_row=(row == 4)
                    )
                    db.session.add(seat)

            # Maintenance Types & Sample Log
            mt_a = MaintenanceType(code="A-CHECK", name="Routine Systems Inspection", interval_days=60, description="Comprehensive systems and fluids inspection.")
            mt_c = MaintenanceType(code="C-CHECK", name="Structural & Major Overhaul", interval_days=730, description="Deep structural non-destructive testing.")
            db.session.add_all([mt_a, mt_c])
            db.session.flush()

            m_log = MaintenanceLog(
                aircraft_id=ac1.id,
                maintenance_type_id=mt_a.id,
                scheduled_date=date(2026, 2, 10),
                completed_date=date(2026, 2, 11),
                lead_technician="Chief Eng. David Clark",
                status="Completed",
                cost_estimate=Decimal('12500.00'),
                notes="Standard 60-day line inspection completed. All avionics, APU, and landing gear certified airworthy."
            )
            db.session.add(m_log)

            # 5. Direct Routes & Schedules
            print("Seeding Routes, Schedules & Flight Instances...")
            r_jfk_lhr = Route(origin_airport_id=apt_jfk.id, destination_airport_id=apt_lhr.id, distance_km=5567.0, estimated_flight_minutes=420, is_active=True)
            r_lhr_dxb = Route(origin_airport_id=apt_lhr.id, destination_airport_id=apt_dxb.id, distance_km=5500.0, estimated_flight_minutes=410, is_active=True)
            r_dxb_hnd = Route(origin_airport_id=apt_dxb.id, destination_airport_id=apt_hnd.id, distance_km=7935.0, estimated_flight_minutes=560, is_active=True)
            r_jfk_cdg = Route(origin_airport_id=apt_jfk.id, destination_airport_id=apt_cdg.id, distance_km=5835.0, estimated_flight_minutes=440, is_active=True)
            r_dxb_lhe = Route(origin_airport_id=apt_dxb.id, destination_airport_id=apt_lhe.id, distance_km=1980.0, estimated_flight_minutes=195, is_active=True)
            db.session.add_all([r_jfk_lhr, r_lhr_dxb, r_dxb_hnd, r_jfk_cdg, r_dxb_lhe])
            db.session.flush()

            # Flight Schedules
            sch1 = FlightSchedule(route_id=r_jfk_lhr.id, flight_number="AF-101", scheduled_departure_time=time(18, 30), scheduled_arrival_time=time(6, 30), days_of_week="Daily")
            sch2 = FlightSchedule(route_id=r_lhr_dxb.id, flight_number="AF-204", scheduled_departure_time=time(9, 15), scheduled_arrival_time=time(19, 45), days_of_week="Daily")
            sch3 = FlightSchedule(route_id=r_dxb_hnd.id, flight_number="AF-310", scheduled_departure_time=time(2, 45), scheduled_arrival_time=time(17, 25), days_of_week="Mon/Wed/Fri")
            sch4 = FlightSchedule(route_id=r_jfk_cdg.id, flight_number="AF-405", scheduled_departure_time=time(20, 0), scheduled_arrival_time=time(9, 20), days_of_week="Daily")
            sch5 = FlightSchedule(route_id=r_dxb_lhe.id, flight_number="AF-512", scheduled_departure_time=time(14, 20), scheduled_arrival_time=time(18, 35), days_of_week="Daily")
            db.session.add_all([sch1, sch2, sch3, sch4, sch5])
            db.session.flush()

            # Generate Flight Instances for current and upcoming 14 days
            base_date = date.today()
            sample_instance = None
            for offset in range(14):
                f_date = base_date + timedelta(days=offset)
                inst1 = FlightInstance(
                    schedule_id=sch1.id,
                    aircraft_id=ac1.id,
                    departure_gate_id=g1.id,
                    arrival_gate_id=g2.id,
                    flight_date=f_date,
                    status="Scheduled"
                )
                inst2 = FlightInstance(
                    schedule_id=sch2.id,
                    aircraft_id=ac2.id,
                    departure_gate_id=g2.id,
                    arrival_gate_id=None,
                    flight_date=f_date,
                    status="Scheduled"
                )
                inst3 = FlightInstance(
                    schedule_id=sch5.id,
                    aircraft_id=ac3.id,
                    departure_gate_id=None,
                    arrival_gate_id=None,
                    flight_date=f_date,
                    status="Scheduled"
                )
                db.session.add_all([inst1, inst2, inst3])
                if offset == 0:
                    sample_instance = inst1
            db.session.flush()

            # 6. Fare Classes & Pricing
            print("Seeding Fare Classes and Pricing...")
            fc_sav = FareClass(name="Economy Saver", code="ECO-SAV", is_refundable=False, change_fee=Decimal('100.00'), miles_earning_rate=0.5)
            fc_flx = FareClass(name="Economy Flex", code="ECO-FLX", is_refundable=True, change_fee=Decimal('25.00'), miles_earning_rate=1.0)
            fc_biz = FareClass(name="Business Premier", code="BIZ-PREM", is_refundable=True, change_fee=Decimal('0.00'), miles_earning_rate=2.0)
            db.session.add_all([fc_sav, fc_flx, fc_biz])
            db.session.flush()

            # Set price for sample instance
            if sample_instance:
                p1 = FlightPrice(flight_instance_id=sample_instance.id, cabin_class_id=c_eco.id, fare_class_id=fc_sav.id, base_fare=Decimal('245.00'), tax_amount=Decimal('35.00'), available_seats=150)
                p2 = FlightPrice(flight_instance_id=sample_instance.id, cabin_class_id=c_eco.id, fare_class_id=fc_flx.id, base_fare=Decimal('320.00'), tax_amount=Decimal('40.00'), available_seats=80)
                p3 = FlightPrice(flight_instance_id=sample_instance.id, cabin_class_id=c_biz.id, fare_class_id=fc_biz.id, base_fare=Decimal('1250.00'), tax_amount=Decimal('120.00'), available_seats=24)
                db.session.add_all([p1, p2, p3])

            # 7. Ancillaries, Meals & Baggage Policies
            bp_eco = BaggagePolicy(cabin_class_id=c_eco.id, max_free_pieces=1, max_weight_kg_per_piece=23.0, excess_charge_per_kg=Decimal('15.00'))
            bp_biz = BaggagePolicy(cabin_class_id=c_biz.id, max_free_pieces=2, max_weight_kg_per_piece=32.0, excess_charge_per_kg=Decimal('20.00'))
            db.session.add_all([bp_eco, bp_biz])

            m1 = MealOption(code="VGML", name="Vegetarian Meal", description="Fresh seasonal plant-based meal.", is_vegetarian=True)
            m2 = MealOption(code="HNML", name="Halal Certified Meal", description="Prepared in accordance with Islamic dietary laws.", is_vegetarian=False)
            m3 = MealOption(code="KSML", name="Kosher Meal", description="Certified Kosher meal prepared under strict rabbinical supervision.", is_vegetarian=False)
            db.session.add_all([m1, m2, m3])

            s1 = AncillaryService(name="High-Speed In-Flight Wi-Fi", category="Connectivity", price=Decimal('18.00'), description="Full-flight unlimited browsing and messaging streaming pass.")
            s2 = AncillaryService(name="VIP Airport Lounge Pass", category="Lounge", price=Decimal('50.00'), description="Access to premium departures lounge, buffet, and quiet work suites.")
            s3 = AncillaryService(name="Priority Boarding Group A", category="FastTrack", price=Decimal('15.00'), description="Be among the first passengers to board with dedicated overhead bin space.")
            db.session.add_all([s1, s2, s3])

            # 8. Promo Codes & Loyalty Programs
            promo1 = PromoCode(code="SKY20", discount_percentage=20, max_discount_amount=Decimal('150.00'), valid_from=date(2026, 1, 1), valid_to=date(2026, 12, 31), usage_limit=500, used_count=12, is_active=True)
            promo2 = PromoCode(code="WELCOME10", discount_percentage=10, max_discount_amount=Decimal('50.00'), valid_from=date(2026, 1, 1), valid_to=date(2026, 12, 31), usage_limit=1000, used_count=45, is_active=True)
            db.session.add_all([promo1, promo2])

            lp_bronze = LoyaltyProgram(tier_name="Bronze Explorer", min_points_required=0, points_multiplier=1.0)
            lp_silver = LoyaltyProgram(tier_name="Silver Wing", min_points_required=25000, points_multiplier=1.25, priority_boarding=True)
            lp_gold = LoyaltyProgram(tier_name="Gold SkyMaster", min_points_required=50000, points_multiplier=1.5, priority_boarding=True, lounge_access=True, extra_baggage_kg=10.0)
            db.session.add_all([lp_bronze, lp_silver, lp_gold])
            db.session.flush()

            # 9. Departments, Roles & Staff
            dept_ops = Department(name="Flight Operations", description="Flight deck operations, route planning, and dispatch.")
            dept_ground = Department(name="Ground Handling & Customer Care", description="Terminal operations, gate control, and baggage.")
            db.session.add_all([dept_ops, dept_ground])
            db.session.flush()

            role_capt = EmployeeRole(department_id=dept_ops.id, title="Captain / Commander", access_level="FlightCrew")
            role_fo = EmployeeRole(department_id=dept_ops.id, title="First Officer", access_level="FlightCrew")
            db.session.add_all([role_capt, role_fo])
            db.session.flush()

            emp1 = Employee(role_id=role_capt.id, employee_code="EMP-1049", first_name="James", last_name="Sutherland", email="j.sutherland@aeroflask.com", phone="+1-555-0192", hire_date=date(2018, 4, 1))
            db.session.add(emp1)

            # 10. Default System Users
            print("Seeding Users & Accounts...")
            admin_user = User(username="admin", email="admin@aeroflask.com", role="admin")
            admin_user.set_password("AdminPass123!")
            db.session.add(admin_user)
            db.session.flush()

            admin_prof = UserProfile(user_id=admin_user.id, first_name="System", last_name="Administrator", phone_number="+1-555-999-0000")
            db.session.add(admin_prof)

            passenger_user = User(username="passenger1", email="passenger@gmail.com", role="customer")
            passenger_user.set_password("Pass123!")
            db.session.add(passenger_user)
            db.session.flush()

            passenger_prof = UserProfile(user_id=passenger_user.id, first_name="Sarah", last_name="Jenkins", phone_number="+1-555-321-7890", nationality="United States", passport_number="USA9823419")
            db.session.add(passenger_prof)

            # Loyalty member link
            l_member = LoyaltyMember(user_id=passenger_user.id, loyalty_program_id=lp_silver.id, membership_number="AERO-789012", points_balance=32400, lifetime_miles=45600)
            db.session.add(l_member)

            # 11. Initial Confirmed Booking & Ticket
            print("Seeding Initial Booking, Ticket & Boarding Pass...")
            sample_booking = Booking(
                user_id=passenger_user.id,
                booking_reference="AER8912",
                booking_date=datetime.utcnow() - timedelta(days=2),
                total_amount=Decimal('280.00'),
                booking_status="Confirmed",
                payment_status="Paid"
            )
            db.session.add(sample_booking)
            db.session.flush()

            pass_record = Passenger(
                booking_id=sample_booking.id,
                user_id=passenger_user.id,
                first_name="Sarah",
                last_name="Jenkins",
                gender="Female",
                date_of_birth=date(1994, 6, 18),
                passport_number="USA9823419",
                nationality="United States"
            )
            db.session.add(pass_record)
            db.session.flush()

            emerg_contact = EmergencyContact(
                passenger_id=pass_record.id,
                full_name="Mark Jenkins",
                relationship="Brother",
                phone_number="+1-555-888-2121",
                email="m.jenkins@gmail.com"
            )
            db.session.add(emerg_contact)

            sample_ticket = Ticket(
                booking_id=sample_booking.id,
                flight_instance_id=sample_instance.id,
                passenger_id=pass_record.id,
                fare_class_id=fc_sav.id,
                ticket_number="065-2983109283",
                fare_paid=Decimal('280.00'),
                status="CheckedIn"
            )
            db.session.add(sample_ticket)
            db.session.flush()

            sample_bp = BoardingPass(
                ticket_id=sample_ticket.id,
                sequence_number=101,
                boarding_group="A",
                gate_number="B24",
                boarding_time=datetime.utcnow() + timedelta(days=1),
                barcode_hash=uuid.uuid4().hex,
                has_boarded=False
            )
            db.session.add(sample_bp)

            # Commit everything!
            db.session.commit()
            print("Seeding completed successfully! 51 models populated with interconnected data.")

if __name__ == '__main__':
    seed_database()
