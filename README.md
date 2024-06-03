# OpenClinic
A simple to use, self-contained portable clinic application
for use in overseas missions to manage clinic operations.

## Getting Started
Running this project would require basics in git and the use of the command line. Refer to the section on **Basics** below for a quick rundown and a list of resources.
***

### Activating the virtual environment
Assuming that you have successfully cloned the repository into your system and are inside the directory, the very first step is to activate your python virtual environment. This is a **highly** important step so as to clearly separate the dependencies of this project from those that already exist in your own system. Mixing them up can lead to some of your system depencies to malfunction.

We will be using [virtualenv](https://python-guide-ru.readthedocs.io/en/latest/dev/virtualenvs.html) to set up our virtual environment. Run this command if you have yet to install it:

```
$ pip install virtualenv
```

 For setting up the virtual environment for the first time:

```
$ virtualenv venv
```

This creates a /venv folder in your directory. Optimally, you will never need to touch this folder.

Starting the virtual environment:
```
$ source venv/bin/activate
```

This command needs to be run everytime you are working on your project! Or else, you run the risk of installing dependencies/ packages straight into your system.

To ascertain that the virutal environment is active, you should be able to see the word 'venv' appear on the latest line of your terminal/ shell:
```
(venv) (base) Angelico-MBP:sabai_2019 angelico$ 
```

Deactivating the virtual environment:
```
$ deactivate
```

To ensure that it is indeed inactive, the word 'venv' would be gone from the latest line of your terminal/ shell:
```
(base) Angelico-MBP:sabai_2019 angelico$ 
```

### Making migrations
This command checks the changes done and sets up the migrations to be done to the database

```
$ python manage.py makemigrations
```

### Migrating models to PostgreSQL database
This command updates the schema of the database based on the migrations set up

```
$ python manage.py migrate
```

### Running the server
Running this command runs the service locally

```
$ python manage.py runserver
```

A localhost link will be provided for you to access the service. It will look in the command line as such:

```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
August 21, 2019 - 00:22:30
Django version 2.2.4, using settings 'sabaibiometrics.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

### Common Issues

#### Issue involving psycopg2
This should occur mostly for Mac OS users. The issue will look as such on the terminal:

```
ImportError: dlopen(/Users/Craig/pyenv/mysite/lib/python2.7/site-packages/psycopg2/_psycopg.so, 2): Library not loaded: @executable_path/../lib/libssl.1.0.0.dylib

Referenced from: /Applications/Postgres.app/Contents/MacOS/lib/libpq.dylib

Reason: image not found
```

##### References
- https://stackoverflow.com/questions/16407995/psycopg2-image-not-found
- https://medium.com/pixel-heart/os-x-sierra-postgresql-and-psycopg2-42c0c95acb23
- https://medium.com/@ssscripting/fixing-library-not-loaded-usr-local-opt-openssl-1-1-lib-libssl-1-1-dylib-loaderror-d4c2a21ddf9

Here are the possible solutions that you could try in order:

##### Re-install psycopg2
```
$ pip uninstall psycopg2
$ pip install psycopg2
```

##### Re-install postgreSQL
```
$ brew update
$ brew doctor
$ brew install postgresql
```

##### Install/ re-install openSSL

```
$ brew install openssl
```

##### Link the appropriate libraries from openSSL
To correctly do this, take note of the library that cannot be loaded in your error message. For the error message above, the library in question is `libssl.1.0.0.dylib`. For this library, copy-paste the commands below and run it:

```
$ sudo ln -s /usr/local/Cellar/openssl/<insert version here>/lib/libssl.1.0.0.dylib /usr/local/lib

$ sudo ln -s /usr/local/Cellar/openssl/<insert version here>/lib/libcrypto.1.0.0.dylib /usr/local/lib
```

To check out the correct version of openssl you can move to the directory and view its contents:

```
$ cd /usr/local/Cellar/openssl

$ ls
```

It should only contain one directory, named as the version.

If the library in question is `libssl.1.1.dylib`, you would need to ensure that you have version 1.1 of openSSL. You can download it via Homebrew:

```
$ brew reinstall openssl@1.1
```

You can then copy-paste the commands below and run it:

```
$ sudo ln -s /usr/local/Cellar/openssl@1.1/<insert version here>/lib/libssl.1.1.dylib /usr/local/lib

$ sudo ln -s /usr/local/Cellar/openssl@1.1/<insert version here>/lib/libcrypto.1.1.dylib /usr/local/lib
```





## API Documentation
The OpenClinic API is separated into different modules.
For example, all functions related to patients is done
by the patients module. The API Documentation will be
separated by these modules.

### Errors
All successful requests return a HTTP status code of 200. 
If the requested resource is not found, a status code of 404
is sent. If the request is malformed due to user error, a status
code of 400 is sent. Any 500 series error indicates a bug on
the application side, and a bugfix request will need to be sent.

### Patient
#### GET: /patients/by_name
Parameters:
```
name: Full or partial name of the patient(s) you want 
to retrieve
```
This endpoint retrieves an array of patient objects. The
'name' parameter is used as a substring to retrieve all
patients with that string in their name.

Result:
```
[
  {
    "model": "clinicmodels.patient",
    "pk": 1,
    "fields": {
      "village_prefix": "TGV",
      "name": "Aloha Samsam",
      "contact_no": "12345678",
      "gender": "Female",
      "travelling_time_to_village": 30,
      "date_of_birth": "1995-09-30",
      "drug_allergy": "all",
      "parent": 1,
      "face_encodings": "22",
      "picture": "static/images/Screenshot_1_w0Aipr6.png"
    }
  }
]
```

#### GET: /patients/by_id
Parameters:
```
id: Primary key of the Patient you want to retrieve
```
This endpoint retrieves a Patient object in a one element 
array according to the primary key provided by the id.

## Basics

### Git

#### Reference 
https://git-scm.com/docs

#### Common Commands
These are the common commands that will be used throughout the duration of the project. Do familiarise yourself with them through the link above and know how to correctly use them.
- git add
- git commit
- git push
- git pull
- git clone
- git checkout

### Command Line

#### Reference 
https://lifehacker.com/a-command-line-primer-for-beginners-5633909

#### Common Commands
Aside from running program commands such as `python` or `git`, these are commands as well that will be used a lot of times when in the terminal/ shell:
- cd
- ls
- rm
- find