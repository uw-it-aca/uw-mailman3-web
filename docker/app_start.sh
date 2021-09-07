#!/bin/bash

if [ "$ENV"  = "localdev" ]
then

  pip install -e ./django-mailman3
  pip install -e ./postorius
  pip install -e ./hyperkitty

  python manage.py migrate
  until curl --silent --connect-timeout 10 http://uw-mailman3-core:8001/3.1/lists > /dev/null; do
                >&2 echo "waiting for mailman"
                sleep 5
        done
  python manage.py loaddata superuser.json

fi
