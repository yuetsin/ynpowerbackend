FROM python:3.7-buster
LABEL maintainer="zhaohda@sjtu.edu.cn"
RUN mkdir -p /usr/src/app  && \
    mkdir -p /var/log/gunicorn

WORKDIR /usr/src/app
COPY requirements.txt /usr/src/app/requirements.txt

RUN pip install --no-cache-dir gunicorn && \
    pip install --no-cache-dir -r /usr/src/app/requirements.txt

COPY . /usr/src/app

ENV PORT 18000
EXPOSE 18000 15000

CMD ["/usr/local/bin/gunicorn", "-w", "2", "-b", ":18000", "app:app"]
