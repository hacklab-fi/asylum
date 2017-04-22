# asylum

Membership management for hacklabs. uses Python 3.4.

Uses django-environ for configurations, you can create `.env`-file in your project dir to override settings.

## TL;DR

Install docker and run the `docker/dev.sh` to set up a development enviroment. The script
will mount the project directory inside the docker container so that all modifications in
the `project/` take effect immediately. Do not create `.env` file yet.

## REST API

Access to all asylum models is available via REST (authentication required for reading as well).

Api root is https://yourserver.example.com/api/ and includes nice web-based API explorer, if
your user has authentication token issued you can get that with:

    curl -X POST --data 'username=YOU&password=YOURPASSWORD'  https://yourserver.example.com/api-auth/get-token/

To use token auth include the standard `Authorization: Token YOURTOKEN` header, like so:

    curl -X GET -H 'Authorization: Token YOURTOKEN' https://yourserver.example.com/api/members/types/

Admins can issue auth tokens to users via https://yourserver.example.com/admin/authtoken/token/

[DjangoFilterBackend][filterbacked] is enabled so you can use [Django lookup syntax][djangoqs] in GET parameters.

[filterbacked]: http://www.django-rest-framework.org/api-guide/filtering/#djangofilterbackend
[djangoqs]: https://docs.djangoproject.com/en/1.8/ref/models/querysets/#field-lookups

## Developer setup

Fork the repo on github and use you local fork as checkout source.

  - Make sure you have [Docker](https://www.docker.com/get-docker)
  - Clone your fork to local machine
  - `git remote add upstream https://github.com/hacklab-fi/asylum.git`
  - `docker/dev.sh`

That script will build docker image and map your checkout directory there so you can
edit the files directly in your checkout.

See also "Updating upstream changes".

## Install/setup in native

### General

Fork the repo on github and use you local fork as checkout source, you will want to add your own modules
with custom callbacks for automating things like mailing list subscriptions for new members

For Ubuntu 14.04 LTS

  - Make sure your're using UTF-8 locale
    - `sudo locale-gen en_US.UTF-8 ; export LC_ALL=en_US.UTF-8`
    - You will want to make your system default locale is UTF-8 one too, see your distribution documentation.
  - Add the original repo as upstream `git remote add upstream https://github.com/hacklab-fi/asylum.git`
  - Enter the "project" directory: `cd asylum/project`
  - Make a branch for your local changes `git checkout -b myhackerspace`
  - Install nodejs v4 first (needs PPA and key and stuff, nodesource has a handy script for this)

<pre><code>sudo apt-get install curl
curl -sL https://deb.nodesource.com/setup_4.x | sudo -E bash -
sudo apt-get install -y nodejs</code></pre>

  - `xargs -a <(awk '/^\s*[^#]/' "requirements.apt") -r -- sudo apt-get install` Installs all packages listed in requirements.apt
  - `sudo pip install maildump` currently not python3 compatible due to broken package, only needed if you're going to run in development mode
  - `` virtualenv -p `which python3` venv && source venv/bin/activate ``
    - Note: this might not work. If it doesn't, try `virtualenv-3.4`.
      If you don't have `virtualenv-3.4`, you might need to install it (`sudo pip3.4 install virtualenv`).
      If the installation command fails, you'll have to bootstrap pip for your python3 installation (`wget https://bootstrap.pypa.io/get-pip.py && sudo python3 get-pip.py`).
      Good luck.
  - `pip install -r requirements/local.txt` (or `pip install -r requirements/production.txt` if installing on production)
  - Create the postgres database
    - `sudo apt-get install postgresql-9.3` this is not in requirements.apt since you might want to use a dedicated postgres host.
    - `sudo su - postgres`
    - `createuser asylum && createdb -E utf-8 -T template0 -O asylum asylum && psql -U postgres -d postgres -c "alter user asylum with password 'asylum';"`
      - Change at least the password,in createdb `-O asylum` is the user that owns the database.
  - If installing for production create your `.env` file now.
  - `./manage.py migrate`
  - `find . -name '._*' | xargs rm ; for app in $( find . -path '*/locale' | grep -v venv/ ); do (cd $(dirname $app) && ../manage.py compilemessages ); done`
  - `./manage.py createinitialrevisions`
  - `./manage.py createsuperuser`
  - `npm run build`

### Production setup

  - Create a `.env` file in the project directory before running any of the manage.py commands above. See the example file, you need at least the following variables
      - DJANGO_SETTINGS_MODULE (=config.settings.production)
      - DJANGO_SENTRY_DSN
        - https://hub.docker.com/_/sentry/
        - https://docs.getsentry.com/hosted/
        - OR set `USE_SENTRY=False`
      - DATABASE_URL (=postgres://pguser:pgpassword@localhost/dbname)
      - DJANGO_SECRET_KEY
      - DJANGO_ADMIN_URL (=admin/)
      - DJANGO_ALLOWED_HOSTS (comma separated list)
  - `./manage.py collectstatic --noinput`
  - Setup uWSGI
    - `sudo apt-get install uwsgi-plugin-python3 uwsgi`
    - `sudo nano -w /etc/uwsgi/apps-available/asylum.ini` (see below)
    - `sudo ln -s /etc/uwsgi/apps-available/asylum.ini /etc/uwsgi/apps-enabled/asylum.ini`
    - `sudo service uwsgi restart`
  - Setup Nginx
    - `sudo apt-get install nginx`
    - `sudo nano -w /etc/nginx/sites-available/asylum.ini` (see below)
    - `sudo ln -s /etc/nginx/sites-available/asylum.ini /etc/nginx/sites-enabled/asylum.ini`
    - `sudo service nginx restart`
  - Configure backups
    - See the cronjobs below, offsite backups are recommended.

#### uWSGI config example

<pre><code>[uwsgi]
vhost = true
plugins = python3
# You could also use the unix socket but we use the http-one
http-socket = 127.0.0.1:9001
master = true
enable-threads = true
processes = 2
wsgi-file = /home/myhackerspace/asylum/project/config/wsgi.py
virtualenv = /home/myhackerspace/asylum/project/venv
chdir = /home/myhackerspace/asylum/project
touch-reload = /home/myhackerspace/asylum/project/reload
env = DJANGO_SETTINGS_MODULE=config.settings.production</code></pre>

#### Nginx config example

<pre><code>upstream asylum {
    server 127.0.0.1:9001 fail_timeout=0;
}
server {
    listen 80;
    server_name asylum.mylab.hacklab.fi;

    root /usr/share/nginx/html;
    index index.html index.htm;
    client_max_body_size 50M;
    keepalive_timeout 5;

    location / {
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $http_host;
        proxy_redirect off;
        proxy_pass http://asylum;
    }
}</code></pre>

## Updating upstream changes

In the `project` dir of your checkout (`myhackerspace` being the branch you want to
update upstream changes to)

    git checkout master
    git fetch upstream
    git rebase upstream/master master
    git checkout myhackerspace
    git merge master

And in the production server (or inside your Docker dev container):

    source venv/bin/activate
    pip install -r requirements/production.txt
    ./manage.py migrate
    npm run build
    ./manage.py collectstatic --noinput
    find . -name '._*' | xargs rm ; for app in $( find . -path '*/locale' | grep -v venv/ ); do (cd $(dirname $app) && ../manage.py compilemessages ); done

And if you have uWSGI configured `touch reload`, Docker dev env reloads automatically.

## Cron jobs

Until we maybe decide on Celery for running various (timed or otherwise) tasks add the following to your crontab:

    SHELL=/bin/bash
    @daily      cd /path/to/project ; source venv/bin/activate ; ./manage.py addrecurring
    @daily      cd /path/to/project ; set -o allexport ; source .env; set +o allexport ; pg_dump -c $DATABASE_URL | gzip >database_backup.sql.gz
    @daily      cd /path/to/project ; source venv/bin/activate ; ./manage.py import_holvidata # if using Holvi integrations

## Running in development mode

  - `maildump --http-ip 0.0.0.0 -p ~/maildump.pid` (maybe needs sudo)
    - Web interface at <http://localhost:1080/> (replace localhost with your vagrant ip)
  - `source venv/bin/activate`
  - `npm run watch &` If you want to develop the JS/LESS stuff this will autocompile them on change
  - `./manage.py runserver 0.0.0.0:8000`
  - `maildump -p ~/maildump.pid --stop`
  - Make localizations: `find . -name '._*' | xargs rm ; for app in $( find . -path '*/locale' | grep -v venv/ ); do (cd $(dirname $app) && ../manage.py makemessages ); done`
    - If you add your own apps, make sure to create the `locale` directory for them too.
  - use `npm run fix` to run autopep8 and friends before committing.

If you need the special environment variables in scripts not run via manage.py, use `set -o allexport ; source .env; set +o allexport` to load them.

## Backups and direct database access

See the cronjobs above for a nightly database dump. As for manual dump or restore start with  `set -o allexport ; source .env; set +o allexport` to load the environment.

For a manual dump run ```pg_dump -c $DATABASE_URL | gzip >database_backup_`date +%Y%m%d_%H%M`.sql.gz```.

For restore run ```zcat database_backup.sql.gz | psql $DATABASE_URL``` (you might need to drop and recreate the database first, see the setup instructions for creating)

## About the example handlers

Use these as example for building your own callbacks (though some might be rather useful as-is).
