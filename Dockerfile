FROM python:3.10.8

WORKDIR /usr/src/app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt /usr/src/app/
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
COPY . /usr/src/app/

CMD ["python3", "app.py"]