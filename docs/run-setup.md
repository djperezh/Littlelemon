## Technical Requirements
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