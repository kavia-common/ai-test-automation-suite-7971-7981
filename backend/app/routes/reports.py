from flask.views import MethodView
from flask_smorest import Blueprint, abort

from ..models import Report
from ..schemas import ReportSchema

blp = Blueprint(
    "Reports",
    "reports",
    url_prefix="/api/reports",
    description="Access execution reports",
)


@blp.route("/")
class ReportsListResource(MethodView):
    @blp.response(200, ReportSchema(many=True), description="List all reports")
    def get(self):
        """List all reports."""
        return Report.query.order_by(Report.id.desc()).all()


@blp.route("/by-execution/<int:execution_id>")
class ReportsByExecutionResource(MethodView):
    @blp.response(200, ReportSchema, description="Get report by execution id")
    def get(self, execution_id: int):
        """Get a single report by execution id."""
        rep = Report.query.filter_by(execution_id=execution_id).first()
        if not rep:
            abort(404, message="Report not found")
        return rep


@blp.route("/<int:execution_id>")
class ReportsAliasByExecutionResource(MethodView):
    @blp.response(
        200,
        ReportSchema,
        description="Alias of /api/reports/by-execution/{execution_id} for backward compatibility",
    )
    def get(self, execution_id: int):
        """
        Alias endpoint that proxies to the by-execution route.

        This maintains backward compatibility with older clients expecting:
        GET /api/reports/<execution_id>

        Path params:
        - execution_id: integer

        Returns:
        - ReportSchema for the given execution_id, or 404 if not found.
        """
        rep = Report.query.filter_by(execution_id=execution_id).first()
        if not rep:
            abort(404, message="Report not found")
        return rep
