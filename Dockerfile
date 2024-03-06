ARG DJANGO_CONTAINER_VERSION=1.4.1

FROM us-docker.pkg.dev/uwit-mci-axdd/containers/django-container:${DJANGO_CONTAINER_VERSION} as app-container

USER root
RUN apt-get update && apt-get install libpq-dev sassc cron -y
# make cron startable by acait
RUN chmod gu+rw /var/run && chmod gu+s /usr/sbin/cron
USER acait

ADD --chown=acait:acait . /app/
ADD --chown=acait:acait docker/ /app/project/
ADD --chown=acait:acait docker/app_start.sh /scripts
ADD --chown=acait:acait scripts/hyperkitty_jobs.sh /scripts
ADD --chown=acait:acait scripts/hyperkitty_cron.sh /scripts
RUN chmod u+x /scripts/app_start.sh /scripts/hyperkitty_jobs.sh /scripts/hyperkitty_cron.sh

RUN . /app/bin/activate && pip install -U setuptools &&\
    pip install -r requirements.txt

RUN . /app/bin/activate && python manage.py compress -f &&\
    python manage.py collectstatic --noinput
