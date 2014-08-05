ID da Cultura Provider
======================

ID da Cultura - Provider OpenID para o Ministério da Cultura

Desenvolvido com Django (https://www.djangoproject.com/) e a biblioteca python-openid (https://github.com/openid/python-openid).

Ambiente de desenvolvimento
---------------------------

- sudo apt-get install python-setuptools python-virtualenv python-dev build-essential
- cd ~/devel
- mkdir ~/devel/mapasculturais-openid-env
- virtualenv ~/devel/mapasculturais-openid-env
  -  [for arch linux] virtualenv -p \`which python2\`  ~/devel/mapasculturais-openid-env
- git clone git@github.com:hacklabr/mapasculturais-openid.git
- source mapasculturais-openid-env/bin/activate
- cd mapasculturais-openid
- pip install -r requirements.txt
- cp iddacultura/settings_local.py.sample iddacultura/settings_local.py
- gedit iddacultura/settings_local.py
- Inserir as chaves do recaptcha no final do arquivo (é preciso ter ou criar uma conta no site do Recaptcha)
- ./manage.py syncdb
- ./manage.py runserver

Como usar
---------

- source ~/devel/mapasculturais-openid-env/bin/activate
- cd ~/devel/mapasculturais-openid
- ./manage.py runserver
- Abrir no browser http://localhost:8000
