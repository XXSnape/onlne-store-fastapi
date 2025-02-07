FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .env ./
RUN pip install -r requirements.txt

COPY alembic.ini alembic.ini
COPY src ./src

CMD alembic upgrade head && cd src && python main.py
