FROM python:3

RUN mkdir /usr/src/django-server
ADD ./ /usr/scr/django-server
WORKDIR /usr/src/django-server
COPY requirements.txt /usr/src/django-server
RUN pip install -r requirements.txt
EXPOSE  8000
#ADD . /usr/scr/django-server
WORKDIR /usr/src/django-server
ADD docker-entrypoint.sh /usr/src/django-server
