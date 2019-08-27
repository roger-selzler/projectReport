#!/bin/bash
set -e # stop on first error.
sudo apt-get -y install python-pip
sudo pip install virtualenv
sudo apt-get -y install virtualenv

sudo virtualenv /prjvenv
source /prjvenv/bin/activate
pip install flask flask-user Flask-MongoEngine



# -- Install the mongoDB package
wget -qO - https://www.mongodb.org/static/pgp/server-4.2.asc | sudo apt-key add - 
echo "deb [ arch=amd64 ] https://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/4.2 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.2.list

sudo apt-get update
sudo apt-get install -y mongodb-org 
sudo service mongod start


# -- add autocompletion functionalities for vim
cd ~/ 
sudo apt-get install curl vim exuberant-ctags git ack-grep
sudo pip install pep8 flake8 pyflakes isort yapf 
[ -f ~/.vimrc ] || wget https://raw.github.com/fisadev/fisa-vim-config/master/.vimrc -O ~/.vimrc
vim -c :q! ~/.vimrc

# Create autocompletion for python on bash shell
[ -f ~/.pythonrc ] && echo "File ~/.pythonrc already exist" || touch ~/.pythonrc && sudo echo "try:
    import readline
    import rlcompleter
    readline.parse_and_bind(\"tab: complete\")
except ImportError:
    print(\"Module readline not available.\")" > ~/.pythonrc

[ -f ~/.bashrc ] || touch ~/.bashrc 
grep -qxF 'export PYTHONSTARTUP=~/.pythonrc' ~/.bashrc && echo 'export PYTHONSTARTUP=~/.pythonrc already exists on ~/.bashrc' || echo 'export PYTHONSTARTUP=~/.pythonrc' >> ~/.bashrc


