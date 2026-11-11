import unittest
from datetime import datetime, date
from decimal import Decimal
from app import create_app
from app.models import (
    db, AircraftManufacturer, AircraftModel, Aircraft, User, Booking, Airport
)

class AirlineAppTestCase(unittest.TestCase):
    """Automated test suite verifying Rubric criteria: Models, CRUD, Soft Delete, Routes."""

    def setUp(self):
        self.app = create_app('development')
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_01_fifty_one_models_exist(self):
        """Verify minimum 40 models requirement (we have 51)."""
        from app.models import __all__ as model_symbols
        models = [m for m in model_symbols if m not in ('db', 'TimestampMixin', 'SoftDeleteMixin')]
        self.assertGreaterEqual(len(models), 40)
        self.assertEqual(len(models), 51)
        print(f"[PASS] Minimum 40 models rubric test: {len(models)} models verified.")

    def test_02_soft_delete_lifecycle(self):
        """Verify soft-delete functionality on models."""
        mfg = AircraftManufacturer.query.first()
        model = AircraftModel.query.first()

        # CREATE
        test_ac = Aircraft(
            model_id=model.id,
            tail_number="TEST-999",
            serial_number="MSN-TEST-999",
            manufacture_date=date(2025, 1, 1),
            status="Active"
        )
        db.session.add(test_ac)
        db.session.commit()
        ac_id = test_ac.id

        # READ (Active)
        retrieved = Aircraft.query.filter_by(id=ac_id, is_deleted=False).first()
        self.assertIsNotNone(retrieved)
        self.assertFalse(retrieved.is_deleted)

        # UPDATE
        retrieved.total_flight_hours = 120.5
        db.session.commit()

        # SOFT DELETE
        retrieved.soft_delete()

        # READ after soft delete
        active_check = Aircraft.query.filter_by(id=ac_id, is_deleted=False).first()
        self.assertIsNone(active_check, "Soft deleted record must not appear in active queries")

        deleted_check = Aircraft.query.filter_by(id=ac_id).first()
        self.assertIsNotNone(deleted_check, "Row must physically remain in the database")
        self.assertTrue(deleted_check.is_deleted)
        self.assertIsNotNone(deleted_check.deleted_at)

        # RESTORE
        deleted_check.restore()
        restored_check = Aircraft.query.filter_by(id=ac_id, is_deleted=False).first()
        self.assertIsNotNone(restored_check)
        self.assertFalse(restored_check.is_deleted)

        # Cleanup test object
        db.session.delete(deleted_check)
        db.session.commit()
        print("[PASS] Soft-delete lifecycle (Create, Read, Update, Soft-Delete, Restore) verified.")

    def test_03_public_routes(self):
        """Verify public web endpoints return HTTP 200."""
        routes = ['/', '/about', '/contact', '/flights/search', '/flights/schedules', '/fleet/']
        for route in routes:
            response = self.client.get(route)
            self.assertEqual(response.status_code, 200, f"Route {route} failed with {response.status_code}")
        print("[PASS] Public routes responding with HTTP 200.")

    def test_04_auth_and_session(self):
        """Verify user login, session state, and protected route access."""
        # Unauthenticated access to profile redirects
        res = self.client.get('/auth/profile', follow_redirects=False)
        self.assertEqual(res.status_code, 302)

        # Authenticate with test admin credentials
        login_res = self.client.post('/auth/login', data={
            'username_or_email': 'admin',
            'password': 'AdminPass123!'
        }, follow_redirects=True)
        self.assertEqual(login_res.status_code, 200)

        # Authenticated access to admin schema browser
        admin_res = self.client.get('/admin/schema-browser')
        self.assertEqual(admin_res.status_code, 200)
        self.assertIn(b'51-Model Relational Database Inspector', admin_res.data)
        print("[PASS] Authentication, session state, and role-based access verified.")

    def test_05_api_endpoints(self):
        """Verify JSON API responses."""
        res = self.client.get('/api/health')
        self.assertEqual(res.status_code, 200)
        json_data = res.get_json()
        self.assertEqual(json_data['status'], 'healthy')

        stats_res = self.client.get('/api/stats')
        self.assertEqual(stats_res.status_code, 200)
        stats_data = stats_res.get_json()
        self.assertEqual(stats_data['models_count'], 51)
        print("[PASS] JSON API endpoints verified.")

if __name__ == '__main__':
    unittest.main()
