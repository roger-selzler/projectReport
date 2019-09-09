#!/bin/bash
DIR=$(date +"project_dump_%Y_%m_%d_%H_%M")
echo $DIR
# [ -d /var/backups/dump ] || /bin/mkdir /var/backups/dump
[ -d /var/backups/$DIR/dump ] || mkdir /var/backups/$DIR/dump
cd /var/backups/$DIR/dump
echo /var/backups/$DIR/dump
mongodump -o /var/backups/$DIR/dump
