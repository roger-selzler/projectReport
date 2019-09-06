#!/bin/bash
set -e # stop on first error.
PATHTOPROJECT = $(pwd)
sudo apt-get -y install python-pip
sudo pip install virtualenv
sudo apt-get -y install virtualenv

virtualenv ~/prjvenv
source ~/prjvenv/bin/activate
pip install flask flask-user Flask-MongoEngine numpy Flask-Security flask-bcrypt pandas xlrd



# -- Install the mongoDB package
wget -qO - https://www.mongodb.org/static/pgp/server-4.2.asc | sudo apt-key add - 
echo "deb [ arch=amd64 ] https://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/4.2 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.2.list

sudo apt-get update
sudo apt-get install -y mongodb-org 
sudo service mongod start


# -- add autocompletion functionalities for vim
cd ~/ 
sudo apt-get install curl vim exuberant-ctags git ack-grep
pip install pep8 flake8 pyflakes isort yapf 
[ -f ~/.vimrc ] || wget https://raw.github.com/fisadev/fisa-vim-config/master/.vimrc -O ~/.vimrc
vim -c :q! ~/.vimrc

# Create autocompletion for python on bash shell
if [ -f ~/.pythonrc ]; then
	echo "File ~/.pythonrc already exist"
else
	touch ~/.pythonrc
	sudo echo "try:
    import readline
    import rlcompleter
    readline.parse_and_bind(\"tab: complete\")
except ImportError:
    print(\"Module readline not available.\")" > ~/.pythonrc
fi

[ -f ~/.bashrc ] || touch ~/.bashrc 
grep -qxF 'export PYTHONSTARTUP=~/.pythonrc' ~/.bashrc && echo 'export PYTHONSTARTUP=~/.pythonrc already exists on ~/.bashrc' || echo 'export PYTHONSTARTUP=~/.pythonrc' >> ~/.bashrc

# preparing google cloud platform
# echo "Installing google cloud sdk - need account and project information"
# echo "Refer to https://cloud.google.com/sdk/docs/#linux"
# cd ~/
# [ -f google-cloud-sdk*.tar.gz] && echo "Google cloud files already exist" || wget https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-260.0.0-linux-x86_64.tar.gz
# tar -xvzf google-cloud-sdk-*.tar.gz
# ./google-cloud-sdk/install.sh
# ./google-cloud-sdk/bin/gcloud init



sudo apt-get install apache2
sudo apt-get install libapache2-mod-wsgi
sudo a2enmod wsgi
cd PATHTOPROJECT
[ -d "/var/www/sysc3010" ] || sudo mkdir /var/www/sysc3010
cd sysc3010
[ -d "/var/www/sysc3010/sysc3010" ] || sudo mkdir /var/www/sysc3010/sysc3010
sudo cp -s PATHTOPROJECT+/sysc3010.conf /etc/apache2/sites-available/sysc3010.conf
