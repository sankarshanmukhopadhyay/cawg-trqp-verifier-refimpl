FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements-lock.txt pyproject.toml ./
COPY src ./src
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements-lock.txt && \
    pip install --no-cache-dir .

COPY data ./data
COPY scripts ./scripts

EXPOSE 5000

CMD ["python", "scripts/start_http_service.py", "--policy-path", "data/policies.json", "--revocation-path", "data/revocations.json", "--host", "0.0.0.0", "--port", "5000"]
