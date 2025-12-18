from flask_smorest import Blueprint
from flask.views import MethodView

from ..models import TestCase

blp = Blueprint("Healt Check", "health check", url_prefix="/", description="Health check route")


@blp.route("/")
class HealthCheck(MethodView):
    def get(self):
        # Attempt a simple DB operation to confirm connectivity
        try:
            db_ok = True
            # lightweight query - will also create tables on first run via init_db
            _ = TestCase.query.count()
        except Exception:
            db_ok = False
        return {"message": "Healthy", "database": "ok" if db_ok else "error"}
