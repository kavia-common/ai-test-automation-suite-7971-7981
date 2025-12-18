from flask import Flask
from flask_cors import CORS
from flask_smorest import Api

from .db import init_app as init_db
from .routes.health import blp as health_blp
from .routes.tests import blp as tests_blp
from .routes.executions import blp as executions_blp
from .routes.reports import blp as reports_blp
from .routes.ai import blp as ai_blp

app = Flask(__name__)
app.url_map.strict_slashes = False

# Enable CORS for preview origins and localhost
CORS(
    app,
    resources={r"/**": {"origins": ["*", "http://localhost:*", "http://127.0.0.1:*"]}},
)

# OpenAPI / Swagger UI configuration
app.config["API_TITLE"] = "AI Test Automation Suite API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/docs"
app.config["OPENAPI_SWAGGER_UI_PATH"] = ""
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

# Initialize Smorest and DB
api = Api(app)
init_db(app)

# Register blueprints
api.register_blueprint(health_blp)
api.register_blueprint(tests_blp)
api.register_blueprint(executions_blp)
api.register_blueprint(reports_blp)
api.register_blueprint(ai_blp)
