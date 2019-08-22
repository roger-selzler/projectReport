#!/bin/bash
sudo apt-get -y install python-pip
pip install virtualenv
sudo apt-get -y install virtualenv

virtualenv /venv
source /venv/bin/activate
pip install flask

