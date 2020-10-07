FROM locustio/locust:1.2.3
COPY requirements.txt /home/locust
COPY . /
RUN pip install -r requirements.txt