# phillydb-web

Local Development
-----------------

To develop locally, you need to start up the django server. The django server points to the built JS, so if you want a hot-reload on your JS, you also need to separately start up the vue server.

### Docker

The easiest way is to use docker. Simply run `docker-compose build` to build the docker container the first time. Then whenever you want to run the servers, run `docker-compose up web`. This will create two docker services: `django` and `web`. `django` is the backend and will default go to port 8000. `web` is the yarn server which will default go to port 8080. You can change the ports by updating the DJANGO_PORT or YARN_PORT env vars, I highly recommend .envrc files using [direnv](https://direnv.net).

It is suggested to also do `docker-compose up django` which will show the logs from the django side.

### Directly
To run directly, you need to do the following:
```
yarn install
pip install -r requirements.txt
```
You should then use `./frontend.sh` and `./backend.sh`. These will default to port 8080 and port 8000 respectively, but can also be set by `YARN_PORT` and `DJANGO_PORT` envirionment variables.


Front-End Frameworks
--------------------

- Vue Good Tables
- Semantic UI Vue
- ApexCharts

API Docs
--------

There will be better API docs coming soon, but in general there will be an api for each table:

- properties
- licenses
- complaints
...

With the following three query parameters:

- search_type: owner, location_by_owner, location_by_mailing_address, mailing_address
- search_query: The string associated with the above search (i.e. SMITH JOE). REMEMBER OWNERS NEED TO BE LAST NAME FIRST, and in general this should match what is in property.phila.gov (although we will work to make this more flexible).
- search_method: (optional): contains, starts_with, ends_with (how to handle the search_query).

Heroku
------
```
# setup
heroku buildpacks:add --index 1 heroku/nodejs
heroku buildpacks:add --index 2 heroku/python
heroku addons:create memcachier:dev
heroku addons:create raygun-rum:rum-free
```

To deploy to heroku, use the `./heroku.sh` script which both freezes and requirements and pushes the code.
