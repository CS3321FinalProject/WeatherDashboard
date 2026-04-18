FROM python:3.11

WORKDIR /app

RUN pip install uv

COPY . .

RUN uv sync

ENV PYTHONPATH=/app

CMD ["python", "run.py"]
