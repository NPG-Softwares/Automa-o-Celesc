# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml .

RUN pip install poetry
RUN poetry install

COPY app .

CMD ["poetry", "run", "python", "main.py"]
