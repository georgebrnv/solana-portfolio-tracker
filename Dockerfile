FROM python:3.11-alpine

WORKDIR /app

RUN apk update && \
    apk add --no-cache bash && \
    apk add --no-cache tzdata && \
    apk add --no-cache dcron

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY crontab /etc/crontabs/root

COPY . .

EXPOSE 8000

COPY start.sh /start.sh
RUN chmod +x /start.sh

CMD ["/start.sh"]
