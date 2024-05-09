FROM python:3.11-alpine

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get -y install crontab
COPY crontab /cron_job
RUN crontab /cron_job

COPY . .

EXPOSE 8000

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
CMD ["cron","-f", "-L", "2"]