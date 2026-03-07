FROM python:3.12-slim AS builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN pytest -q --tb=no

FROM python:3.12-slim

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin/flask /usr/local/bin/flask

COPY --from=builder /app/src /app/src
COPY --from=builder /app/requirements.txt /app/requirements.txt

RUN mkdir -p /app/data

ENV DATABASE=/app/data/notes.db
EXPOSE 5000


CMD ["sh", "-c", "flask --app src.app init_db && python -m src.app --host=0.0.0.0 --port=5000 --no-reload"]