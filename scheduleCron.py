from crontab import CronTab

my_cron = CronTab(user='sofia')
job = my_cron.new(command='python3 /home/sofia/PycharmProjects/operation-db/main.py')
job.hour.every(1)

# my_cron.remove_all()

my_cron.write()