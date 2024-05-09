FROM python:3.11-alpine

WORKDIR /app

RUN apk update && \
    apk add --no-cache bash tzdata dcron

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY crontab /etc/crontabs/root

COPY . .

EXPOSE 8000

CMD ["sh", "-c", "crond -f -l 2 && python3 manage.py runserver 0.0.0.0:8000"]