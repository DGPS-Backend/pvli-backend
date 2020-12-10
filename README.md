# Django Starter Project

This repo is a starting point for a clasic django web service project running on docker that have the following services:

* **web:** Web server running django on port 8000.
* **worker:** Run async tasks with celery.
* **redis:** Used to store celery tasks.
* **nginx:** So this nginx proxy server will help us handle requests and serving static files.

The database should be configured in the host machine, as it is easier for development.

## Getting started
If you are starting a new project go ahead and clone this repo in a directory of your choosing

Create a database for your project. Then you need to create a file called `.env` and write the environment variables you wish to use for development

```
ENV=dev
DEBUG=on
SECRET_KEY='123'
DATABASE_URL=postgres://<user>:<password>@127.0.0.1:5432/<db_name>
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
USE_DEBUG_TOOLBAR=on
ALLOWED_HOSTS=web,localhost,127.0.0.1

#Celery Broker with redis
#CELERY_BROKER_URL=redis://localhost:6379/0

#Sentry
#LOGS_ROOT=./logs
#USE_SENTRY=on
#SENTRY_DSN=https://<project-key>@sentry.io/<project-id>
```

We now need to override `DATABASE_URL` environment variable inside of Docker to connect directly to you host machine. Create a file called `.env.docker` with the following content:

```
DATABASE_URL=postgres://<user>:<password>@<host>:5432/<db_name>
```

* **user** is the user in your host machine that has access to postgres in this case.
* **password** is the user password in your host machine that has access to postgres database.
* **host** is the ip or address of your host machine.
* **db_name** Database name.

We are all set up for bringing everything live with

```
docker-compose up
```

Wait for everything to load, and you can visit `https://127.0.0.1:8000` and your new awesomely configured site will be there.



## Docker commands
Here are a few commands that may come in handy

Command | Description
--- | ---
`docker ps` | List all containers (-a to include stopped)
`docker logs --follow <container_id>` | Display the logs of a container
`docker exec -it <container_id> /bin/bash` | Attach into a running container
`docker run --rm <image_name> /bin/bash` | Run a docker container based on an image and get a prompt
`docker-compose run --rm web /bin/bash` | Same as before but for services defined in docker-compose.yml
`docker-compose run --rm web /bin/bash -c 'python manage.py migrate'` | Run a management command

## Old fashion install
First of all, install pipenv so you can use the specified python version (check out .python-version). Then, run `pip install pipenv` to install it's pip's successor: pipenv. Then install dependencies by running `pipenv install`. You can now start developing.

These commands are at your disposal:

Command | Shortcut for
--- | ---
`pipenv run server` | `gunicorn conf.wsgi:application --bind 0.0.0.0:8000`
`pipenv run server_dev` | `python manage.py runserver`
`pipenv run tests` | `pytest`
`pipenv run celery` | `python manage.py celery_autoreload`
`pipenv run shell` | `python manage.py shell`
`pipenv run makemigrations` | `python manage.py makemigrations`
`pipenv run migrate` | `python manage.py migrate`
`pipenv run createsuperuser` | `python manage.py createsuperuser`
`pipenv run static` | `python manage.py collectstatic`
`pipenv run isort` | isort is a Python utility / library to sort imports alphabetically, and automatically separated into sections. 
`pipenv run flake8` | Flake8 runs all the tools by launching the single flake8 command. It displays the warnings in a per-file, merged output.

To compile your static files, you need to run `pipenv run static`.

### Environment variables
These environment variables can be provided to configure your project.

#### Django

Name | Values | Default | Description
--- | --- | --- | ---
ENV | dev, test, qa, prod | prod | Indicates in which environmet the project is running on
DEBUG | on, off | off | Run server in debug mode
LANGUAGE_CODE | Language Identifier (RFC 3066) | en-US | [List of language codes](http://www.i18nguy.com/unicode/language-identifiers.html)
TIME_ZONE | Record of IANA time zone database | America/Santiago | [List of timezones](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)
USE_I18N | on, off | on | Enable translation system
USE_L10N | on, off | on | Enable localized formatting
USE_TZ | on, off | on | Enable timezone aware dates in
DEFAULT_FROM_EMAIL | E-mail addresss | -- | Email address from which transactional emails will be sent from
EMAIL_BACKEND | Path to backend | django.core.mail.backends.smtp.EmailBackend | The backend to use for sending emails. [List of backends](https://docs.djangoproject.com/en/2.2/topics/email/#email-backends)
SECRET_KEY | Random string | -- | Used to provide cryptographic signing
ALLOWED_HOSTS | List of domains | -- | Represents the host/domain names that this site can serve.
DJANGO_DATABASE_URL | Database url | -- | Describes the database connection with [a url strucure](https://github.com/joke2k/django-environ).
LOGIN_URL | Url | /login/ | Url to redirect users when login is needed
LOGIN_REDIRECT_URL | Url | / | Url to redirect users after login in
STATIC_URL | Url | /static/ | Url from which static files are served
MEDIA_URL | Url | /media/ | Url from which media files are served

#### Django Registration Redux 

[Documentation](https://django-registration-redux.readthedocs.io)

Name | Values | Default | Description
--- | --- | --- | ---
ACCOUNT_ACTIVATION_DAYS | int | 7 | How long (in days) after signup an account has in which to activate.
REGISTRATION_OPEN | on, off | on | Indicates whether registration of new accounts is currently permitted.
REGISTRATION_AUTO_LOGIN | on, off | on | If this is True, your users will automatically log in when they click on the activation link in their email.

#### Celery

Name | Values | Default | Description
--- | --- | --- | ---
CELERY_BROKER_URL | Database url | -- | A common value for development is to use redis://cache, but it's recommended for production to use RabbitMQ
CELERY_TASK_ALWAYS_EAGER | on, off | off | If this is True, all tasks will be executed locally by blocking until the task returns. 

#### Loggin & Sentry

Name | Values | Default | Description
--- | --- | --- | ---
LOGS_ROOT | path | -- | Path to the directory where logs are to be stored
USE_SENTRY | on, off | off | Enables sentry
SENTRY_DSN | string | -- | Private URL-like configuration
