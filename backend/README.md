# AI Test Automation Suite - Backend

Flask backend for the AI-enabled testing framework. Provides REST APIs for:
- Health: GET /
- Tests CRUD: /api/tests
- Executions: /api/executions
- Reports: /api/reports (including alias /api/reports/{execution_id})
- AI Generate: POST /api/ai/generate-tests (and alias /api/ai/tests/generate)

Swagger UI is served at /docs and OpenAPI JSON is available at /openapi.json.

## Environment Variables

- DATABASE_URL: Optional SQLAlchemy database URI. Defaults to SQLite at instance/app.db.
- REACT_APP_FRONTEND_URL: Frontend origin for CORS allowlist (e.g., https://host:3000). If not set, permissive defaults are used for local development.

## CORS

The backend enables CORS with flask-cors. It prefers an explicit frontend origin via `REACT_APP_FRONTEND_URL`. If unset, it allows:
- http://localhost:* and http://127.0.0.1:* (development)

For preview environments, set:
- REACT_APP_FRONTEND_URL=https://vscode-internal-36116-beta.beta01.cloud.kavia.ai:3000

This ensures requests from the frontend preview are accepted without additional configuration.

## Running locally

1. Create venv and install dependencies:
   - pip install -r requirements.txt
2. Run the app:
   - python run.py
3. Visit:
   - http://localhost:5000/ (health)
   - http://localhost:5000/docs (Swagger UI)

## Notes

- Tables are auto-created on startup (SQLite by default).
- Execution service is a stub that immediately completes with a "passed" status and generates a simple report.
- The /docs and /openapi.json endpoints are provided by flask-smorest. If these endpoints fail, verify environment variables and that CORS resources are configured as `{r"/*": {"origins": ...}}` (already set in app/__init__.py).
