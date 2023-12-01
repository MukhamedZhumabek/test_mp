FROM python:3.10-alpine
WORKDIR /server
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . /server