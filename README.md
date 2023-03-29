DRT.FM
========
--------

## Installation and configuration

1.  Install Python, virtualenv, npm and coffee script.

2. Clone the repository and cd into it
        $ cd ~/some/path/to/django-boiler

3.  Make, and activate a virtualenv:

        $ virtualenv venv --no-site-packages
        $ source venv/bin/activate

3.  Go through the following files, editing as necessary:

        `drt/settings/testing.py`
        `drt/settings/development.py`

4.  Symlink the project directory into the virtualenv's `site-packages`:

        $ cd drt/
        $ ln -s `pwd` ../venv/lib/python2.7/site-packages/drt

    Replace `python2.7` with the installed version of Python on your machine.

5.  Set the `DJANGO_SETTINGS_MODULE` environment variable now, and on every
    virtualenv activation:

        $ export DJANGO_SETTINGS_MODULE=drt.settings.development
        $ echo "!!" >> ../venv/bin/activate

6. Add the db directory for local development

        $ cd ~/some/path/to/django-boiler
        $ mkdir db

7.  Install the basic project requirements:

        $ cd ~/some/path/to/django-boiler/drt
        $ pip install -r requirements/DEVELOPMENT
        $ pip install -r requirements/TESTING        

    As you edit your `REQUIREMENTS` files, you can run those last commands again;
    `pip` will realize which packages you've added and will ignore those already
    installed. If for any reason you get a complaint about missing constance module run

        $ pip install -r requirements/COMMON
8. npm install --global coffeescript
9. Init and start the local development environment

        $ ./manage.py migrate
        $ ./manage.py bower install
        $ ./manage.py collectstatic
        $ ./manage.py runserver

    You should now be able to access the server at http://localhost:8000



#db backup

psql -h localhost -U drt -d drt -W
o23sR1n6LZgB
ssh -i "drtfm.pem" ubuntu@ec2-52-55-198-69.compute-1.amazonaws.com
pg_dump drt -h localhost -U drt > 2018XXXX_dump.sql
