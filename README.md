# FlaskAPIRest

Rest API developed in Flask (Python) with user authentication.

Endpoints can only be accessed after login. Otherwise, error 403 will appear.

When accessing an endpoint, the user will see the requested information in JSON format.

## Installation

Use the requirements file to install all packages

```bash
pip install -r requirements.txt
```

## Run Server with CMD

Open the project folder that contains the app.py file.

Run the commands below.

```bash
set FLASK_APP=app
set FLASK_ENV=development
flask run
```

## Run Server with BATCH file

Open the project folder that contains the app.py file.

Run the run_server.bat file

## Usage

Now head over to http://127.0.0.1:5000, and you should see the login page.

Enter with the credentials below.

Username
```bash
financeiro
```
Password
```bash
financeiro01
```

You will be redirect to index page.

Choose which endpoint you want to access. The options are patients, pharmacies and transactions.

Each endpoint returns the information in JSON format.
