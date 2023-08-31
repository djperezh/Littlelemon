# Littlelemon
Example application in Python using Django Framework
Coursera: [Meta API](https://www.coursera.org/learn/apis?specialization=meta-back-end-developer)

## Requirements
* Python
* pip
* pipenv

# Run Locally
Open a Terminal session and run the followin commands
## Activate virtual environment using pipenv
```
pipenv shell
```
NOTE: use `deactivate` command to exit the virtual environment
## Install project dependencies
```
pipenv install
```
## Make and Apply migrations
```
python3 manage.py makemigrations
```
```
python3 manage.py migrate
```
## Run the Server (API)
```
python manage.py runserver
```
# Dev SetUp
This setup is using VS Code as suggested IDE

Intalls the following VS Code extensions
* Python
* SQLite
* Python Indent
* Postman
* Django

1. Clone repository
2. Open Project forlder on VS Code
3. Open a Terminal window inside VS Code
4. Activate virtual environment using pipenv
   - pipenv shell
5. Attach the virtual environment to VS Code
   - < CTRL > < SHIFT > < P > + "Pyhton: Select Interpreter" + < Select the created by the Virtual Environment >)
6. Install project dependencies
   - pipenv install

NOTE: make sure you run the migrations before to run the server/service
