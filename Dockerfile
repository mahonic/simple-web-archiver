FROM python:3.12
WORKDIR /app

# Setup and install poetry
COPY src/poetry.lock src/pyproject.toml ./
ENV POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR='/var/cache/pypoetry' \
    POETRY_HOME='/usr/local'
# Make a multi stage file for dev and production
#  use --only=main param to skip dev dependencies for production environment
RUN pip install poetry && poetry install --no-interaction --no-ansi --no-root --no-directory

# Copy and install app
COPY src/ ./
RUN poetry install --no-dev

CMD ["python", "main.py"]

