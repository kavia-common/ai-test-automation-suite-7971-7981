from typing import List, Optional

from .db import db
from .models import TestCase, Execution, Report


# PUBLIC_INTERFACE
def create_test_case(title: str, description: str = "", status: str = "draft") -> TestCase:
    """Create and persist a new TestCase."""
    obj = TestCase(title=title, description=description, status=status)
    db.session.add(obj)
    db.session.commit()
    return obj


# PUBLIC_INTERFACE
def get_test_case(test_case_id: int) -> Optional[TestCase]:
    """Retrieve a TestCase by id."""
    return TestCase.query.get(test_case_id)


# PUBLIC_INTERFACE
def list_test_cases() -> List[TestCase]:
    """List all TestCases ordered by newest first."""
    return TestCase.query.order_by(TestCase.id.desc()).all()


# PUBLIC_INTERFACE
def update_test_case(test_case_id: int, **fields) -> Optional[TestCase]:
    """Update fields on a TestCase and persist changes."""
    obj = TestCase.query.get(test_case_id)
    if not obj:
        return None
    for k, v in fields.items():
        if hasattr(obj, k):
            setattr(obj, k, v)
    db.session.commit()
    return obj


# PUBLIC_INTERFACE
def delete_test_case(test_case_id: int) -> bool:
    """Delete a TestCase and cascade-delete related objects if configured."""
    obj = TestCase.query.get(test_case_id)
    if not obj:
        return False
    db.session.delete(obj)
    db.session.commit()
    return True


# PUBLIC_INTERFACE
def create_execution(test_case_id: int, status: str = "queued") -> Optional[Execution]:
    """Create an Execution for a given TestCase."""
    if not TestCase.query.get(test_case_id):
        return None
    exe = Execution(test_case_id=test_case_id, status=status)
    db.session.add(exe)
    db.session.commit()
    return exe


# PUBLIC_INTERFACE
def update_execution(execution_id: int, **fields) -> Optional[Execution]:
    """Update an Execution entry."""
    exe = Execution.query.get(execution_id)
    if not exe:
        return None
    for k, v in fields.items():
        if hasattr(exe, k):
            setattr(exe, k, v)
    db.session.commit()
    return exe


# PUBLIC_INTERFACE
def create_report(execution_id: int, summary: str = "", details: str = "") -> Optional[Report]:
    """Create a Report for a given Execution."""
    if not Execution.query.get(execution_id):
        return None
    rep = Report(execution_id=execution_id, summary=summary, details=details)
    db.session.add(rep)
    db.session.commit()
    return rep


# PUBLIC_INTERFACE
def get_report(execution_id: int) -> Optional[Report]:
    """Get a Report by execution id."""
    return Report.query.filter_by(execution_id=execution_id).first()
