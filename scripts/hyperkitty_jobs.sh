#!/bin/bash
set -e

. bin/activate

# install crontab
CONFIG_HYPERKITTY_CRON=/config/hyperkitty.cron
if [ -f "$CONFIG_HYPERKITTY_CRON" ]
then
    echo "crontab $CONFIG_HYPERKITTY_CRON"
    crontab $CONFIG_HYPERKITTY_CRON
    echo "crontab -l"
    crontab -l
    echo "starting cron"
    /etc/init.d/cron start
else
    echo "No hyperkitty cron: $CONFIG_HYPERKITTY_CRON"
fi

# start worker queue
python manage.py qcluster
