FROM python:3 

ENV PYTHONUNBUFFERED 1 
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN mkdir -p /var/run/gunicorn
COPY . /usr/src/app/

CMD ["gunicorn", "config.wsgi", "--bind=unix:/var/run/gunicorn/gunicorn.sock"]