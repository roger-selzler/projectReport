#!/bin/bash
set -e # stop on first error.
PATHTOPROJECT=$(pwd)

echo $PATHTOPROJECT
cd /
sudo apt-get install apache2
sudo apt-get install libapache2-mod-wsgi
sudo a2enmod wsgi
cd $PATHTOPROJECT
[ -d "/var/www/sysc3010" ] || sudo mkdir /var/www/sysc3010
[ -d "/var/www/sysc3010/sysc3010" ] || sudo mkdir /var/www/sysc3010/sysc3010
sudo cp -sf $PATHTOPROJECT/sysc3010.conf /etc/apache2/sites-available/sysc3010.conf
sudo a2dissite 000-default.conf
sudo a2ensite sysc3010.conf

sudo cp -sf $PATHTOPROJECT/application.wsgi /var/www/sysc3010/application.wsgi
sudo cp -srf $PATHTOPROJECT/* /var/www/sysc3010/sysc3010/
sudo systemctl reload apache2
sudo service mongod start
sudo service apache2 restart

sudo apt-get install ufw
sudo ufw allow 80/tcp

cd /usr/local/src
[ -f noip-duc-linux.tar.gz ] || sudo wget http://www.no-ip.com/client/linux/noip-duc-linux.tar.gz
[ -d no-ip-2.1.9 ] || sudo tar xzf noip-duc-linux.tar.gz
cd noip-2.1.9-1/
sudo make
sudo make install
sudo /usr/local/bin/noip2
