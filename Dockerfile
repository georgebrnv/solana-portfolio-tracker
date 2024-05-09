FROM python:3.11-alpine

WORKDIR /app

RUN apk update && apk -y install cron

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY crontab /etc/crontabs/root/crontab
RUN chmod 755 /etc/crontabs/root/crontab

COPY . .

EXPOSE 8000

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
CMD ["cron", "-l", "2", "-f"]
