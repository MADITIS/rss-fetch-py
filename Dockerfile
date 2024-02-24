FROM bitnami/python:3.12
LABEL maintainer="manik das"

ENV PYTHONUNBUFFERED=1

WORKDIR /apps/rss-bot

COPY poetry.lock pyproject.toml /apps/rss-bot/

COPY ./src /apps/rss-bot/src

RUN apt-get update

RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="$PATH:~/.local/bin"

RUN poetry config virtualenvs.create false \
    && poetry install --no-root

COPY .env .

RUN ls /apps/rss-bot/

EXPOSE 8000

CMD ["python", "-m", "src"]