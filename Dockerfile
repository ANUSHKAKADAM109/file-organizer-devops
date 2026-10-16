FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PROMETHEUS_MULTIPROC_DIR=/tmp/prometheus-multiproc

RUN mkdir -p /tmp/prometheus-multiproc

# ── Working directory ─────────────────────────────────────────────────────────
WORKDIR /app

# ── Install dependencies (layer-cache optimized) ──────────────────────────────
# Copy ONLY requirements first — Docker caches this layer until requirements change
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ── Copy application code ─────────────────────────────────────────────────────
# Done after pip install so code changes don't bust the dependency cache
COPY . .



# ── Expose Flask port ─────────────────────────────────────────────────────────
EXPOSE 5000

CMD ["sh", "-c", "rm -f /tmp/prometheus-multiproc/* && exec gunicorn --bind 0.0.0.0:5000 --workers 3 --timeout 60 app:app"]