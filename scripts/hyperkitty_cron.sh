#!/bin/bash
set -e

# launch a cron referenced task

. bin/activate

python manage.py runjobs $1
