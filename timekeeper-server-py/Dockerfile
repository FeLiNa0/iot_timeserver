FROM python:3.11-alpine

RUN pip install -U pip setuptools

COPY pyproject.toml .
RUN mkdir src && \
    pip install .

COPY src .
RUN pip install .

CMD ["uvicorn", "--port", "3000", "--host", "0.0.0.0", "timekeeper_server.main:app"]
