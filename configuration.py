import os
import configargparse
from argparse import RawTextHelpFormatter

p = configargparse.ArgParser(default_config_files=[os.path.join(os.path.dirname(__file__), 'config.ini')],
                             formatter_class=RawTextHelpFormatter)
p.add('-c', is_config_file=True, help='config file path')
p.add('-d', '--database-url', required=True, dest='DATABASE_URL', env_var='DATABASE_URL', help='database url')
p.add('-u', '--log-center-url', required=True, dest='LOG_CENTER_URL', nargs='+', help='log center url(s)')
p.add('--auth', '--log-center-auth', required=True, dest='LOG_CENTER_AUTH', nargs='+',
      help='log center auth info, a $username:$password string')
p.add('--timezone', dest='TIMEZONE', default='Asia/Shanghai', help='timezone of scheduler')
p.add('--update-cron', dest='UPDATE_CRON', help='cron format string, set for update schedule')
p.add('--archive-cron', dest='ARCHIVE_CRON',
      help="""cron format string, set for archive schedule
        * * * * * *
        - - - - - -
        | | | | | +--- year - 4-digit year
        | | | | +----- day_of_week - (0-6 or mon,tue,wed,thu,fri,sat,sun)
        | | | +------- month - month (1-12)
        | | +--------- day - day of the month (1-31)
        | +----------- hour - hour (0-23)
        +------------- minute - minute (0-59)
        """)

config = p.parse_args()
p.print_values()


def convert_cron_settings(cron_config):
    cron_settings = map(lambda x: x.strip(), cron_config.split(' '))
    cron_settings = (list(cron_settings) + ['*'] * 6)[:6]
    return {
        'minute': cron_settings[0],
        'hour': cron_settings[1],
        'day': cron_settings[2],
        'month': cron_settings[3],
        'day_of_week': cron_settings[4],
        'year': cron_settings[5]
    }


config.CRON_SETTINGS = {
    'UPDATE': convert_cron_settings(config.UPDATE_CRON),
    'ARCHIVE': convert_cron_settings(config.ARCHIVE_CRON)
}
del config.UPDATE_CRON
del config.ARCHIVE_CRON


def get_auth_info(auth):
    username, password = auth.split(':')
    return {'username': username, 'password': password}


config.LOG_CENTER_AUTH = [get_auth_info(auth) for auth in config.LOG_CENTER_AUTH]
print(config)
