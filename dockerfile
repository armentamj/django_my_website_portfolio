FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
# This starts your app using Daphne instead of runserver
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "config.asgi:application"]
