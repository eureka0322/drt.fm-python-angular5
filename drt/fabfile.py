# -*- coding: utf-8 -*-

import sys
from os.path import abspath, dirname, join
from contextlib import contextmanager as _contextmanager

from fabric.utils import puts
from fabric.api import cd, lcd, run, sudo, env, prefix, local, settings, abort
from fabric.contrib.console import confirm
from fabric.contrib.files import upload_template
from fabric.contrib import django

env.git_url = 'git@gitlab.com:panda-network/drt.git'
env.git_branch = 'master'
env.local_path = dirname(abspath(__file__))
sys.path.append(env.local_path)
sys.path.append(join(env.local_path, 'drt'))

django.settings_module('drt.settings.test')

env.hosts = ['52.44.247.129']
env.user = 'ubuntu'
env.forward_agent = True

env.parent_path = '/web/'
env.project_path = '/web/drt.fm/'
env.manage_path = '/web/drt.fm/drt/'
env.activate = 'source /web/drt.fm/venv/bin/activate'
env.requirements = 'requirements/PRODUCTION'
env.settings_path = 'drt.settings.production'
env.nginx_restart = '/etc/init.d/nginx restart'
env.supervisor_restart = 'supervisorctl reload'
env.server_name = 'drt.fm'
env.http_auth = False
env.http_user = 'ubuntu'
env.http_password = '{SSHA}ldonehNHmXvQN8ic7CULuJ/UaFxxRXJi'
env.test_settings_module = 'drt.settings.test'
env.https = False
env.browser_cache = False
env.wsgi_module = 'drt.wsgi'

@_contextmanager
def virtualenv():
    with cd(env.manage_path):
        with prefix(env.activate):
            yield


def _requirements_and_static():
    run('pip install -r {0}'.format(env.requirements))
    run('python manage.py bower install --settings={0}'.format(env.settings_path))
    run('python manage.py collectstatic --noinput --settings={0}'.format(env.settings_path))
    run('python manage.py assets build --settings={0}'.format(env.settings_path))


def _ec2():
    env.user = 'ubuntu'
    env.nginx_restart = 'sudo service nginx restart'
    env.project_path = '/web/drt.fm/'
    env.manage_path = '/web/drt.fm/drt/'
    env.activate = 'source /web/drt.fm/venv/bin/activate'


def production():
    _ec2()
    env.settings_path = 'drt.settings.production'
    env.hosts = ['52.55.198.69']
    env.key_filename = '~/.ssh/drtfm.pem'
    env.git_branch = 'master'
    env.git_url = '-b {0} {1}'.format(env.git_branch, env.git_url)
    env.server_name = 'drt.fm'
    env.nginx_restart = 'sudo /etc/init.d/nginx restart'
    env.supervisor_restart = 'sudo supervisorctl -c /etc/supervisor/supervisord.conf reload'
    env.http_auth = False
    env.https = False
    env.browser_cache = True


def staging():
    _ec2()
    env.settings_path = 'drt.settings.staging'
    env.hosts = ['52.71.60.10']
    env.key_filename = '~/.ssh/onstage.pem'
    env.git_branch = 'development'
    env.git_url = '-b {0} {1}'.format(env.git_branch, env.git_url)
    # env.server_name = 'staging.drt.fm'
    env.server_name = '52.71.60.10'
    env.nginx_restart = 'sudo /etc/init.d/nginx restart'
    env.supervisor_restart = 'sudo supervisorctl -c /etc/supervisor/supervisord.conf reload'
    env.http_auth = False
    env.https = False
    env.browser_cache = True


def test(integration=1):
    """
    Execute the tests suite with the correct settings. Accept one
    argument that indicates when execute unit tests or not.

    Usage:
        $ fab test
        $ fab test:integration=0
    """
    command = 'django-admin.py test -v 2 --where=./apps --settings=drt.settings.testing'

    if int(integration) == 0:
        command += " --exclude='integration_tests' --exclude='jasmine_tests'"

    local(command)


def upload_configs():
    with lcd(env.local_path):
        upload_template('nginx/drt.conf',
                        '/etc/nginx/sites-enabled/drt.conf',
                        context={
                            'server_name': env.server_name,
                            'project_path': env.project_path,
                            'manage_path': env.manage_path,
                            'http_auth': env.http_auth,
                            'https': env.https,
                            'browser_cache': env.browser_cache
                        },
                        template_dir='{0}/config'.format(env.local_path),
                        use_jinja=True,
                        use_sudo=True)
        upload_template('supervisor/drt.conf',
                        '/etc/supervisor/conf.d/drt.conf',
                        context={
                            'settings_path': env.settings_path,
                            'project_path': env.project_path,
                            'manage_path': env.manage_path,
                            'user': env.user
                        },
                        template_dir='{0}/config'.format(env.local_path),
                        use_jinja=True,
                        use_sudo=True),


def upload_gunicorn():
    with lcd(env.local_path):
        upload_template('gunicorn/gunicorn_start',
                        '/web/drt.fm/gunicorn_start',
                        context={
                            'settings_path': env.settings_path,
                            'project_path': env.project_path,
                            'manage_path': env.manage_path,
                            'user': env.user,
                            'wsgi_module': env.wsgi_module
                        },
                        template_dir='{0}/config'.format(env.local_path),
                        use_jinja=True,
                        use_sudo=False),
        run('sudo chmod u+x {0}gunicorn_start'.format(env.project_path)),


def restart_services():
    sudo(env.supervisor_restart)
    sudo(env.nginx_restart)


def update_http_access():
    upload_template('nginx/.seap.htpasswd',
                    '/etc/nginx/.seap.htpasswd',
                    context={
                        'http_user': env.http_user,
                        'http_password': env.http_password
                    },
                    template_dir='{0}/config'.format(env.local_path),
                    use_jinja=True,
                    use_sudo=True)
    upload_configs()
    restart_services()


def update():
    # test()
    with cd(env.project_path):
        run('git checkout {0} && git pull'.format(env.git_branch))
    with virtualenv():
        _requirements_and_static()
        run('python manage.py migrate --settings={0}'.format(env.settings_path))
    upload_configs()
    upload_gunicorn
    restart_services()


def deploy():
    # test()
    upload_configs()
    with cd(env.parent_path):
        run('git clone {0} drt.fm'.format(env.git_url))
    with cd(env.project_path):
        run('virtualenv venv')
    with cd(env.manage_path):
        run('ln -s `pwd` ../venv/lib/python2.7/site-packages/drt')
    with virtualenv():
        _requirements_and_static()
        run('python manage.py syncdb --noinput --settings={0}'.format(env.settings_path))
        run('python manage.py migrate --fake --settings={0}'.format(env.settings_path))
        run('''echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@example.com', 'admin')" | python manage.py shell --settings={0}'''.format(env.settings_path))
    upload_gunicorn()
    restart_services()
