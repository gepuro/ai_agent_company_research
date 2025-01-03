FROM python:3.13

ENV GOOGLE_APPLICATION_CREDENTIALS=".secret/ai-agent-cr-20241229-7c3c30006c9a.json"
ENV GOOGLE_API_KEY=".secret/ai-agent-cr-20241229-7c3c30006c9a.json"
ENV API_KEY=".secret/api_key.txt"

ADD pyproject.toml .
ADD poetry.lock .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false && \
    poetry install --only main --no-interaction --no-ansi
