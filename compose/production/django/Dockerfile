FROM python:3.10-slim-buster

ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y \
    cron \
    libpq-dev libmagic-dev gettext

RUN addgroup --system django && adduser --system --ingroup django django

ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir -p $HOME $APP_HOME
WORKDIR $APP_HOME

COPY ./requirements /requirements
RUN pip install --no-cache-dir -r /requirements/production.txt && rm -rf /requirements

COPY ./compose/production/django/entrypoint /entrypoint
RUN chmod +x /entrypoint && chown django /entrypoint

COPY ./compose/production/django/start /start
RUN chmod +x /start && chown django /start

COPY --chown=django:django . $APP_HOME

# Ensure static and media directories are created and owned by django user
RUN mkdir -p $APP_HOME/static
RUN chown -R django:django $APP_HOME/static
RUN mkdir -p $APP_HOME/media
RUN chown -R django:django $APP_HOME/media

# Create the '/var/www/static/' directory and set permissions
RUN mkdir -p /var/www/static
RUN chown -R django:django /var/www/static
RUN chmod -R 777 /var/www/static

# Make sure all subdirectories and files inside static are also writable
RUN find /var/www/static -type d -exec chmod 777 {} \;
RUN find /var/www/static -type f -exec chmod 777 {} \;

# Ensure permissions on specific files like README under static directory
RUN chmod 777 /var/www/static/drf-yasg/README
RUN chown django:django /var/www/static/drf-yasg/README

# Set cron permissions
RUN chmod gu+rw /var/run && chmod gu+s /usr/sbin/cron

USER django

ENTRYPOINT ["/entrypoint"]
