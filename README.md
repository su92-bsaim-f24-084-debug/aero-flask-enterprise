# Aero-Flask Enterprise: Airline Management System

[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-3776AB.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Flask 3.0](https://img.shields.io/badge/Flask-3.0.3-000000.svg?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-51_Models-red.svg)](https://www.sqlalchemy.org/)
[![Render](https://img.shields.io/badge/Render-Deployed-46E3B7.svg?logo=render&logoColor=white)](https://render.com)
[![Status](https://img.shields.io/badge/Rubric-100%2F100_Target-success.svg)](#grading-rubric-compliance)

An enterprise-grade, full-stack Airline Management and Commercial Reservation System developed with **Flask**, **SQLAlchemy ORM**, **Jinja2**, **WTForms**, and **Render Cloud Hosting**.

Target Audience: **BS (Data Science) / BS (Artificial Intelligence)**  
Course: **Web Engineering (CSE601330)** — Weeks 5–8 Evaluation (100 Points)

---

## 🌟 Key Features & Rubric Highlights

| Feature / Rubric Area | Implementation & Coverage |
| :--- | :--- |
| **Database Scope (40+ Models)** | **51 fully relational SQLAlchemy models** across 8 operational domains (exceeds the 40-table hard minimum). |
| **Soft Delete Policy** | Every model inherits `SoftDeleteMixin` (`is_deleted`, `deleted_at`). Data is never permanently dropped without audit recovery. |
| **All DB Code in Flask** | 100% pure SQLAlchemy models, migrations, seeds, and CRUD queries directly executed through Flask. |
| **Application Architecture** | Modern **Application Factory Pattern** (`create_app`) with 7 modular blueprints (`auth`, `flights`, `bookings`, `fleet`, `admin`, `api`, `main`). |
| **Forms & Server-Side Validation** | **Flask-WTF** with CSRF tokens, strict server-side validation (`DataRequired`, `Email`, `Length`, cross-field validation). |
| **Sessions & Cookies** | Session-based authentication, user roles (`admin`, `staff`, `customer`), `Remember Me` cookie state, flash messaging with **Post-Redirect-Get (PRG)**. |
| **Templating & Jinja2** | 100% DRY architecture using base template inheritance (`base.html`), navigation bars, responsive modals, and alert components. |
| **Render Cloud Deployment** | Pre-configured `render.yaml`, `Procfile`, and `wsgi.py` for automated zero-downtime deployment on Render. |

---

## 🗄️ Database Architecture (51 Interconnected Models)

The system is organized into **8 decoupled operational subsystems**:

```
app/models/
├── base.py          # db instance, SoftDeleteMixin, TimestampMixin
├── fleet.py         # 10 Models: AircraftManufacturer, AircraftModel, Aircraft, CabinClass,
│                    #           AircraftSeatLayout, AircraftSeat, MaintenanceType, MaintenanceLog,
│                    #           AircraftPart, PartReplacementLog
├── geography.py     # 6 Models:  Country, City, Airport, AirportTerminal, AirportGate, AirportRunway
├── flights.py       # 7 Models:  Route, FlightSchedule, FlightInstance, FlightStatusHistory,
│                    #           FlightDelayReason, FlightDelayLog, FlightFuelLog
├── crew.py          # 6 Models:  Department, EmployeeRole, Employee, PilotCertification,
│                    #           CrewSchedule, DutyHourLog
├── users.py         # 4 Models:  User, UserProfile, Passenger, EmergencyContact
├── bookings.py      # 6 Models:  FareClass, FlightPrice, Booking, Ticket, SeatReservation, BoardingPass
├── services.py      # 6 Models:  BaggagePolicy, BaggageItem, MealOption, PassengerMealRequest,
│                    #           AncillaryService, AncillaryOrder
└── commercial.py    # 6 Models:  PaymentMethod, PaymentTransaction, RefundRecord, PromoCode,
                     #           LoyaltyProgram, LoyaltyMember
```

> **Interactive Schema Explorer**: Log in as an administrator and visit `/admin/schema-browser` to inspect real-time row counts, column definitions, and active vs. soft-deleted statistics for all 51 models.

---

## 🚀 Quickstart Guide (Local Setup)

### 1. Clone & Enter Directory
```bash
git clone https://github.com/su92-bsaim-f24-084-debug/aero-flask-enterprise.git
cd aero-flask-enterprise
```

### 2. Activate Virtual Environment
```powershell
# Windows PowerShell
.\venv\Scripts\Activate.ps1

# Linux / macOS
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Seed the Database
Populate the database with airlines, international airports, commercial fleet, flight routes, schedules, and default accounts:
```bash
python seed.py
```

### 5. Run the Application
```bash
python app.py
```
Open **http://127.0.0.1:5000** in your browser.

---

## 🔐 Default Demo Credentials

| Role | Username / Email | Password | Access Capabilities |
| :--- | :--- | :--- | :--- |
| **System Admin** | `admin` or `admin@aeroflask.com` | `AdminPass123!` | Full control panel, airport/route/promo CRUD, 51-model inspector, soft-delete restores. |
| **Passenger** | `passenger1` or `passenger@gmail.com` | `Pass123!` | Flight booking, digital boarding pass issuance, personal itinerary management, booking cancellation (soft delete). |

---

## 🧪 Automated Testing Suite

Run the built-in test suite to verify rubric criteria, models count, soft-delete lifecycles, and route endpoints:
```bash
python tests.py
```

Expected output:
```text
.....
----------------------------------------------------------------------
Ran 5 tests in 1.4s

OK
[PASS] Minimum 40 models rubric test: 51 models verified.
[PASS] Soft-delete lifecycle (Create, Read, Update, Soft-Delete, Restore) verified.
[PASS] Public routes responding with HTTP 200.
[PASS] Authentication, session state, and role-based access verified.
[PASS] JSON API endpoints verified.
```

---

## ☁️ Deployment on Render

This project is pre-configured for **Render** via `render.yaml` and `Procfile`.

### Steps to Deploy on Render:
1. Log in to [dashboard.render.com](https://dashboard.render.com/).
2. Click **New +** &rarr; **Blueprint** (or **Web Service**).
3. Connect your GitHub repository `aero-flask-enterprise`.
4. Configure environment settings:
   - **Build Command**: `pip install -r requirements.txt && python seed.py`
   - **Start Command**: `gunicorn wsgi:app`
   - **Environment Variables**:
     - `FLASK_CONFIG`: `production`
     - `SECRET_KEY`: *(Auto-generated or enter your random secret)*
     - `DATABASE_URL`: *(Attach Render PostgreSQL internal connection URL or leave blank to use persistent SQLite)*
5. Click **Apply / Deploy**.

---

## 📂 Project Directory Structure

```
d:\web_dev_project_airline\
├── app/
│   ├── __init__.py           # Application Factory (create_app)
│   ├── utils.py              # Auth decorators (login_required, admin_required)
│   ├── models/               # 51 SQLAlchemy models with SoftDeleteMixin
│   ├── forms/                # WTForms server-side validation classes
│   ├── routes/               # Blueprints (main, auth, flights, bookings, fleet, admin, api)
│   ├── templates/            # Jinja2 templates extending base.html
│   └── static/               # CSS, JS, and branding assets
├── instance/                 # Local SQLite database storage
├── config.py                 # Development & Production (PostgreSQL) configs
├── app.py                    # Main application runner & CLI commands
├── wsgi.py                   # Gunicorn WSGI entrypoint for Render
├── seed.py                   # Automated database populator across all 51 models
├── tests.py                  # Automated test suite
├── requirements.txt          # Python dependencies
├── Procfile                  # Render process runner
├── render.yaml               # Render Infrastructure-as-Code blueprint
└── README.md                 # Complete project documentation
```

---

## 📜 Academic Integrity & Course Information
This repository is submitted for the **Web Engineering (CSE601330)** course evaluation. Built with clean architecture, documented models, and adherence to Python PEP 8 conventions.
