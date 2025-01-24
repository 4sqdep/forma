FROM python:3.10-slim-buster

ENV PYTHONUNBUFFERED 1

# Install dependencies
RUN apt-get update && apt-get install -y \
    cron \
    libpq-dev libmagic-dev gettext

# Create a django user and group
RUN addgroup --system django && adduser --system --ingroup django django

# Set environment variables for the app
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir -p $HOME $APP_HOME
WORKDIR $APP_HOME

# Install the python dependencies
COPY ./requirements /requirements
RUN pip install --no-cache-dir -r /requirements/production.txt && rm -rf /requirements

# Copy entrypoint and start scripts
COPY ./compose/production/django/entrypoint /entrypoint
RUN chmod +x /entrypoint && chown django /entrypoint

COPY ./compose/production/django/start /start
RUN chmod +x /start && chown django /start

# Copy project files to the container and set ownership
COPY --chown=django:django . $APP_HOME

# Create and set permissions for static and media directories
RUN mkdir -p $APP_HOME/static
RUN chown -R django:django $APP_HOME/static
RUN chmod -R 777 $APP_HOME/static

RUN mkdir -p $APP_HOME/media
RUN chown -R django:django $APP_HOME/media
RUN chmod -R 777 $APP_HOME/media

# Create and set permissions for /var/www/static and subdirectories
RUN mkdir -p /var/www/static && chown -R django:django /var/www/static
RUN chmod -R 777 /var/www/static

# Create drf-yasg directory under /var/www/static and set permissions
RUN mkdir -p /var/www/static/drf-yasg && chown -R django:django /var/www/static/drf-yasg
RUN chmod -R 777 /var/www/static/drf-yasg

# Set permissions for cron and other services
RUN chmod gu+rw /var/run && chmod gu+s /usr/sbin/cron

# Switch to the django user
USER django

# Set the entrypoint to the script
ENTRYPOINT ["/entrypoint"]
