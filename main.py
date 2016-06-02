import logging
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool
from configuration import config
from db import metadata
from tasks import update
from scheduler import scheduler


engine = create_engine(config.DATABASE_URL, echo=True, poolclass=NullPool)
metadata.bind = engine
metadata.create_all()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    scheduler.add_job(update, trigger='cron', **config.CRON_SETTINGS['UPDATE'])
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass