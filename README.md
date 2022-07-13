# FlaskAPIRest

Rest API developed in Flask (Python) with JSON Web Token authentication.

Endpoints can only be accessed after login. Otherwise, error will appear.

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

## Run Server with BATCH file (only for Windows)

Open the project folder that contains the app.py file.

Run the run_server.bat file

## Test

The file FlaskAPICollection.postman_collection.json contains the test automation.

Import this file in Postman.

You must send a login request first. The response will save the token in global variable.

Then, you wll have the permission to access others requests.

## Credentials

Username
```bash
financeiro
```
Password
```bash
financeiro01
```

## Filter

In requests, you can put some text and if it is in any field, it will return only the lines that contain the text (it doesn't have to be the exact text).

Example:
```bash
/patients?filter=joan
```

The response will return the lines with JOANA.
