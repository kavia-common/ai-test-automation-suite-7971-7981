from datetime import datetime
from typing import Optional

from .db import db


class TimestampMixin:
    """Adds created_at and updated_at timestamps to models."""
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )


class TestCase(db.Model, TimestampMixin):
    """Represents a test case managed by the system."""
    __tablename__ = "test_cases"

    id = db.Column(db.Integer, primary_key=True)
    title = db.LargeBinary().with_variant(db.String(255), "sqlite")  # safe default on sqlite
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(50), nullable=False, default="draft")

    executions = db.relationship("Execution", backref="test_case", lazy=True)


class Execution(db.Model, TimestampMixin):
    """Represents a single execution of a test case."""
    __tablename__ = "executions"

    id = db.Column(db.Integer, primary_key=True)
    test_case_id = db.Column(db.Integer, db.ForeignKey("test_cases.id"), nullable=False)
    status = db.Column(db.String(50), nullable=False, default="queued")
    started_at: Optional[datetime] = db.Column(db.DateTime, nullable=True)
    finished_at: Optional[datetime] = db.Column(db.DateTime, nullable=True)

    report = db.relationship("Report", backref="execution", uselist=False, lazy=True)


class Report(db.Model, TimestampMixin):
    """Represents an execution report with results and logs."""
    __tablename__ = "reports"

    id = db.Column(db.Integer, primary_key=True)
    execution_id = db.Column(db.Integer, db.ForeignKey("executions.id"), nullable=False)
    summary = db.Column(db.Text, nullable=True)
    details = db.Column(db.Text, nullable=True)
