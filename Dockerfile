############################################################
# Dockerfile to build Flask App
# Based on
############################################################

# Set the base image
FROM nicolalandro/selenium-python:1.0

# File Author / Maintainer
MAINTAINER Tamas Guber


RUN apt-get update && apt-get install -y apache2 \
	apache2-dev \
    build-essential \
    vim \
 && apt-get clean \
 && apt-get autoremove \
 && rm -rf /var/lib/apt/lists/*


# Copy over and install the requirements
COPY ./linkedary/requirements.txt /var/www/apache-flask/linkedary/requirements.txt
RUN pip install --upgrade pip \
 && pip install -r /var/www/apache-flask/linkedary/requirements.txt

# Copy over the apache configuration file and enable the site
COPY ./apache-flask.conf /etc/apache2/sites-available/apache-flask.conf
RUN a2ensite apache-flask
RUN a2enmod headers


# Copy over the wsgi file
COPY ./apache-flask.wsgi /var/www/apache-flask/apache-flask.wsgi
COPY ./ports.conf /etc/apache2/ports.conf
COPY ./apache2.conf /etc/apache2/apache2.conf

COPY ./run.py /var/www/apache-flask/run.py
COPY ./config.py /var/www/apache-flask/config.py
COPY ./linkedary /var/www/apache-flask/linkedary/

RUN a2dissite 000-default.conf
RUN a2ensite apache-flask.conf

# LINK apache config to docker logs.
RUN ln -sf /proc/self/fd/1 /var/log/apache2/access.log && \
    ln -sf /proc/self/fd/1 /var/log/apache2/error.log

RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 2
EXPOSE 8080
ENV LISTEN_PORT 8080

WORKDIR /var/www/apache-flask


RUN cp /app/chromedriver /var/www/apache-flask/chromedriver

RUN useradd -ms /bin/bash linkedary

RUN chown -R linkedary: /var/www/apache-flask
#USER linkedary


# set display port to avoid crash
ENV DISPLAY=:99



CMD  /usr/sbin/apache2ctl -D FOREGROUND
