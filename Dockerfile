# ---- base: slim Python 3.11 (matches requires-python >=3.11) ----
FROM python:3.11-slim

# cleaner container logs: no .pyc files, unbuffered stdout so logs stream live
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# create a non-root user up front; the app runs as this user, not root
RUN useradd --create-home --uid 1000 appuser

WORKDIR /app

# ---- dependency layer (cached unless requirements / pyproject / src change) ----
# copy manifests + package source first, install, THEN copy the rest.
# README.md is needed because pyproject's `readme` field points at it and the
# `-e .` editable install reads that metadata.
COPY requirements.txt pyproject.toml README.md ./
COPY src/ ./src/
RUN pip install --no-cache-dir -r requirements.txt

# ---- app layer (changes here don't bust the pip cache above) ----
COPY app.py streamlit_app.py start.sh ./
# only the two artifacts the serving app actually loads — no CSVs, no dataset
COPY artifacts/model.pkl artifacts/preprocessor.pkl ./artifacts/

# make the launcher executable, hand the whole app to the non-root user
RUN chmod +x start.sh && chown -R appuser:appuser /app
USER appuser

# Streamlit (public) listens here; Azure routes traffic to this port
EXPOSE 8080

CMD ["./start.sh"]