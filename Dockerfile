FROM ubuntu:18.04
ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND noninteractive
EXPOSE 8000

# Usual update / upgrade with locale setup
RUN apt-get update \
    && apt-get dist-upgrade -y \
    && apt-get install -yq software-properties-common sudo curl locales\
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/* \
    && echo en_US.UTF-8 UTF-8 >> /etc/locale.gen \
    && locale-gen \
    && ln -fs /usr/share/zoneinfo/Europe/Helsinki /etc/localtime

ENV LANG='en_US.UTF-8' LANGUAGE='en_US:en' LC_ALL='en_US.UTF-8' LC_CTYPE='en_US.UTF-8'


# Install basics
RUN apt-get update \
    && apt-get install -yq postgresql git python3-dev virtualenv python3-virtualenv vim \
    python3-pip python-pip npm \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

# Install maildump
EXPOSE 1080
RUN pip install --no-cache-dir maildump

# Create database
USER postgres
RUN service postgresql start && \
    createuser asylum && \
    createdb -E utf-8 -T template0 -O asylum asylum && \
    psql -U postgres -d postgres -c "alter user asylum with password 'asylum'; alter user asylum with createdb;"

# Create a newuser
USER root
RUN adduser --disabled-password --gecos '' asylum && \
    adduser asylum sudo && \
    echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

# Create volume
RUN mkdir /opt/asylum/ && chown asylum:asylum /opt/asylum/
# VOLUME /opt/asylum/ # Your local uid != 1000? Tough. Create an issue and add an idea how to fix it.
WORKDIR /opt/asylum/

# Install system packages
COPY project/requirements.apt /opt/asylum/
RUN apt-get update \
    && awk '/^\s*[^#]/' requirements.apt | xargs -r -- sudo apt-get install --no-install-recommends -y \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

USER root

# Install python requirements
RUN virtualenv -p `which python3` ../asylum-venv
COPY project/requirements /opt/asylum/requirements/
RUN . ../asylum-venv/bin/activate && \
    pip3 install --no-cache-dir packaging appdirs urllib3[secure] && \
    pip3 install --no-cache-dir -r requirements/local.txt && \
    chown -R asylum:asylum ../asylum-venv && \
    true

# Configure application
USER root
RUN echo "DATABASE_URL=postgres://asylum:asylum@localhost/asylum" > .env
COPY project /opt/asylum/
RUN chown -R asylum:asylum /opt/asylum/

# Build localisations
USER asylum
RUN . ../asylum-venv/bin/activate && \
    for app in locale */locale; do (cd $(dirname $app) && ../manage.py compilemessages ); done

# Run migrate and create admin user
USER asylum
RUN npm run build \
    && sudo -u postgres service postgresql start; \
    . ../asylum-venv/bin/activate \
    && export PGPASSWORD=asylum; while true; do psql -q asylum -c 'SELECT 1;' 1>/dev/null 2>&1 ; if [ "$?" -ne "0" ]; then echo "Waiting for psql"; sleep 1; else break; fi; done \
    && ./manage.py migrate \
    && echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'nospamplz@hacklab.fi', 'admin') ; from rest_framework.authtoken.models import Token ; Token.objects.create(user=User.objects.get(username='admin'), key='deadbeefdeadbeefdeadbeefdeadbeefdeadbeef')" | ./manage.py shell

ENTRYPOINT ["/opt/asylum/docker-entrypoint.sh"]
