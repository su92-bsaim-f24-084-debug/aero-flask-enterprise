from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class TimestampMixin:
    """Provides automatic audit timestamps for all database records."""
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

class SoftDeleteMixin:
    """
    Implements soft delete capability across all tables.
    Data is never physically erased from the database; instead, is_deleted is flagged
    and deleted_at is recorded, maintaining historical integrity and audit compliance.
    """
    is_deleted = db.Column(db.Boolean, default=False, nullable=False, index=True)
    deleted_at = db.Column(db.DateTime, nullable=True)

    def soft_delete(self):
        """Flags record as deleted without dropping row."""
        self.is_deleted = True
        self.deleted_at = datetime.utcnow()
        db.session.commit()

    def restore(self):
        """Restores a soft-deleted record back to active state."""
        self.is_deleted = False
        self.deleted_at = None
        db.session.commit()
