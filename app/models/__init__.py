from .base import db, TimestampMixin, SoftDeleteMixin
from .fleet import (
    AircraftManufacturer, AircraftModel, Aircraft, CabinClass,
    AircraftSeatLayout, AircraftSeat, MaintenanceType, MaintenanceLog,
    AircraftPart, PartReplacementLog
)
from .geography import (
    Country, City, Airport, AirportTerminal, AirportGate, AirportRunway
)
from .flights import (
    Route, FlightSchedule, FlightInstance, FlightStatusHistory,
    FlightDelayReason, FlightDelayLog, FlightFuelLog
)
from .crew import (
    Department, EmployeeRole, Employee, PilotCertification,
    CrewSchedule, DutyHourLog
)
from .users import (
    User, UserProfile, Passenger, EmergencyContact
)
from .bookings import (
    FareClass, FlightPrice, Booking, Ticket, SeatReservation, BoardingPass
)
from .services import (
    BaggagePolicy, BaggageItem, MealOption, PassengerMealRequest,
    AncillaryService, AncillaryOrder
)
from .commercial import (
    PaymentMethod, PaymentTransaction, RefundRecord, PromoCode,
    LoyaltyProgram, LoyaltyMember
)

__all__ = [
    'db', 'TimestampMixin', 'SoftDeleteMixin',
    # Fleet (10)
    'AircraftManufacturer', 'AircraftModel', 'Aircraft', 'CabinClass',
    'AircraftSeatLayout', 'AircraftSeat', 'MaintenanceType', 'MaintenanceLog',
    'AircraftPart', 'PartReplacementLog',
    # Geography (6)
    'Country', 'City', 'Airport', 'AirportTerminal', 'AirportGate', 'AirportRunway',
    # Flights (7)
    'Route', 'FlightSchedule', 'FlightInstance', 'FlightStatusHistory',
    'FlightDelayReason', 'FlightDelayLog', 'FlightFuelLog',
    # Crew (6)
    'Department', 'EmployeeRole', 'Employee', 'PilotCertification',
    'CrewSchedule', 'DutyHourLog',
    # Users (4)
    'User', 'UserProfile', 'Passenger', 'EmergencyContact',
    # Bookings (6)
    'FareClass', 'FlightPrice', 'Booking', 'Ticket', 'SeatReservation', 'BoardingPass',
    # Services (6)
    'BaggagePolicy', 'BaggageItem', 'MealOption', 'PassengerMealRequest',
    'AncillaryService', 'AncillaryOrder',
    # Commercial (6)
    'PaymentMethod', 'PaymentTransaction', 'RefundRecord', 'PromoCode',
    'LoyaltyProgram', 'LoyaltyMember'
]
