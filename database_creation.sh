#!/bin/bash

BASEDIR=$(dirname $0)

if [ -f "$BASEDIR/base.db" ]; then
	rm "$BASEDIR/base.db"
fi

ADMIN_USER=admin
ADMIN_EMAIL=asd@asd.asd

echo Digite a senha após o ./manage.py entrar em espera
echo Pressione Enter para continuar...

read

./manage.py syncdb << EOF
yes
$ADMIN_USER
$ADMIN_EMAIL
EOF

APP_SECRET=9a6a249b9c50f6062bc6b1dfdfab66e2
APP_ID=302841666574002

sqlite3 base.db << EOF
UPDATE django_site SET DOMAIN = '127.0.0.1:8000', name = 'Mapas Culturais OpenID' WHERE id=1;
INSERT INTO socialaccount_socialapp (provider, name, secret, client_id, 'key') VALUES ('facebook', 'Facebook', '$APP_SECRET', 'APP_ID', '');
INSERT INTO socialaccount_socialapp_sites (socialapp_id, site_id) VALUES (1,1);
EOF
