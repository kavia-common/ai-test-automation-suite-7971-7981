from datetime import datetime
from typing import Optional

from ..repository import update_execution, create_report, get_report
from ..models import Execution, Report

# PUBLIC_INTERFACE
def trigger_execution(execution: Execution) -> Execution:
    """
    Simulate an asynchronous execution trigger.

    For this stub implementation, we mark execution as running immediately,
    set started_at, and also immediately finish with a 'passed' status,
    creating a simple report. Real implementations would enqueue jobs.
    """
    # Start
    update_execution(execution.id, status="running", started_at=datetime.utcnow())
    # Finish
    update_execution(
        execution.id,
        status="passed",
        finished_at=datetime.utcnow(),
    )
    # Create report if not exists
    if not get_report(execution.id):
        create_report(
            execution_id=execution.id,
            summary=f"Execution {execution.id} finished successfully.",
            details="This is a simulated execution result.",
        )
    return execution


# PUBLIC_INTERFACE
def poll_status(execution: Execution) -> str:
    """
    Return the current status for an execution.
    """
    return execution.status


# PUBLIC_INTERFACE
def get_execution_report(execution: Execution) -> Optional[Report]:
    """
    Retrieve report for the given execution.
    """
    return get_report(execution.id)
