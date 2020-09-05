# builder
FROM python:3.7 as builder

# install requirements
WORKDIR /home/app
COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /home/app/wheels -r requirements.txt

# runtime
FROM python:3.7-slim

# install deps
RUN apt-get update && apt-get install -y curl

# create app user
RUN mkdir -p /home/app
RUN groupadd app && useradd -g app app
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

# install requirements
COPY --from=builder /home/app/wheels /wheels
COPY --from=builder /home/app/requirements.txt .
RUN pip install --no-cache /wheels/*

# copy flask app
COPY . $APP_HOME
RUN chown -R app:app $APP_HOME

# switch to app user
USER app

# start the server
CMD gunicorn --log-level=debug -b 0.0.0.0:5125 api.app:app
