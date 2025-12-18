from flask.views import MethodView
from flask_smorest import Blueprint, abort

from ..repository import create_execution, update_execution
from ..models import Execution
from ..schemas import ExecutionCreateSchema, ExecutionSchema
from ..services.executor import trigger_execution

blp = Blueprint(
    "Executions",
    "executions",
    url_prefix="/api/executions",
    description="Trigger and poll test executions",
)


@blp.route("/")
class ExecutionsResource(MethodView):
    @blp.arguments(ExecutionCreateSchema)
    @blp.response(201, ExecutionSchema, description="Create and queue a new execution")
    def post(self, json_data):
        """Create a new execution for a given test case and immediately trigger it."""
        exe = create_execution(test_case_id=json_data["test_case_id"], status="queued")
        if not exe:
            abort(404, message="Test case not found")
        # Simulate trigger
        trigger_execution(exe)
        # Reload object to reflect latest state
        exe = Execution.query.get(exe.id)
        return exe


@blp.route("/<int:execution_id>")
class ExecutionDetailResource(MethodView):
    @blp.response(200, ExecutionSchema, description="Get execution status/details")
    def get(self, execution_id: int):
        """Get execution details."""
        exe = Execution.query.get(execution_id)
        if not exe:
            abort(404, message="Execution not found")
        return exe

    @blp.response(200, ExecutionSchema, description="Cancel execution (stub)")
    def delete(self, execution_id: int):
        """Cancel an execution (stub implementation marks as failed if running/queued)."""
        exe = Execution.query.get(execution_id)
        if not exe:
            abort(404, message="Execution not found")
        if exe.status in ("queued", "running"):
            update_execution(execution_id, status="failed")
            exe = Execution.query.get(execution_id)
        return exe
