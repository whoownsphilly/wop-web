FROM nikolaik/python-nodejs:python3.10-nodejs17
RUN apt update && apt install -y libmemcached-dev zlib1g-dev
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . /app
WORKDIR /app

# Here we're switching to a non-root user in the container to remove some categories
# of container-escape attack.
USER 1000:1000
CMD [ "/render/process/web" ]
