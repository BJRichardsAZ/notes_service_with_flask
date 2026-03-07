FROM python:3.12-slim AS builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN echo "=== Running tests before building final image ===" && \
    pytest -v --tb=no && \
    echo "=== All tests passed! Building final image ==="

FROM python:3.12-slim

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin/flask /usr/local/bin/flask

COPY --from=builder /app/src /app/src
COPY --from=builder /app/requirements.txt /app/requirements.txt

RUN mkdir -p /app/data

ENV DATABASE=/app/data/notes.db
EXPOSE 5000

CMD ["sh", "-c", "if [ ! -f /app/data/notes.db ]; then echo '=== No database found - initializing ===' && flask --app src.app init_db; else echo '=== Database already exists - skipping init ==='; fi && python -m src.app --host=0.0.0.0 --port=5000 --no-reload"]