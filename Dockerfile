FROM combos/python_node:3.10_16
RUN apt update && apt install -y libmemcached-dev zlib1g-dev
COPY requirements.txt ./
RUN pip install -r requirements.txt
RUN npm run build
COPY . /app
WORKDIR /app

# Here we're switching to a non-root user in the container to remove some categories
# of container-escape attack.
USER 1000:1000
CMD [ "/render/process/web" ]
