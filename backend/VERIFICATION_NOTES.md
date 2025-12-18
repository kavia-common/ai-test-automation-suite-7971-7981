End-to-End Verification Notes

Date: 2025-12-18
Environment:
- Frontend preview: https://vscode-internal-36116-beta.beta01.cloud.kavia.ai:3000
- Backend preview: https://vscode-internal-36116-beta.beta01.cloud.kavia.ai:3001

Observed Failures
- GET / -> 500 Internal Server Error
- GET /docs -> 500 Internal Server Error
- GET /openapi.json -> 500 Internal Server Error
- GET /api/tests -> 500 Internal Server Error

Reproduction (curl):
- curl -sk -D - https://...:3001/ -o -
- curl -sk -D - https://...:3001/docs/ -o -
- curl -sk -D - https://...:3001/openapi.json -o -
- curl -sk -D - https://...:3001/api/tests -o -

Code Review Summary
- Flask app initialization includes:
  - flask-smorest Api with OpenAPI at /docs and swagger UI via CDN
  - CORS enabled with REACT_APP_FRONTEND_URL preference; fallback includes wildcard/localhost
  - DB init (Flask-SQLAlchemy)
  - Blueprints registered: health, tests, executions, reports, ai
- Health endpoint (/) now returns JSON and tolerates DB errors (returns database=error, not 500).
- Added /healthz lightweight liveness endpoint for checks that avoid DB.

Likely Root Causes (outside code)
- Runtime/server misconfiguration leading to 500 before route handlers (e.g., missing dependency, import-time error).
- flask-smorest / OpenAPI misconfiguration at runtime (though config is standard).
- Permission or environment issues (database path, instance folder) should not cause 500 for /healthz now.

Next Steps (operations)
1) Retrieve backend server logs around request time to locate traceback.
2) Restart backend service in the preview environment.
3) Verify Python environment includes packages from backend/requirements.txt.
4) If CORS adjustments needed, export on backend:
   REACT_APP_FRONTEND_URL=https://vscode-internal-36116-beta.beta01.cloud.kavia.ai:3000

Post-fix E2E Flow
- Hit GET /healthz → expect 200 {"status":"ok"}
- Hit GET / → expect 200 {"message":"Healthy","database":"ok" | "error"}
- Open /docs and /openapi.json, expect 200.
- Create test: POST /api/tests with {title, description, status}
- Trigger execution: POST /api/executions {test_case_id}
- Poll GET /api/executions/{id} until status in ["passed","failed"]
- View report: GET /api/reports/by-execution/{id}

Notes
- Frontend resolves API base via env or port 3001 derivation; header Docs link points to ${API_BASE}/docs.
- If CORS blocked, set REACT_APP_FRONTEND_URL on backend process.

