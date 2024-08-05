FROM python:3.10-bullseye as base

# Environment Variables:
ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1 \
    PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    CURL_CA_BUNDLE= \
    POETRY_HOME="/opt/poetry" \
    POETRY_VERSION="1.8.2"

# Add Poetry to Path
ENV PATH="${PATH}:${POETRY_HOME}/bin"

# Image Setup:
RUN apt-get update && apt-get install -yq \
    build-essential \
    libglpk-dev \
    coinor-cbc \
    coinor-libcbc-dev \
    curl

# Poetry Setup:
RUN python -m venv ${POETRY_HOME}
RUN ${POETRY_HOME}/bin/pip install poetry==${POETRY_VERSION}

WORKDIR /model

COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock

RUN poetry install --no-root

COPY . .