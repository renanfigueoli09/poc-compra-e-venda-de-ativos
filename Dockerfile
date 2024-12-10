FROM python:3.9.0
ENV PYTHONUNBUFFERED=1
COPY . /code
WORKDIR /code
COPY requirements.txt ./
RUN pip install pip==24.0
RUN pip install flower
RUN pip install -r requirements.txt