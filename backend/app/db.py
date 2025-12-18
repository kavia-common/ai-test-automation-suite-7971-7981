import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Single SQLAlchemy instance to be imported by models and other modules
db = SQLAlchemy()


# PUBLIC_INTERFACE
def init_app(app: Flask) -> None:
    """Initialize database integration with the provided Flask app.

    This sets up the SQLALCHEMY_DATABASE_URI and binds the SQLAlchemy instance.

    Configuration:
    - Uses environment variable DATABASE_URL if provided.
    - Otherwise defaults to sqlite database at instance/app.db (created automatically).

    Args:
        app: The Flask application instance to configure and initialize.

    Returns:
        None. The function initializes global db and creates tables if necessary.
    """
    # Prefer env var DATABASE_URL when provided, otherwise default to sqlite in instance folder.
    default_sqlite_path = os.path.join(app.instance_path, "app.db")
    default_uri = f"sqlite:///{default_sqlite_path}"
    database_uri = os.getenv("DATABASE_URL", default_uri)

    # Ensure instance folder exists for sqlite storage
    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError:
        # If running in restrictive environment, ignore inability to pre-create
        pass

    app.config.setdefault("SQLALCHEMY_DATABASE_URI", database_uri)
    # Disable tracking modifications overhead unless needed
    app.config.setdefault("SQLALCHEMY_TRACK_MODIFICATIONS", False)

    db.init_app(app)

    # Create tables on startup
    with app.app_context():
        from .models import TestCase, Execution, Report  # noqa: F401

        db.create_all()
