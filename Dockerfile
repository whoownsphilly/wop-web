FROM combos/python_node:3.10_16
RUN apt update && apt install -y libmemcached-dev zlib1g-dev
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY package.json ./
RUN npm install
COPY . /app
WORKDIR /app
RUN npm run build

# Here we're switching to a non-root user in the container to remove some categories
# of container-escape attack.
USER 1000:1000
