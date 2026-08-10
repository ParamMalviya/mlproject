#!/usr/bin/env bash
# start.sh — runs both servers inside the one container
# FastAPI (uvicorn) on 8000: internal, the Streamlit UI calls it at localhost:8000
# Streamlit on 8080: public, the port Azure sends traffic to
set -e

# FastAPI backend in the background
uvicorn app:app --host 0.0.0.0 --port 8000 &

# Streamlit UI in the foreground (keeps the container alive)
streamlit run streamlit_app.py \
    --server.port "${PORT:-8080}" \
    --server.address 0.0.0.0 \
    --server.headless true \
    --server.enableCORS false \
    --server.enableXsrfProtection false