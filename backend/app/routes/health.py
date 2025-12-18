from flask_smorest import Blueprint
from flask.views import MethodView

from ..models import TestCase

blp = Blueprint("Health", "health", url_prefix="/", description="Health check route")

@blp.route("/")
class HealthCheck(MethodView):
    def get(self):
        """Return service and DB health."""
        try:
            db_ok = True
            _ = TestCase.query.count()
        except Exception:
            db_ok = False
        return {"message": "Healthy", "database": "ok" if db_ok else "error"}
