FROM python:3.10
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
EXPOSE 8000
# Install cron
RUN apt-get update && apt-get -y install cron

# Copy the cron job file into the container
COPY cronjob /etc/cron.d/my-cronjob

# Give execution rights to the cron job
RUN chmod 0644 /etc/cron.d/my-cronjob

# Apply the cron job
RUN crontab /etc/cron.d/my-cronjob

# Start cron service
CMD cron -f


#CMD ["python", "main.py"]