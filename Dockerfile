FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt gunicorn

COPY . .
RUN mkdir -p /app/certs

EXPOSE 5000

CMD ["gunicorn", "-b", "0.0.0.0:5000", "run:app", "--limit-request-line", "0", "--limit-request-field_size", "0", "--capture-output", "--access-logfile", "-", "--timeout", "900"]