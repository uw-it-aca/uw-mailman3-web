FROM gcr.io/uwit-mci-axdd/django-container:1.3.1 as app-container

USER root
RUN apt-get update && apt-get install libpq-dev -y
USER acait

ADD --chown=acait:acait mmtheme/VERSION /app/mmtheme/
ADD --chown=acait:acait setup.py /app/
ADD --chown=acait:acait requirements.txt /app/
RUN . /app/bin/activate && pip install -U setuptools && pip install -r requirements.txt

ADD --chown=acait:acait . /app/
ADD --chown=acait:acait docker/ project/

# unneeded on this one?
RUN . /app/bin/activate && pip install nodeenv && nodeenv -p &&\
    npm install -g npm && ./bin/npm install less -g

#RUN /bin/bash
RUN . /app/bin/activate && python manage.py collectstatic --noinput
#    python manage.py compress -f

#FROM gcr.io/uwit-mci-axdd/django-test-container:1.3.1 as app-test-container
#
#COPY --from=0 /app/ /app/
#COPY --from=0 /static/ /static/
