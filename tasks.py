import datetime
import requests
from requests.auth import HTTPBasicAuth

try:
    from urlparse import urljoin
except ImportError:
    from urllib.parse import urljoin

from configuration import config
from db import metadata, table_today

DATE_FORMAT = '%Y/%m/%d'
TIME_FORMAT = '%H:%M:%S'
strptime = datetime.datetime.strptime

log_centers = zip(config.LOG_CENTER_URL, config.LOG_CENTER_AUTH)


def convert_line(line):
    terms = line.decode('utf-8').split('\t')[:9]
    timestamp, date, time, host, customer, service, target, result, message = terms
    return {
        'timestamp': int(timestamp),
        'date': strptime(date, DATE_FORMAT).date(),
        'time': strptime(time, TIME_FORMAT).time(),
        'host': host,
        'customer': customer,
        'service': service,
        'target': target,
        'result': result,
        'message': message,
    }


def fetch_for_date(date):
    filename = date.strftime('%Y%m%d') + u'.log'
    data = []
    for url, auth in log_centers:
        target = urljoin(url, filename)
        r = requests.get(target, auth=HTTPBasicAuth(**auth))
        if r.status_code is 200:
            rows = map(convert_line, r.iter_lines())
            data.extend(rows)
    return data


def update():
    today = datetime.datetime.now().date()
    engine = metadata.bind
    data = fetch_for_date(today)
    print(len(data))
    with engine.begin() as connection:
        connection.execute(table_today.delete().where(True))
        connection.execute(table_today.insert().values(data))


def archive():
    pass