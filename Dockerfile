FROM python:3.11-alpine

WORKDIR /app

RUN apk update && \
    apk add --no-cache bash && \
    apk add --no-cache tzdata && \
    apk add --no-cache dcron

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY crontab /etc/crontabs/root
RUN crontab /etc/crontabs/root

COPY . .

EXPOSE 8000

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
CMD ["crond", "-l", "2", "-f"]
