# BackEnd

1. Prerequisities

   Before proceeding with the installation, ensure that the following prerequisites are met:

   - PostgreSQL 15 is installed on your system.
   - Python version 3.8 or higher max 3.11 is available in your environment.

   ```bash
   git clone https://github.com/NUS-Project-SaBai/BackEnd/
   ```

2. Set up postgreSQL Database

   - Install PostgreSQL 15 if not already installed.
   - Create a new PostgreSQL database for Project SaBai.

3. Configure Database Settings
   Navigate to the Backend directory and create a .env file if it is not present. Copy the content from `.env.example` and update the database configuration settings to match your PostgreSQL database credentials. Cloudinary credentials is in the Key Credentials doc.

## Activating the virtual environment

Assuming that you have successfully cloned the repository into your system and are inside the directory, the very first step is to activate your python virtual environment. This is a highly important step so as to clearly separate the dependencies of this project from those that already exist in your own system. Mixing them up can lead to some of your system dependencies to malfunction.

We will be using Pipenv. <https://pipenv.pypa.io/en/latest/>

Run this command if you have yet to install it:

```bash
pip install pipenv
```

To initialise a new `pipenv` environment for python 3.11 (note you must already have this python version installed):

```bash
pipenv --python 3.11
```

To use the virtual environment, run:

```bash
pipenv shell
```

To exit from the virtual environment, run:

```bash
exit
```

### Install dependencies

To install the dependencies, run:

```bash
pipenv install
```

\*Do this in the virtual environment

### Making migrations

This command checks the changes done and sets up the migrations to be done to the database

```bash
python manage.py makemigrations
```

### Migrating models to PostgreSQL database

This command updates the schema of the database based on the migrations set up

```bash
python manage.py migrate
```

Note: Above commands from installing requirements to migrating models only need to be done once during setup.

### Authentication (obtainin user accounts from auth0)

Running the following command in Backend folder will pull all the users from auth0 into Django database before starting the server

```bash
python manage.py get_auth0_users
```

### Running the server

Running this command runs the service locally

```bash
python manage.py runserver
```

A localhost link will be provided for you to access the service. It will look in the command line as such:

```bash
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
August 21, 2019 - 00:22:30
Django version 2.2.4, using settings 'sabaibiometrics.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

### Creating a superuser account in Django

```bash
python manage.py createsuperuser
```

### Creating the dummy users

```bash
python manage.py create_default_users
```

## pgAdmin4

This can be used as a tool to view your database and check if the data is correct.

To view data tables:

1.  Launch pgAdmin4
2.  Navigate to your database
3.  Schemas => public => table
4.  Right click table and view/edit data
