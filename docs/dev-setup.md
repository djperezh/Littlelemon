
## Technical Requirements
* Python
* pip
* pipenv

# Dev SetUp
This setup is using VS Code as suggested IDE

Intalls the following VS Code extensions
* Python
* SQLite OR MySQL
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

7. For MySQL, make sure mysql service is running. If not, you can start the service using the following commands (assuming that mysql was installed using Homebrew):

```shell
brew services start mysql 
```
For stopping the service, use:
```shell
brew services stop mysql 
```

You probably will need the MySQL DB API Driver, so from the CMD terminal in VS Code, use PIP utility with following command:

```shell
pip3 install mysqlclient
```

Once mySql service is running, connect to the DB (use `root` as password):
```shell
mysql -u root -p
```

NOTE: make sure you run the migrations before to run the server/service
