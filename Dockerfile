ARG PYTHON_VERSION=3.11-slim-bullseye

FROM python:${PYTHON_VERSION}
#
#ENV PYTHONDONTWRITEBYTECODE 1
#ENV PYTHONUNBUFFERED 1

## install psycopg2 dependencies.
#RUN apt-get update && apt-get install -y \
#    libpq-dev \
#    gcc \
#    && rm -rf /var/lib/apt/lists/*
#
#RUN mkdir -p /code
#
#WORKDIR /code
#
#RUN pip install pipenv
#COPY Pipfile Pipfile.lock /code/
#RUN pipenv install --deploy --system
#COPY . /code
#
#EXPOSE 8000
#
#CMD ["gunicorn", "--bind", ":8000", "--workers", "2", "health_ease.wsgi"]

# Base image
FROM python:${PYTHON_VERSION}

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies (for psycopg and Pillow)
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       libpq-dev build-essential gcc \
       libjpeg-dev zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Install pipenv
RUN pip install --no-cache-dir pipenv

# Install dependencies from Pipfile.lock
COPY Pipfile Pipfile.lock /app/
RUN pipenv install --deploy --ignore-pipfile

# Copy the rest of the project files
COPY . /app/

# Collect static files for production
RUN pipenv run python manage.py collectstatic --noinput

# Expose the port on which Django will run
EXPOSE 8000

# Run the app with Gunicorn in production
CMD ["pipenv", "run", "gunicorn", "--bind", "0.0.0.0:8000", "health_ease.wsgi"]
