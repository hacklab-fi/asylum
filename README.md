# asylum

Membership management for hacklabs. uses Python 3.4.

Uses django-environ for configurations, create `.env`-file in your project dir to override settings.

## Install/setup

For Ubuntu 14.04 LTS

  - `xargs -a <(awk '/^\s*[^#]/' "requirements.apt") -r -- sudo apt-get install` Installs all packages listed in requirements.apt
  - `sudo pip install maildump` currently not python3 compatible due to broken package
  - `` virtualenv -p `which python3.4` venv && source venv/bin/activate ``
    - Note: this might not work. If it doesn't, try `virtualenv-3.4`.
      If you don't have `virtualenv-3.4`, you might need to install it (`sudo pip3.4 install virtualenv`).
      If the installation command fails, you'll have to bootstrap pip for your Python3.4 installation (`wget https://bootstrap.pypa.io/get-pip.py && sudo python3.4 get-pip.py`).
      Good luck.
  - `pip install -r requirements/local.txt` (or `pip install -r requirements/production.txt` if installing on production)
  - `./manage.py migrate`
  - `./manage.py createsuperuser`

### uWSGI & Nginx setup

NOTE: the "sane defaults" are for local development, for production create a `.env` file which at least sets the following variables

  - DJANGO_SETTINGS_MODULE (=config.settings.production)
  - DJANGO_SENTRY_DSN
  - DATABASE_URL

## Running in development mode

  - `maildump --http-ip 0.0.0.0 -p ~/maildump.pid` (maybe needs sudo)
    - Web interface at <http://localhost:1080/> (replace localhost with your vagrant ip)
  - `source venv/bin/activate`
  - `./manage.py runserver 0.0.0.0:8000`
  - `maildump -p ~/maildump.pid --stop`

If you need the special environment variables in scripts not run via manage.py, use `source .env` to load them.

