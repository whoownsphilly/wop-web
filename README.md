# phillydb-web

Local Development
-----------------

To develop locally, you need to start up the django server. The django server points to the built JS, so if you want a hot-reload on your JS, you also need to separately start up the vue server.


### Dev
We are currently working out the dev environment. For now it appears you need to comment out pyscopg2 and pymemc from the requirements.txt if you are installing it locally on Ubuntu. 
```
npm install -g yarn
pip install -r requirements.txt
```


```
### DJANGO ###
# either install [poetry](https://python-poetry.org/)
./django_serve.sh

# or directly install the requirements and run django
pip install -r requirements.txt
python manage.py runserver

# Mac Catalina Installation
- Install Poetry
- Install `xcode-select --install`
- Link open SSL stuff
    - `export LDFLAGS="-L/usr/local/opt/openssl@1.1/lib"`
    - `export CPPFLAGS="-I/usr/local/opt/openssl@1.1/include"`
- Install Postgre
    - `brew install postgresql`
- `poetry shell` to enter venv
- `pip install -r requirements.txt`
- `./django_serve.sh`

yarn start
```

Front-End Frameworks
--------------------

- Vue Good Tables
- Semantic UI Vue
- ApexCharts

Testing
-------

```
# this will run the django server which will also serve the built vue JS.
poetry python run manage.py runserver

# you can run this as well if you need a hot-reload for the frontend
yarn start
```

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

Python
------
This uses poetry for virtual environment creation. To add new dependencies, add them in hte pyproject.toml and then run `poetry lock; poetry install`. The `requirements.txt` is only for heroku and should be generated before deploying to heroku using `poetry run pip freeze > requirements.txt`.

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

Vue
-----

## Project setup
```
yarn install
```

### Compiles and hot-reloads for development
```
yarn serve
```

### Compiles and minifies for production
```
yarn build
```

### Lints and fixes files
```
yarn lint
```

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).

Special Thanks
--------------

- Timeline code based off of [vue-timeline-component](https://github.com/0xdv/vue-timeline-component)
