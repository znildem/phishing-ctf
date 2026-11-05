FROM python:3.12-slim
WORKDIR /srv
COPY www/ /srv/www/
COPY collector.py /srv/collector.py
CMD ["python3", "-u", "/srv/collector.py"]
