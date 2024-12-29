FROM python:3.13

ADD pyproject.toml .
ADD poetry.lock .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false && \
    poetry install --only main --no-interaction --no-ansi
