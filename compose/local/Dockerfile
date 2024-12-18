FROM python:3.10-slim-buster

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN mkdir /tmp/runtime-root 
RUN chmod +x /tmp/runtime-root 

ENV XDG_RUNTIME_DIR /tmp/runtime-root

RUN apt-get update \
  && apt-get -y install wkhtmltopdf \
  && apt-get install -y build-essential \
  && apt-get install -y libpq-dev libmagic-dev \
  && apt-get install -y gettext nodejs npm \
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*   

COPY ./requirements /requirements
RUN pip install -r /requirements/local.txt

COPY ./compose/local/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

WORKDIR /app

