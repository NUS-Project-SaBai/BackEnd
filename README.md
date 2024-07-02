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

### Windows

We will be using virtualenv to set up our virtual environment. <https://python-guide-ru.readthedocs.io/en/latest/dev/virtualenvs.html>

Run this command if you have yet to install it:

```bash
pip install virtualenv
```

For setting up the virtual environment for the first time:

```bash
virtualenv venv
```

This creates a /venv folder in your directory. Optimally, you will never need to touch this folder.

Starting the virtual environment (for Windows, using powershell):

```bash
.\venv\Scripts\activate
```

Activate virtual environment (You should see the following):

```bash
(venv) PS C:\Users\angpe\Desktop\work\New folder>
```

Now that your environment is activated, you can install Python packages using pip. Packages installed while the environment is activated will only be available within this environment.

Deactivating the virtual environment

```bash
deactivate
```

Deactivated virtual environment (You should see the following):

```bash
PS C:\Users\angpe\Desktop\work\New folder>
```

### MacOS

We will be using virtualenv to set up our virtual environment. <https://python-guide-ru.readthedocs.io/en/latest/dev/virtualenvs.html>

Run this command if you have yet to install it:

```bash
pip install virtualenv
```

For setting up the virtual environment for the first time:

```bash
virtualenv venv
```

If your Python environment is managed externally, likely by Homebrew (on MacOS), you might get an error message. An alternative step to set up virtual environment (recommended by ChatGPT) is:

Navigate into your backend directory.

Run the following code:

```bash
python3 -m venv myenv
```

You've created a virtual environment called myenv using venv module

Starting the virtual environment (for MacOS)

```bash
source venv/bin/activate
```

Active virtual environment (You should see the following):

```bash
(venv) Angelico-MBP:sabai_2019 angelico$
```

Now that your environment is activated, you can install Python packages using pip. Packages installed while the environment is activated will only be available within this environment.

Deactivating the virtual environment:

```bash
deactivate
```

Deactivated virtual environment (You should see the following):

```bash
Angelico-MBP:sabai_2019 angelico$
```

### Installing requirements (ensure you are in venv!)

```bash
pip install -r requirements.txt
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

### Authentication

Running the following command in Backend folder will pull all the users from auth0 into Django database before starting the server

```bash
./start-server.sh
```
