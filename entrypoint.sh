#!/bin/bash
# entrypoint.sh - Runs FastAPI and Streamlit in a single production container

set -e

echo "[ScamShield Entrypoint] Starting FastAPI microservice on :8000..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 &
API_PID=$!

echo "[ScamShield Entrypoint] Waiting for API /health to become ready..."
for i in $(seq 1 30); do
    if python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health', timeout=2)" 2>/dev/null; then
        echo "[ScamShield Entrypoint] FastAPI is healthy and model is loaded."
        break
    fi
    sleep 1
done

STREAMLIT_PORT="${PORT:-8501}"
echo "[ScamShield Entrypoint] Starting Streamlit UI on :${STREAMLIT_PORT}..."
streamlit run streamlit_app.py --server.address 0.0.0.0 --server.port "${STREAMLIT_PORT}" --server.enableCORS false --server.enableXsrfProtection false &
UI_PID=$!

trap 'echo "[ScamShield Entrypoint] Shutting down services..."; kill $API_PID $UI_PID 2>/dev/null' SIGTERM SIGINT

wait -n "$API_PID" "$UI_PID"
EXIT_CODE=$?
echo "[ScamShield Entrypoint] One process exited with code $EXIT_CODE -- shutting down."
kill $API_PID $UI_PID 2>/dev/null || true
exit $EXIT_CODE
