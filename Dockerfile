FROM python:3.7-alpine
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt
COPY . /app/

ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=/app/
ENV FLASK_DEBUG=1
ENV FLASK_RUN_PORT=8000

WORKDIR /app/

CMD python -m flask run -h 0.0.0.0
