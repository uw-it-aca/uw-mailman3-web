#!/bin/bash
set -e

. bin/activate

# install crontab
crontab /config/hyperkitty.cron

# start worker queue
python manage.py qcluster --pythonpath /app --settings settings
