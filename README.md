# voting-backend

A practice-use repo including basic functioality of a voting application API built by Django.

[![Python Version](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/)
[![Django Version](https://img.shields.io/badge/django%20versions-2.1.1-blue.svg)](https://www.djangoproject.com/)

### Prerequisites

What things you need to install and how to install them:

- [Python](https://www.python.org/downloads/) 3.6
- [pipenv](https://pipenv.readthedocs.io/en/latest/) 2018.10.13 or above
- [PostgreSQL](https://www.postgresql.org/download/) 9.6 or above
  - During install, you will be prompted to setup credentials for a root user. Please jot them down as you have to use them later in the `.env` file.

### Procedures

1. Clone this repository: `git clone https://github.com/ytkalan/voting_backend.git`

2. Setup `pipenv` and Python dependencies:

   ```shell
   pip install --user pipenv
   pipenv --python 3.6
   ```


   After successful setup, a prefix `(env_name)` should appear on the left of your terminal.

   ```
   (env) C:\Users\User\Projects\voting_backend> 
   ```

3. Create the environment file `.env` on the root directory
    - To create the `.env` file, open Git Bash and type:

     ```shell
     touch .env
     ```

### Environmental Variables

| Name | Required | Value |
|------|----------|---------|
| `SECRET_KEY` | :heavy_check_mark: | String |
| `DATABASE_URL` | :heavy_check_mark: | SQL String |

Example setup (copying this would not work):

```
SECRET_KEY=a-very-long-secret-key
DATABASE_URL=postgres://username:password@localhost:5432/voting_app

```

### API Development

1. Install python packages

   ```shell
   pipenv sync --dev
   ```

2. Create databases

   ```shell
   psql -c "CREATE DATABASE voting_app;" -U postgres
   ```

3. Migrate databases

   This step creates / updates the table schemas defined in the django project onto the databases.

   ```shell
   python manage.py migrate --database=default
   ```

4. Load data fixtures

   ```shell
   python manage.py loaddata ./voting_backend/fixtures/vote_campaign.json --database=default 
   python manage.py loaddata ./voting_backend/fixtures/vote_option.json --database=default
   python manage.py loaddata ./voting_backend/fixtures/vote_record.json --database=default

5. Run the server

   ```shell
   python manage.py runserver
   ```
