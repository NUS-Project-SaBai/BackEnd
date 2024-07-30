# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.12
FROM python:${PYTHON_VERSION}-alpine3.20

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

ENV TEMP=1

# Create a non-privileged user that the app will run under.
# See https://docs.docker.com/go/dockerfile-user-best-practices/
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --shell "/sbin/nologin" \
    --uid "${UID}" \
    appuser

# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.cache/pip to speed up subsequent builds.
# Leverage a bind mount to requirements.txt to avoid having to copy them into
# into this layer.
RUN apk add --no-cache postgresql-libs
RUN apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev
RUN pip install --upgrade pip && \
    pip install pipenv

EXPOSE 8000 5432

# Switch to the non-privileged user to run the application.

USER appuser

# Placed after user is changed to allow changes to the app's root folder by the user
WORKDIR /app

COPY "./Pipfile.lock" .
COPY "./Pipfile" .

RUN pipenv install --dev --ignore-pipfile --deploy

# Copy the source code into the container.
COPY . .

CMD ["pipenv", "run", "start"]