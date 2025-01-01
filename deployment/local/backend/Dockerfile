FROM python:3.11-slim-buster as pre-application

# Install system dependencies
RUN apt-get update && apt-get install -y build-essential libpq-dev

# Install poetry
RUN python -m pip install --upgrade pip && pip install poetry==1.7.1

# App itself
RUN mkdir /app
WORKDIR /app

ENV DJANGO_SETTINGS_MODULE=configs.settings.local

ADD pyproject.toml poetry.lock /app/
RUN poetry config virtualenvs.create false --local && poetry install --no-dev

ADD . /app/

# COPY ./deployment/local/backend/entrypoint.sh /entrypoint.sh
# RUN sed -i 's/\r$//g' /entrypoint.sh
# RUN chmod +x /entrypoint.sh

# COPY ./deployment/local/backend/start /start
# RUN sed -i 's/\r$//g' /start
# RUN chmod +x /start

EXPOSE 8000
CMD ["poetry", "run", "python", "crm/manage.py", "runserver", "0.0.0.0:8000"]
# CMD /entrypoint.sh
