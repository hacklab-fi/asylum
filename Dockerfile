FROM ubuntu:14.04
ENV PYTHONUNBUFFERED 1
EXPOSE 8000

# Install basics
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y build-essential postgresql
RUN apt-get install -y python-virtualenv python3-pip # to make builds faster

# Create database
RUN service postgresql start && \
    su -c "createuser asylum" postgres && \
    su -c "createdb -E utf-8 -T template0 -O asylum asylum" postgres && \
    su -c "psql -U postgres -d postgres -c \"alter user asylum with password 'asylum';\"" postgres

# Install system packages
COPY project/requirements.apt /opt/asylum/
WORKDIR /opt/asylum
RUN awk '/^\s*[^#]/' requirements.apt | xargs -r -- sudo apt-get install --no-install-recommends -y
RUN virtualenv -p `which python3.4` ../asylum-venv

# Install python requirements
COPY project/requirements /opt/asylum/requirements/
WORKDIR /opt/asylum
RUN . ../asylum-venv/bin/activate && pip install -r requirements/local.txt

# Configure application
COPY project /opt/asylum/
RUN echo "DATABASE_URL=postgres://asylum:asylum@localhost/asylum" > .env

# Create
RUN service postgresql start; \
    . ../asylum-venv/bin/activate && \
    ./manage.py migrate && \
    echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'nospamplz@hacklab.fi', 'admin')" | ./manage.py shell

ENTRYPOINT ["/opt/asylum/docker-entrypoint.sh"]
