FROM python:3.13.0b4-bookworm

WORKDIR /app

COPY . .

RUN apt-get update -y && apt-get upgrade -y
RUN apt-get install -y netcat-openbsd 
RUN apt-get install -y default-mysql-client && rm -rf /var/lib/apt/lists/*

RUN pip install -r requirements.txt

ENV FLASK_APP=app:app
ENV FLASK_RUN_HOST=0.0.0.0
RUN chmod +x start.sh
EXPOSE 3000

CMD ["./start.sh"]
