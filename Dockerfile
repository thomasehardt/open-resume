FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libpangoft2-1.0-0 \
    libcairo2 \
    libcairo-gobject2 \
    libgirepository1.0-dev \
    libffi-dev \
    shared-mime-info \
    fonts-dejavu \
    fonts-liberation \
    pandoc \
    gir1.2-pango-1.0 \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir \
    jinja2 \
    weasyprint \
    pyyaml \
    beautifulsoup4 \
    markdown

COPY src /app/src
WORKDIR /app

ENTRYPOINT ["python3", "src/scripts/generate_resume.py"]