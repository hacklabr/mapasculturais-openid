ID da Cultura Provider
======================

ID da Cultura - Provider OpenID para o Ministério da Cultura

Desenvolvido com Django (https://www.djangoproject.com/) e a biblioteca python-openid (https://github.com/openid/python-openid).

Ambiente de desenvolvimento
---------------------------

- sudo apt-get install python-setuptools python-virtualenv libmysqlclient-dev python-dev
- cd ~/devel
- mkdir ~/devel/mapasculturais-openid-env
- virtualenv ~/devel/mapasculturais-openid-env
- git clone git@github.com:hacklabr/mapasculturais-openid.git
- source mapasculturais-openid-env/bin/activate
- cd mapasculturais-openid
- easy_install -U distribute
- pip install -r dependencies.txt
- mysqladmin create mapasculturais-openid
- cp iddacultura/settings_local.py.sample iddacultura/settings_local.py
- ./manage.py syncdb
- ./manage.py runserver

Como usar
---------

- source ~/devel/mapasculturais-openid-env/bin/activate
- cd ~/devel/iddacultura-provider
- ./manage.py runserver
- Abrir no browser http://localhost:8000
