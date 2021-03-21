This was built using [this](https://dev.to/shakib609/deploy-your-django-react-js-app-to-heroku-2bck).

Local Development
-----------------

To develop locally, you need to start up the django server. The django server points to the built JS, so if you want a hot-reload on your JS, you also need to separately start up the react server.

```
### DJANGO ###
# either install [poetry](https://python-poetry.org/)
poetry run pip install -r requirements.txt
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
- Install Postgres
    - `brew install postgresql`
- `poetry shell` to enter venv
- `pip install -r requirements.txt`
- `./django_serve.sh`

### React ###
yarn start
```

If you want to reference the bios, you must supply the airtable table id and key as environment variables.

```
AIRTABLE_KEY=
AIRTABLE_TABLE_ID=
```

Testing
-------

```
# this will run the django server which will also serve the built react JS.
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
```

To deploy to heroku, use the `./heroku.sh` script which both freezes and requirements and pushes the code.

create-react-app docs
---------------------

# Getting Started with Create React App

This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).

## Available Scripts

In the project directory, you can run:

### `yarn start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

The page will reload if you make edits.\
You will also see any lint errors in the console.

### `yarn test`

Launches the test runner in the interactive watch mode.\
See the section about [running tests](https://facebook.github.io/create-react-app/docs/running-tests) for more information.

### `yarn build`

Builds the app for production to the `build` folder.\
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.\
Your app is ready to be deployed!

See the section about [deployment](https://facebook.github.io/create-react-app/docs/deployment) for more information.

### `yarn eject`

**Note: this is a one-way operation. Once you `eject`, you can’t go back!**

If you aren’t satisfied with the build tool and configuration choices, you can `eject` at any time. This command will remove the single build dependency from your project.

Instead, it will copy all the configuration files and the transitive dependencies (webpack, Babel, ESLint, etc) right into your project so you have full control over them. All of the commands except `eject` will still work, but they will point to the copied scripts so you can tweak them. At this point you’re on your own.

You don’t have to ever use `eject`. The curated feature set is suitable for small and middle deployments, and you shouldn’t feel obligated to use this feature. However we understand that this tool wouldn’t be useful if you couldn’t customize it when you are ready for it.

## Learn More

You can learn more in the [Create React App documentation](https://facebook.github.io/create-react-app/docs/getting-started).

To learn React, check out the [React documentation](https://reactjs.org/).

### Code Splitting

This section has moved here: [https://facebook.github.io/create-react-app/docs/code-splitting](https://facebook.github.io/create-react-app/docs/code-splitting)

### Analyzing the Bundle Size

This section has moved here: [https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size](https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size)

### Making a Progressive Web App

This section has moved here: [https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app](https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app)

### Advanced Configuration

This section has moved here: [https://facebook.github.io/create-react-app/docs/advanced-configuration](https://facebook.github.io/create-react-app/docs/advanced-configuration)

### Deployment

This section has moved here: [https://facebook.github.io/create-react-app/docs/deployment](https://facebook.github.io/create-react-app/docs/deployment)

### `yarn build` fails to minify

This section has moved here: [https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify](https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify)
