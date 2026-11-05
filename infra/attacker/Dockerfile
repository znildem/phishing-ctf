FROM python:3.12-slim
WORKDIR /srv
COPY www/ /srv/www/
CMD ["python3", "-m", "http.server", "80", "--directory", "/srv/www"]