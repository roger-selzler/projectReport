#!/usr/bin/python
# from flup.server.fcgi import WSGIServer
import sys
import logging
import os
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/var/www/sysc3010/sysc3010/')

activate_this = os.path.expanduser('~/prjvenv/bin/activate_this.py')
execfile(activate_this, dict(__file__=activate_this))

from main import app as application
application.secret_key = "anykey"

# if __name__ == '__main__':
#     WSGIServer(app).run()

 