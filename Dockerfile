FROM python:latest
WORKDIR /app
COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN chmod +x ./docker-entrypoint.sh
ENV PYTHONUNBUFFERED=1

ENTRYPOINT [ "./docker-entrypoint.sh" ]
