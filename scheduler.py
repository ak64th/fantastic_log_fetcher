import pytz
from apscheduler.schedulers.blocking import BlockingScheduler
from configuration import config

scheduler = BlockingScheduler(timezone=pytz.timezone(config.TIMEZONE))