from flask_smorest import Blueprint
from flask.views import MethodView

from ..models import TestCase

blp = Blueprint("Health", "health", url_prefix="/", description="Health check route")

@blp.route("/")
class HealthCheck(MethodView):
    def get(self):
        """Return service and DB health."""
        try:
            _ = TestCase.query.count()
            db_ok = True
        except Exception:
            db_ok = False
        return {"message": "Healthy", "database": "ok" if db_ok else "error"}

@blp.route("/healthz")
class LivenessCheck(MethodView):
    def get(self):
        """Lightweight liveness endpoint that does not touch the database."""
        return {"status": "ok"}
