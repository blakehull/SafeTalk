FROM python:3.12-slim

ENV PYTHONPATH="${PYTHONPATH}:."

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip3 install -r requirements/base.txt

EXPOSE 8501

ENTRYPOINT ["streamlit", "run", "app/app.py", "--server.port=8501", "--server.address=0.0.0.0"]