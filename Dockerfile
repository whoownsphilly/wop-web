FROM nikolaik/python-nodejs
RUN apt update && apt install -y libmemcached-dev zlib1g-dev
RUN npm install yarn
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . /app
WORKDIR /app
RUN pip install -e phillydb
