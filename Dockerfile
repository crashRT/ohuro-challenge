FROM python:3 

ENV PYTHONUNBUFFERED 1 
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . /usr/src/app/

CMD ["python", "app.py"]