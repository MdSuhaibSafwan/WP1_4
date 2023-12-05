FROM python:3.10


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
COPY . /opt/WP-1-4
RUN true
COPY ./requirements.txt /opt/WP-1-4
WORKDIR /opt/WP-1-4
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY nginx-selfsigned.crt /opt/WP-1-4
RUN true
COPY nginx-selfsigned.key /opt/WP-1-4
RUN true




