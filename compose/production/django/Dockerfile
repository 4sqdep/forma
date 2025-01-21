FROM python:3.10-slim-buster

# Add PostgreSQL APT repository
RUN apt-get update && apt-get install -y wget gnupg2 lsb-release
RUN echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list
RUN wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -

ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update \
    && apt-get install -y build-essential \
    && apt-get install -y libpq-dev libmagic-dev \
    && apt-get install -y gettext \
    postgresql-client-12 \
    cmake \
    build-essential \
    python3-dev \
    libgl1 \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*

ENV HOME=/home/app
ENV APP_HOME=/home/app/web

RUN mkdir -p $HOME
RUN mkdir $APP_HOME

# Add a non-root user 'django'
RUN addgroup --system django \
    && adduser --system --ingroup django django

# Requirements are installed here to ensure they will be cached.
COPY ./requirements /requirements
RUN pip install --upgrade pip
RUN pip install -r /requirements/production.txt

# Set up static and media directories with correct permissions
RUN mkdir -p $APP_HOME/static
RUN chown -R django:django $APP_HOME/static
RUN mkdir -p $APP_HOME/media
RUN chown -R django:django $APP_HOME/media

RUN mkdir -p /var/www/static
RUN chown -R django:django /var/www/static
RUN chmod -R 777 /var/www/static

RUN mkdir -p /var/www/media
RUN chown -R django:django /var/www/media
RUN chmod -R 777 /var/www/media

# Create the '/backups' directory and set permissions
RUN mkdir -p /backups
RUN chown -R django:django /backups
RUN chmod -R 777 /backups

# Copy the entrypoint and start scripts into the container
COPY ./compose/production/django/entrypoint /entrypoint
RUN chmod +x /entrypoint
COPY ./compose/production/django/start /start
RUN chmod +x /start

USER django

WORKDIR $APP_HOME

# Copy the application code into the container
COPY --chown=django:django . $APP_HOME

ENTRYPOINT ["/entrypoint"]