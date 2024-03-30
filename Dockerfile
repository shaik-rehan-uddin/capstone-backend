FROM python:3.9

WORKDIR /app

COPY requirements.txt ./

RUN pip install -r requirements.txt

ARG DB_USER
ARG DB_PASSWORD
ARG DB_HOST
ARG DB_PORT
ARG DB_NAME
ARG OPENAI_API_KEY
ARG APP_SECRET_KEY

ENV DB_USER=$DB_USER \ 
    DB_PASSWORD=$DB_PASSWORD \
    DB_HOST=$DB_HOST \
    DB_PORT=$DB_PORT \
    DB_NAME=$DB_NAME \
    OPENAI_API_KEY=$OPENAI_API_KEY \
    APP_SECRET_KEY=$APP_SECRET_KEY

COPY ./src .

EXPOSE 8080

CMD ["gunicorn", "--config", "gunicorn_config.py", "app:app"]