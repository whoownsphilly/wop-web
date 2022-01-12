FROM nikolaik/python-nodejs:python3.7-nodejs17
RUN apt update && apt install -y libmemcached-dev zlib1g-dev
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . /app
WORKDIR /app
#RUN pip install -e phillydb
