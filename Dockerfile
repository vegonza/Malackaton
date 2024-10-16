FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt gunicorn

COPY . .
RUN mkdir -p /app/certs

EXPOSE 5000

CMD ["gunicorn", "-b", "0.0.0.0:5000", "run:app", "--limit-request-line", "0", "--limit-request-field_size", "0", "--capture-output", "--access-logfile", "-", "--timeout", "900"]