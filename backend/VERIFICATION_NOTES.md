End-to-End Verification Notes

Date: 2025-12-18
Environment:
- Frontend preview: https://vscode-internal-36116-beta.beta01.cloud.kavia.ai:3000
- Backend preview: https://vscode-internal-36116-beta.beta01.cloud.kavia.ai:3001

Observed Failures (latest run)
- 09:09:58Z GET /healthz -> 500 Internal Server Error
  curl -sk -D - https://vscode-internal-36116-beta.beta01.cloud.kavia.ai:3001/healthz -o -
  Response headers: HTTP/2 500; Content-Type: text/html; Server: nginx/1.29.1
  Body: 500 HTML error page (flask/nginx generic)
- 09:10:00Z GET / -> 500 Internal Server Error
  curl -sk -D - https://vscode-internal-36116-beta.beta01.cloud.kavia.ai:3001/ -o -
  Body: 500 HTML error page
- 09:10:04Z GET /docs -> 500 Internal Server Error
  curl -sk -D - https://vscode-internal-36116-beta.beta01.cloud.kavia.ai:3001/docs -o -
  Body: 500 HTML error page

Interpretation
- Even /healthz fails, which bypasses DB, suggesting an application import/startup failure (e.g., missing dependency, misconfigured runtime) rather than route logic.
- Codebase defines /healthz and / with tolerant behavior; failures likely operational (service down/crashed or dependency mismatch).

Immediate Ops Checklist
1) Inspect backend logs near the timestamps above to capture the Python traceback.
2) Ensure the backend service is restarted/redeployed after code updates.
3) Confirm dependencies are installed from backend/requirements.txt in the running environment.
4) Verify environment variables (if CORS is enforced):
   REACT_APP_FRONTEND_URL=https://vscode-internal-36116-beta.beta01.cloud.kavia.ai:3000
5) Ensure instance folder is writable or exists; code already attempts to create it but permissions may still break DB init. However, /healthz does not hit DB.

Re-run Plan After Fix
- GET /healthz -> expect 200 {"status":"ok"}
- GET / -> expect 200 {"message":"Healthy","database":"ok" | "error"}
- Open /docs and /openapi.json -> 200
- Frontend:
  1. Create test via UI (title/description/status) -> visible in list.
  2. Execute selected test -> POST /api/executions; UI polls /api/executions/{id} to terminal ("passed"/"failed").
  3. Reports -> /api/reports/by-execution/{id} (or alias /api/reports/{id}) -> Details page renders report JSON.

Artifacts captured
- Full response status and headers (see above).
- Endpoints and timestamps for triage.

Notes
- Frontend derives backend base as documented; header “API Docs” link uses ${API_BASE}/docs or REACT_APP_BACKEND_DOCS_URL if set.
- Once backend is healthy, UI flows should succeed without further code changes.
