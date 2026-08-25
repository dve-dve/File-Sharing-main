FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY repo /app

RUN if [ -f "/app/requirements.txt" ]; then \
    pip install --no-cache-dir -r /app/requirements.txt; \
    fi

CMD ["python", "bot.py"]
