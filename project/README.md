# asylum

Membership management for hacklabs. uses Python 3.4.

Uses django-environ for configurations, create `.env`-file in your project dir to override settings.

## Install/setup

For Ubuntu 14.04 LTS

  - Install nodejs v4 first (needs PPA and key and stuff, nodesource has a handy script for this)

    sudo apt-get install curl
    curl -sL https://deb.nodesource.com/setup_4.x | sudo -E bash -
    sudo apt-get install -y nodejs

  - `xargs -a <(awk '/^\s*[^#]/' "requirements.apt") -r -- sudo apt-get install` Installs all packages listed in requirements.apt
  - `sudo pip install maildump` currently not python3 compatible due to broken package
  - `` virtualenv -p `which python3.4` venv && source venv/bin/activate ``
    - Note: this might not work. If it doesn't, try `virtualenv-3.4`.
      If you don't have `virtualenv-3.4`, you might need to install it (`sudo pip3.4 install virtualenv`).
      If the installation command fails, you'll have to bootstrap pip for your Python3.4 installation (`wget https://bootstrap.pypa.io/get-pip.py && sudo python3.4 get-pip.py`).
      Good luck.
  - `pip install -r requirements/local.txt` (or `pip install -r requirements/production.txt` if installing on production)
  - `./manage.py migrate`
  - `find . -name '._*' | xargs rm ; for app in locale */locale; do (cd $(dirname $app) && ../manage.py compilemessages ); done`
  - `./manage.py createinitialrevisions`
  - `./manage.py createsuperuser`
  - `npm run build`
  - `./manage.py collectstatic --noinput`

### uWSGI & Nginx setup

NOTE: the "sane defaults" are for local development, for production create a `.env` file which at least sets the following variables

  - DJANGO_SETTINGS_MODULE (=config.settings.production)
  - DJANGO_SENTRY_DSN
  - DATABASE_URL

## Cron jobs

Until we maybe decide on Celery for running various (timed or otherwise) tasks add the following to your crontab:

    @daily      cd /path/to/project ; source venv/bin/activate ; ./manage.py addrecurring

## Running in development mode

  - `maildump --http-ip 0.0.0.0 -p ~/maildump.pid` (maybe needs sudo)
    - Web interface at <http://localhost:1080/> (replace localhost with your vagrant ip)
  - `source venv/bin/activate`
  - `npm run watch &` If you want to develop the JS/LESS stuff this will autocompile them on change
  - `./manage.py runserver 0.0.0.0:8000`
  - `maildump -p ~/maildump.pid --stop`

If you need the special environment variables in scripts not run via manage.py, use `set -o allexport ; source .env; set +o allexport` to load them.
