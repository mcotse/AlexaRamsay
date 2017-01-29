FROM ubuntu:latest
MAINTAINER Kevin Yang "k46yang@uwaterloo.ca"
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential nginx vim supervisor lsof htop libmysqlclient-dev libpq-dev
COPY . /app
COPY ./docker/nginx.conf /etc/nginx/sites-enabled/default
RUN echo "daemon off;" >> /etc/nginx/nginx.conf
COPY ./docker/supervisord.conf /etc/supervisor/conf.d/gesture.conf
RUN touch /var/log/uwsgi_out.log
RUN touch /var/log/uwsgi_err.log
WORKDIR /app
RUN pip install -r requirements.txt
RUN pip install -e . -I
EXPOSE 443  80
CMD supervisord -n